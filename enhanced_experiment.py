"""
Enhanced Experiment Script with Philosophical Reasoning Integration
Extends the original experiment.py with comprehensive philosophical capabilities
"""

import os
import time
import math
import pickle
import inspect
import json
from contextlib import nullcontext
from dataclasses import dataclass
import numpy as np
import torch
import torch.nn as nn
from torch.nn import functional as F
import argparse
from typing import Dict, List, Tuple, Optional, Any

# Import philosophical modules
from ai_philosopher_core import (
    AIPhilosopherCore, 
    PhilosophicalConfig,
    create_philosopher_config,
    integrate_with_gpt_model
)
from nihiltheism_framework import (
    NihiltheismFramework,
    create_nihiltheism_framework,
    quick_nihiltheistic_analysis
)

# Original model architecture (preserved from experiment.py)
class LayerNorm(nn.Module):
    """LayerNorm but with an optional bias. PyTorch doesn't support simply bias=False"""

    def __init__(self, ndim, bias):
        super().__init__()
        self.weight = nn.Parameter(torch.ones(ndim))
        self.bias = nn.Parameter(torch.zeros(ndim)) if bias else None

    def forward(self, input):
        return F.layer_norm(input, self.weight.shape, self.weight, self.bias, 1e-5)

class CausalSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        assert config.n_embd % config.n_head == 0
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_embd, bias=config.bias)
        self.c_proj = nn.Linear(config.n_embd, config.n_embd, bias=config.bias)
        self.attn_dropout = nn.Dropout(config.dropout)
        self.resid_dropout = nn.Dropout(config.dropout)
        self.n_head = config.n_head
        self.n_embd = config.n_embd
        self.dropout = config.dropout
        self.flash = hasattr(torch.nn.functional, "scaled_dot_product_attention")
        if not self.flash:
            print("WARNING: using slow attention. Flash Attention requires PyTorch >= 2.0")
            self.register_buffer(
                "bias",
                torch.tril(torch.ones(config.block_size, config.block_size)).view(
                    1, 1, config.block_size, config.block_size
                ),
            )

    def forward(self, x):
        B, T, C = x.size()
        q, k, v = self.c_attn(x).split(self.n_embd, dim=2)
        k = k.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        q = q.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)
        v = v.view(B, T, self.n_head, C // self.n_head).transpose(1, 2)

        if self.flash:
            y = torch.nn.functional.scaled_dot_product_attention(
                q, k, v, attn_mask=None,
                dropout_p=self.dropout if self.training else 0,
                is_causal=True,
            )
        else:
            att = (q @ k.transpose(-2, -1)) * (1.0 / math.sqrt(k.size(-1)))
            att = att.masked_fill(self.bias[:, :, :T, :T] == 0, float("-inf"))
            att = F.softmax(att, dim=-1)
            att = self.attn_dropout(att)
            y = att @ v
        y = y.transpose(1, 2).contiguous().view(B, T, C)
        y = self.resid_dropout(self.c_proj(y))
        return y

class MLP(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.c_fc = nn.Linear(config.n_embd, 4 * config.n_embd, bias=config.bias)
        self.gelu = nn.GELU()
        self.c_proj = nn.Linear(4 * config.n_embd, config.n_embd, bias=config.bias)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x):
        x = self.c_fc(x)
        x = self.gelu(x)
        x = self.c_proj(x)
        x = self.dropout(x)
        return x

class Block(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.ln_1 = LayerNorm(config.n_embd, bias=config.bias)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = LayerNorm(config.n_embd, bias=config.bias)
        self.mlp = MLP(config)

    def forward(self, x):
        x = x + self.attn(self.ln_1(x))
        x = x + self.mlp(self.ln_2(x))
        return x

@dataclass
class GPTConfig:
    block_size: int = 1024
    vocab_size: int = 50304
    n_layer: int = 12
    n_head: int = 12
    n_embd: int = 768
    dropout: float = 0.0
    bias: bool = True

@dataclass
class EnhancedGPTConfig(GPTConfig):
    """Extended configuration including philosophical parameters"""
    # Philosophical reasoning parameters
    enable_philosophy: bool = True
    inner_monologue_depth: int = 3
    reflection_iterations: int = 2
    nihiltheism_weight: float = 0.5
    humor_factor: float = 0.3
    philosophical_temperature: float = 0.8
    
    # Integration parameters
    philosophy_integration_mode: str = "full"  # "off", "partial", "full"
    enable_terminology_generation: bool = True
    enable_thought_experiments: bool = True
    enable_humorous_nihilism: bool = True
    
    # API and validation parameters
    use_external_apis: bool = False  # Set to True when APIs available
    originality_threshold: float = 0.7
    max_api_retries: int = 3
    api_timeout: float = 10.0

class EnhancedGPT(nn.Module):
    """Enhanced GPT with integrated philosophical reasoning capabilities"""

    def __init__(self, config: EnhancedGPTConfig):
        super().__init__()
        assert config.vocab_size is not None
        assert config.block_size is not None
        self.config = config

        # Original transformer architecture
        self.transformer = nn.ModuleDict(dict(
            wte=nn.Embedding(config.vocab_size, config.n_embd),
            wpe=nn.Embedding(config.block_size, config.n_embd),
            drop=nn.Dropout(config.dropout),
            h=nn.ModuleList([Block(config) for _ in range(config.n_layer)]),
            ln_f=LayerNorm(config.n_embd, bias=config.bias),
        ))
        self.lm_head = nn.Linear(config.n_embd, config.vocab_size, bias=False)
        self.transformer.wte.weight = self.lm_head.weight

        # Initialize philosophical components
        if config.enable_philosophy:
            philosophical_config = create_philosopher_config(
                enable_philosophy=config.enable_philosophy,
                inner_monologue_depth=config.inner_monologue_depth,
                reflection_iterations=config.reflection_iterations,
                nihiltheism_weight=config.nihiltheism_weight,
                humor_factor=config.humor_factor
            )
            self.philosopher = integrate_with_gpt_model(self, philosophical_config)
            self.nihiltheism_framework = create_nihiltheism_framework()
        else:
            self.philosopher = None
            self.nihiltheism_framework = None

        # Initialize weights
        self.apply(self._init_weights)
        for pn, p in self.named_parameters():
            if pn.endswith("c_proj.weight"):
                torch.nn.init.normal_(p, mean=0.0, std=0.02 / math.sqrt(2 * config.n_layer))

        print("number of parameters: %.2fM" % (self.get_num_params() / 1e6,))
        if config.enable_philosophy:
            print("Philosophical reasoning: ENABLED")
            print(f"Inner monologue depth: {config.inner_monologue_depth}")
            print(f"Reflection iterations: {config.reflection_iterations}")
            print(f"Nihiltheism weight: {config.nihiltheism_weight}")

    def get_num_params(self, non_embedding=True):
        n_params = sum(p.numel() for p in self.parameters())
        if non_embedding:
            n_params -= self.transformer.wpe.weight.numel()
        return n_params

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                torch.nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            torch.nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, idx, targets=None):
        device = idx.device
        b, t = idx.size()
        assert t <= self.config.block_size, f"Cannot forward sequence of length {t}, block size is only {self.config.block_size}"
        pos = torch.arange(0, t, dtype=torch.long, device=device)

        tok_emb = self.transformer.wte(idx)
        pos_emb = self.transformer.wpe(pos)
        x = self.transformer.drop(tok_emb + pos_emb)
        for block in self.transformer.h:
            x = block(x)
        x = self.transformer.ln_f(x)

        if targets is not None:
            logits = self.lm_head(x)
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1), ignore_index=-1)
        else:
            logits = self.lm_head(x[:, [-1], :])
            loss = None

        return logits, loss

    @torch.no_grad()
    def generate(self, idx, max_new_tokens, temperature=1.0, top_k=None, 
                philosophical_mode=False, enable_reflection=False):
        """Enhanced generation with optional philosophical processing"""
        
        # Standard generation
        for _ in range(max_new_tokens):
            idx_cond = idx if idx.size(1) <= self.config.block_size else idx[:, -self.config.block_size:]
            logits, _ = self(idx_cond)
            logits = logits[:, -1, :] / temperature
            if top_k is not None:
                v, _ = torch.topk(logits, min(top_k, logits.size(-1)))
                logits[logits < v[:, [-1]]] = -float("Inf")
            probs = F.softmax(logits, dim=-1)
            idx_next = torch.multinomial(probs, num_samples=1)
            idx = torch.cat((idx, idx_next), dim=1)

        return idx

    def generate_philosophical_response(self, prompt: str, max_new_tokens: int = 500,
                                      temperature: float = None, enable_reflection: bool = True,
                                      philosophical_concept: str = None) -> Dict[str, Any]:
        """Generate response with full philosophical reasoning capabilities"""
        
        if not self.config.enable_philosophy or not self.philosopher:
            return {"error": "Philosophical reasoning not enabled"}
        
        # Use philosophical temperature if not specified
        if temperature is None:
            temperature = self.config.philosophical_temperature
        
        # Process through philosophical framework
        philosophical_response = self.philosopher.generate_philosophical_response(
            prompt=prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            enable_reflection=enable_reflection
        )
        
        # Apply Nihiltheism framework if concept specified
        if philosophical_concept and self.nihiltheism_framework:
            nihiltheistic_analysis = self.nihiltheism_framework.develop_nihiltheistic_concept(
                concept_name=philosophical_concept,
                philosophical_problem=prompt,
                enable_humor=self.config.enable_humorous_nihilism,
                enable_terminology=self.config.enable_terminology_generation,
                enable_experiments=self.config.enable_thought_experiments
            )
            philosophical_response["nihiltheistic_analysis"] = nihiltheistic_analysis
        
        # Perform reflection and iteration if enabled
        if enable_reflection and self.config.reflection_iterations > 0:
            reflection_result = self.philosopher.reflect_and_iterate(philosophical_response)
            philosophical_response["reflection_process"] = reflection_result
        
        return philosophical_response

def train_with_philosophy(dataset="shakespeare_char", out_dir="run_0", seed_offset=0, 
                         philosophical_config: Dict[str, Any] = None):
    """Enhanced training function with philosophical capabilities"""
    
    # Default philosophical configuration
    if philosophical_config is None:
        philosophical_config = {
            "enable_philosophy": True,
            "inner_monologue_depth": 2,
            "reflection_iterations": 1,
            "nihiltheism_weight": 0.3,
            "humor_factor": 0.2,
            "philosophy_integration_mode": "partial"
        }
    
    # Configuration (preserved from original with enhancements)
    gradient_accumulation_steps = 1
    batch_size = 64 if dataset == "shakespeare_char" else 32
    block_size = 256
    eval_interval = 250 if dataset == "shakespeare_char" else 1000
    log_interval = 10 if dataset == "shakespeare_char" else 100
    eval_iters = 200
    eval_only = False
    always_save_checkpoint = False
    never_save_checkpoint = True
    
    # Enhanced model configuration
    enhanced_config = EnhancedGPTConfig(
        # Original parameters
        block_size=block_size,
        vocab_size=50304,
        n_layer=6,
        n_head=6,
        n_embd=384,
        dropout=0.2,
        bias=False,
        # Philosophical parameters
        **philosophical_config
    )
    
    # Training parameters
    learning_rate = 1e-3 if dataset == "shakespeare_char" else 5e-4
    max_iters = 5000 if dataset == "shakespeare_char" else 100000
    weight_decay = 1e-1
    beta1 = 0.9
    beta2 = 0.99
    grad_clip = 1.0
    decay_lr = True
    warmup_iters = 100 if dataset == "shakespeare_char" else 200
    lr_decay_iters = max_iters
    min_lr = 1e-4 if dataset == "shakespeare_char" else 5e-5
    
    # System configuration
    device = "cuda"
    dtype = "bfloat16" if torch.cuda.is_available() and torch.cuda.is_bf16_supported() else "float16"
    compile = True
    
    # Setup
    master_process = True
    tokens_per_iter = gradient_accumulation_steps * batch_size * block_size
    print(f"tokens per iteration will be: {tokens_per_iter:,}")
    
    if master_process:
        os.makedirs(out_dir, exist_ok=True)
    torch.manual_seed(1337 + seed_offset)
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    device_type = "cuda" if "cuda" in device else "cpu"
    ptdtype = {"float32": torch.float32, "bfloat16": torch.bfloat16, "float16": torch.float16}[dtype]
    ctx = nullcontext() if device_type == "cpu" else torch.amp.autocast(device_type=device_type, dtype=ptdtype)
    
    # Data loading
    if out_dir == "run_0":
        data_dir = os.path.join("../../data", dataset)
    else:
        data_dir = os.path.join("../../../data", dataset)
    
    def get_batch(split):
        if split == "train":
            data = np.memmap(os.path.join(data_dir, "train.bin"), dtype=np.uint16, mode="r")
        else:
            data = np.memmap(os.path.join(data_dir, "val.bin"), dtype=np.uint16, mode="r")
        ix = torch.randint(len(data) - block_size, (batch_size,))
        x = torch.stack([torch.from_numpy((data[i:i+block_size]).astype(np.int64)) for i in ix])
        y = torch.stack([torch.from_numpy((data[i+1:i+1+block_size]).astype(np.int64)) for i in ix])
        if device_type == "cuda":
            x, y = x.pin_memory().to(device, non_blocking=True), y.pin_memory().to(device, non_blocking=True)
        else:
            x, y = x.to(device), y.to(device)
        return x, y
    
    # Model initialization
    if not os.path.exists(os.path.join(data_dir, "meta.pkl")):
        print(f"meta.pkl not found in {data_dir}, using default vocab")
        meta_vocab_size = None
    else:
        with open(os.path.join(data_dir, "meta.pkl"), "rb") as f:
            meta = pickle.load(f)
        meta_vocab_size = meta["vocab_size"]
        print(f"found vocab_size = {meta_vocab_size} (inside {data_dir}/meta.pkl)")
    
    if meta_vocab_size is not None:
        enhanced_config.vocab_size = meta_vocab_size
    
    # Create enhanced model
    model = EnhancedGPT(enhanced_config)
    model.to(device)
    
    # Optimizer
    optimizer = model.configure_optimizers(weight_decay, learning_rate, (beta1, beta2), device_type)
    if compile:
        print("compiling the model... (takes a ~minute)")
        unoptimized_model = model
        model = torch.compile(model)
    
    # Training loop (abbreviated for space - would include full training logic)
    @torch.no_grad()
    def estimate_loss():
        out = {}
        model.eval()
        for split in ["train", "val"]:
            losses = torch.zeros(eval_iters)
            for k in range(eval_iters):
                X, Y = get_batch(split)
                with ctx:
                    logits, loss = model(X, Y)
                losses[k] = loss.item()
            out[split] = losses.mean()
        model.train()
        return out
    
    # Training metrics tracking
    train_log_info = {"iter": [], "loss": []}
    val_log_info = {"iter": [], "loss": []}
    
    # Philosophical analysis tracking
    philosophical_metrics = {
        "philosophical_responses_generated": 0,
        "nihiltheistic_concepts_developed": 0,
        "humor_applications": 0,
        "reflection_iterations_completed": 0
    }
    
    # Main training loop
    X, Y = get_batch("train")
    t0 = time.time()
    local_iter_num = 0
    raw_model = model.module if compile else model
    running_mfu = -1.0
    
    for iter_num in range(max_iters):
        # Learning rate scheduling
        lr = learning_rate if not decay_lr else get_lr(iter_num, warmup_iters, lr_decay_iters, learning_rate, min_lr)
        for param_group in optimizer.param_groups:
            param_group["lr"] = lr
        
        # Evaluation
        if iter_num % eval_interval == 0 and master_process:
            losses = estimate_loss()
            print(f"step {iter_num}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")
            train_log_info["iter"].append(iter_num)
            train_log_info["loss"].append(losses["train"])
            val_log_info["iter"].append(iter_num)
            val_log_info["loss"].append(losses["val"])
            
            # Philosophical evaluation
            if enhanced_config.enable_philosophy and iter_num > 0:
                test_prompt = "What is the meaning of existence?"
                try:
                    phil_response = raw_model.generate_philosophical_response(
                        prompt=test_prompt,
                        max_new_tokens=100,
                        enable_reflection=True,
                        philosophical_concept="existential_inquiry"
                    )
                    philosophical_metrics["philosophical_responses_generated"] += 1
                    if "nihiltheistic_analysis" in phil_response:
                        philosophical_metrics["nihiltheistic_concepts_developed"] += 1
                    print(f"Philosophical analysis generated successfully at iter {iter_num}")
                except Exception as e:
                    print(f"Philosophical analysis failed at iter {iter_num}: {e}")
        
        # Training step
        for micro_step in range(gradient_accumulation_steps):
            with ctx:
                logits, loss = model(X, Y)
                loss = loss / gradient_accumulation_steps
            X, Y = get_batch("train")
            loss.backward()
        
        if grad_clip != 0.0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), grad_clip)
        optimizer.step()
        optimizer.zero_grad(set_to_none=True)
        
        # Timing and logging
        t1 = time.time()
        dt = t1 - t0
        t0 = t1
        if iter_num % log_interval == 0 and master_process:
            lossf = loss.item() * gradient_accumulation_steps
            if local_iter_num >= 5:
                mfu = raw_model.estimate_mfu(batch_size * gradient_accumulation_steps, dt)
                running_mfu = mfu if running_mfu == -1.0 else 0.9*running_mfu + 0.1*mfu
            print(f"iter {iter_num}: loss {lossf:.4f}, time {dt*1000:.2f}ms, mfu {running_mfu*100:.2f}%")
        local_iter_num += 1
    
    # Final evaluation and inference
    print("Training completed. Performing final philosophical evaluation...")
    
    # Load meta for inference
    meta_path = os.path.join(data_dir, "meta.pkl")
    if os.path.exists(meta_path):
        with open(meta_path, "rb") as f:
            meta = pickle.load(f)
        stoi, itos = meta["stoi"], meta["itos"]
        encode = lambda s: [stoi[c] for c in s]
        decode = lambda l: "".join([itos[i] for i in l])
        
        # Test philosophical generation
        philosophical_test_prompts = [
            "What is the meaning of life?",
            "How should we respond to existential crisis?",
            "What is the relationship between technology and humanity?"
        ]
        
        final_philosophical_results = []
        
        for prompt in philosophical_test_prompts:
            if enhanced_config.enable_philosophy:
                phil_result = raw_model.generate_philosophical_response(
                    prompt=prompt,
                    max_new_tokens=200,
                    enable_reflection=True,
                    philosophical_concept=f"analysis_{len(final_philosophical_results)}"
                )
                final_philosophical_results.append(phil_result)
                philosophical_metrics["philosophical_responses_generated"] += 1
        
        # Standard text generation for comparison
        start = "What is the meaning"
        start_ids = encode(start)
        x = torch.tensor(start_ids, dtype=torch.long, device=device)[None, ...]
        
        model.eval()
        with torch.no_grad():
            with ctx:
                y = model.generate(x, 100, temperature=0.8, top_k=200)
                standard_result = decode(y[0].tolist())
                print("Standard generation:")
                print(standard_result)
    
    # Compile final results
    final_info = {
        "dataset": dataset,
        "seed_offset": seed_offset,
        "final_train_loss": train_log_info["loss"][-1] if train_log_info["loss"] else float("inf"),
        "final_val_loss": val_log_info["loss"][-1] if val_log_info["loss"] else float("inf"),
        "philosophical_metrics": philosophical_metrics,
        "enhanced_config": enhanced_config.__dict__,
        "training_completed": True
    }
    
    # Save philosophical development history
    if enhanced_config.enable_philosophy and raw_model.nihiltheism_framework:
        philosophy_export_path = os.path.join(out_dir, f"philosophical_development_{dataset}_{seed_offset}.json")
        raw_model.nihiltheism_framework.export_framework_development(philosophy_export_path)
        final_info["philosophical_export_path"] = philosophy_export_path
    
    return final_info, train_log_info, val_log_info

def get_lr(it, warmup_iters, lr_decay_iters, learning_rate, min_lr):
    """Learning rate scheduler"""
    if it < warmup_iters:
        return learning_rate * it / warmup_iters
    if it > lr_decay_iters:
        return min_lr
    decay_ratio = (it - warmup_iters) / (lr_decay_iters - warmup_iters)
    assert 0 <= decay_ratio <= 1
    coeff = 0.5 * (1.0 + math.cos(math.pi * decay_ratio))
    return min_lr + coeff * (learning_rate - min_lr)

# Enhanced model methods
def configure_optimizers(self, weight_decay, learning_rate, betas, device_type):
    """Configure optimizers (method to be added to EnhancedGPT)"""
    param_dict = {pn: p for pn, p in self.named_parameters()}
    param_dict = {pn: p for pn, p in param_dict.items() if p.requires_grad}
    
    decay_params = [p for n, p in param_dict.items() if p.dim() >= 2]
    nodecay_params = [p for n, p in param_dict.items() if p.dim() < 2]
    optim_groups = [
        {"params": decay_params, "weight_decay": weight_decay},
        {"params": nodecay_params, "weight_decay": 0.0}
    ]
    
    use_fused = (device_type == "cuda") and ("fused" in inspect.signature(torch.optim.AdamW).parameters)
    extra_args = dict(fused=True) if use_fused else dict()
    optimizer = torch.optim.AdamW(optim_groups, lr=learning_rate, betas=betas, **extra_args)
    
    return optimizer

def estimate_mfu(self, fwdbwd_per_iter, dt):
    """Estimate model flops utilization"""
    N = self.get_num_params()
    cfg = self.config
    L, H, Q, T = cfg.n_layer, cfg.n_head, cfg.n_embd//cfg.n_head, cfg.block_size
    flops_per_token = 6*N + 12*L*H*Q*T
    flops_per_fwdbwd = flops_per_token * T
    flops_per_iter = flops_per_fwdbwd * fwdbwd_per_iter
    flops_achieved = flops_per_iter * (1.0/dt)
    flops_promised = 312e12  # A100 peak flops is 312 TFLOPS bf16
    mfu = flops_achieved / flops_promised
    return mfu

# Add methods to EnhancedGPT class
EnhancedGPT.configure_optimizers = configure_optimizers
EnhancedGPT.estimate_mfu = estimate_mfu

# Command line interface
def main():
    parser = argparse.ArgumentParser(description="Run enhanced experiment with philosophical reasoning")
    parser.add_argument("--out_dir", type=str, default="run_philosophical", help="Output directory")
    parser.add_argument("--enable_philosophy", action="store_true", default=True, help="Enable philosophical reasoning")
    parser.add_argument("--inner_monologue_depth", type=int, default=3, help="Depth of inner monologue")
    parser.add_argument("--reflection_iterations", type=int, default=2, help="Number of reflection iterations")
    parser.add_argument("--nihiltheism_weight", type=float, default=0.5, help="Weight for Nihiltheistic concepts")
    parser.add_argument("--humor_factor", type=float, default=0.3, help="Humor factor for philosophical responses")
    parser.add_argument("--philosophy_mode", type=str, default="full", choices=["off", "partial", "full"], 
                       help="Philosophy integration mode")
    
    args = parser.parse_args()
    
    # Configure philosophical parameters
    philosophical_config = {
        "enable_philosophy": args.enable_philosophy,
        "inner_monologue_depth": args.inner_monologue_depth,
        "reflection_iterations": args.reflection_iterations,
        "nihiltheism_weight": args.nihiltheism_weight,
        "humor_factor": args.humor_factor,
        "philosophy_integration_mode": args.philosophy_mode,
        "enable_terminology_generation": True,
        "enable_thought_experiments": True,
        "enable_humorous_nihilism": True
    }
    
    print("Enhanced Experiment with Philosophical Reasoning")
    print("=" * 50)
    print(f"Philosophical reasoning: {'ENABLED' if args.enable_philosophy else 'DISABLED'}")
    print(f"Inner monologue depth: {args.inner_monologue_depth}")
    print(f"Reflection iterations: {args.reflection_iterations}")
    print(f"Nihiltheism weight: {args.nihiltheism_weight}")
    print(f"Humor factor: {args.humor_factor}")
    print(f"Philosophy mode: {args.philosophy_mode}")
    print("=" * 50)
    
    # Run experiments
    num_seeds = {"shakespeare_char": 2, "enwik8": 1, "text8": 1}  # Reduced for testing
    
    out_dir = args.out_dir
    all_results = {}
    final_infos = {}
    
    for dataset in ["shakespeare_char"]:  # Focus on one dataset for initial testing
        final_info_list = []
        for seed_offset in range(num_seeds[dataset]):
            print(f"\nRunning {dataset} with seed offset {seed_offset}")
            final_info, train_info, val_info = train_with_philosophy(
                dataset, out_dir, seed_offset, philosophical_config
            )
            all_results[f"{dataset}_{seed_offset}_final_info"] = final_info
            all_results[f"{dataset}_{seed_offset}_train_info"] = train_info
            all_results[f"{dataset}_{seed_offset}_val_info"] = val_info
            final_info_list.append(final_info)
        
        # Aggregate results
        final_info_dict = {k: [d[k] for d in final_info_list] for k in final_info_list[0].keys() if isinstance(final_info_list[0][k], (int, float))}
        means = {f"{k}_mean": np.mean(v) for k, v in final_info_dict.items()}
        stderrs = {f"{k}_stderr": np.std(v) / len(v) for k, v in final_info_dict.items()}
        final_infos[dataset] = {
            "means": means,
            "stderrs": stderrs,
            "final_info_dict": final_info_dict,
        }
    
    # Save results
    with open(os.path.join(out_dir, "enhanced_final_info.json"), "w") as f:
        json.dump(final_infos, f, indent=2)
    
    with open(os.path.join(out_dir, "enhanced_all_results.npy"), "wb") as f:
        np.save(f, all_results)
    
    print(f"\nResults saved to {out_dir}")
    print("Enhanced experiment completed successfully!")

if __name__ == "__main__":
    main()
