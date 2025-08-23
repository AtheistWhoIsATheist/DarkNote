"""
Configuration Loader for Philosophical AI System
Handles loading, validation, and customization of philosophical configurations
"""

import json
import os
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass
import copy

from ai_philosopher_core import PhilosophicalConfig

@dataclass
class PhilosophicalSystemConfig:
    """Complete configuration for the philosophical AI system"""
    
    # Core philosophical parameters
    enable_philosophy: bool = True
    philosophy_integration_mode: str = "full"
    
    # Inner monologue configuration
    inner_monologue_depth: int = 3
    enable_structured_reflection: bool = True
    
    # Nihiltheism framework
    enable_nihiltheism: bool = True
    nihiltheism_weight: float = 0.5
    enable_terminology_generation: bool = True
    enable_thought_experiments: bool = True
    
    # Humorous nihilism
    enable_humor: bool = True
    humor_factor: float = 0.3
    amusement_threshold: float = 0.6
    
    # Reflection and iteration
    enable_reflection: bool = True
    reflection_iterations: int = 2
    enable_self_critique: bool = True
    
    # External APIs
    enable_external_validation: bool = False
    use_philpapers_api: bool = False
    api_timeout: float = 10.0
    max_retries: int = 3
    
    # Generation parameters
    philosophical_temperature: float = 0.8
    creativity_boost: float = 0.2
    coherence_weight: float = 0.7
    novelty_preference: float = 0.6
    
    # Output and evaluation
    include_metadata: bool = True
    show_reasoning_process: bool = True
    track_originality: bool = True
    
    # Safety and ethics
    avoid_harmful_conclusions: bool = True
    maintain_intellectual_humility: bool = True
    
    def to_philosophical_config(self) -> PhilosophicalConfig:
        """Convert to PhilosophicalConfig for core system"""
        return PhilosophicalConfig(
            enable_philosophy=self.enable_philosophy,
            inner_monologue_depth=self.inner_monologue_depth,
            reflection_iterations=self.reflection_iterations,
            originality_threshold=0.7,  # Default value
            nihiltheism_weight=self.nihiltheism_weight,
            humor_factor=self.humor_factor,
            use_external_apis=self.enable_external_validation,
            max_api_retries=self.max_retries,
            api_timeout=self.api_timeout
        )

class ConfigurationLoader:
    """Loads and manages philosophical AI configurations"""
    
    def __init__(self, default_config_path: str = None):
        self.default_config_path = default_config_path or os.path.join(
            os.path.dirname(__file__), "philosophical_config.json"
        )
        self.loaded_config = None
        self.presets = {}
        self._load_default_config()
    
    def _load_default_config(self):
        """Load the default configuration file"""
        try:
            with open(self.default_config_path, 'r') as f:
                self.loaded_config = json.load(f)
            
            # Extract presets
            if "preset_configurations" in self.loaded_config:
                self.presets = self.loaded_config["preset_configurations"]
                
        except FileNotFoundError:
            print(f"Warning: Default config file not found at {self.default_config_path}")
            self.loaded_config = self._create_fallback_config()
        except json.JSONDecodeError as e:
            print(f"Error parsing config file: {e}")
            self.loaded_config = self._create_fallback_config()
    
    def _create_fallback_config(self) -> Dict[str, Any]:
        """Create a fallback configuration if file loading fails"""
        return {
            "philosophical_reasoning": {"enable_philosophy": True},
            "inner_monologue": {"depth": 3},
            "nihiltheism_framework": {
                "enable_nihiltheism": True,
                "nihiltheism_weight": 0.5,
                "enable_terminology_generation": True,
                "enable_thought_experiments": True
            },
            "humorous_nihilism": {
                "enable_humor": True,
                "humor_factor": 0.3
            },
            "reflection_and_iteration": {
                "enable_reflection": True,
                "reflection_iterations": 2
            },
            "external_apis": {
                "enable_external_validation": False,
                "api_timeout": 10.0,
                "max_retries": 3
            },
            "preset_configurations": {
                "standard": {
                    "enable_philosophy": True,
                    "inner_monologue_depth": 3,
                    "reflection_iterations": 2,
                    "nihiltheism_weight": 0.5,
                    "humor_factor": 0.3
                }
            }
        }
    
    def load_preset(self, preset_name: str) -> PhilosophicalSystemConfig:
        """Load a preset configuration"""
        if preset_name not in self.presets:
            available_presets = list(self.presets.keys())
            raise ValueError(f"Preset '{preset_name}' not found. Available: {available_presets}")
        
        preset_config = self.presets[preset_name]
        return self._create_system_config(preset_config)
    
    def load_custom_config(self, config_file: str) -> PhilosophicalSystemConfig:
        """Load a custom configuration file"""
        try:
            with open(config_file, 'r') as f:
                custom_config = json.load(f)
            return self._create_system_config(custom_config)
        except FileNotFoundError:
            raise FileNotFoundError(f"Custom config file not found: {config_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing custom config file: {e}")
    
    def load_with_overrides(self, preset_name: str = "standard", 
                           overrides: Dict[str, Any] = None) -> PhilosophicalSystemConfig:
        """Load preset configuration with custom overrides"""
        base_config = self.load_preset(preset_name)
        
        if overrides:
            # Apply overrides to the configuration
            config_dict = self._system_config_to_dict(base_config)
            config_dict.update(overrides)
            return self._create_system_config(config_dict)
        
        return base_config
    
    def _create_system_config(self, config_data: Dict[str, Any]) -> PhilosophicalSystemConfig:
        """Create PhilosophicalSystemConfig from configuration data"""
        
        # Extract values with defaults
        system_config = PhilosophicalSystemConfig()
        
        # Philosophical reasoning
        phil_reasoning = config_data.get("philosophical_reasoning", {})
        system_config.enable_philosophy = phil_reasoning.get("enable_philosophy", True)
        system_config.philosophy_integration_mode = phil_reasoning.get("philosophy_integration_mode", "full")
        
        # Inner monologue
        inner_monologue = config_data.get("inner_monologue", {})
        system_config.inner_monologue_depth = inner_monologue.get("depth", 3)
        system_config.enable_structured_reflection = inner_monologue.get("enable_structured_reflection", True)
        
        # Nihiltheism framework
        nihiltheism = config_data.get("nihiltheism_framework", {})
        system_config.enable_nihiltheism = nihiltheism.get("enable_nihiltheism", True)
        system_config.nihiltheism_weight = nihiltheism.get("nihiltheism_weight", 0.5)
        system_config.enable_terminology_generation = nihiltheism.get("enable_terminology_generation", True)
        system_config.enable_thought_experiments = nihiltheism.get("enable_thought_experiments", True)
        
        # Humorous nihilism
        humor = config_data.get("humorous_nihilism", {})
        system_config.enable_humor = humor.get("enable_humor", True)
        system_config.humor_factor = humor.get("humor_factor", 0.3)
        system_config.amusement_threshold = humor.get("amusement_threshold", 0.6)
        
        # Reflection and iteration
        reflection = config_data.get("reflection_and_iteration", {})
        system_config.enable_reflection = reflection.get("enable_reflection", True)
        system_config.reflection_iterations = reflection.get("reflection_iterations", 2)
        system_config.enable_self_critique = reflection.get("enable_self_critique", True)
        
        # External APIs
        apis = config_data.get("external_apis", {})
        system_config.enable_external_validation = apis.get("enable_external_validation", False)
        system_config.use_philpapers_api = apis.get("use_philpapers_api", False)
        system_config.api_timeout = apis.get("api_timeout", 10.0)
        system_config.max_retries = apis.get("max_retries", 3)
        
        # Generation parameters
        gen_params = config_data.get("generation_parameters", {})
        system_config.philosophical_temperature = gen_params.get("philosophical_temperature", 0.8)
        system_config.creativity_boost = gen_params.get("creativity_boost", 0.2)
        system_config.coherence_weight = gen_params.get("coherence_weight", 0.7)
        system_config.novelty_preference = gen_params.get("novelty_preference", 0.6)
        
        # Output formatting
        output = config_data.get("output_formatting", {})
        system_config.include_metadata = output.get("include_metadata", True)
        system_config.show_reasoning_process = output.get("show_reasoning_process", True)
        
        # Evaluation metrics
        eval_metrics = config_data.get("evaluation_metrics", {})
        system_config.track_originality = eval_metrics.get("track_originality", True)
        
        # Safety and ethics
        safety = config_data.get("safety_and_ethics", {})
        system_config.avoid_harmful_conclusions = safety.get("avoid_harmful_conclusions", True)
        system_config.maintain_intellectual_humility = safety.get("maintain_intellectual_humility", True)
        
        # Handle direct overrides (for backwards compatibility)
        for key, value in config_data.items():
            if hasattr(system_config, key):
                setattr(system_config, key, value)
        
        return system_config
    
    def _system_config_to_dict(self, config: PhilosophicalSystemConfig) -> Dict[str, Any]:
        """Convert PhilosophicalSystemConfig to dictionary"""
        return {
            "enable_philosophy": config.enable_philosophy,
            "philosophy_integration_mode": config.philosophy_integration_mode,
            "inner_monologue_depth": config.inner_monologue_depth,
            "enable_structured_reflection": config.enable_structured_reflection,
            "enable_nihiltheism": config.enable_nihiltheism,
            "nihiltheism_weight": config.nihiltheism_weight,
            "enable_terminology_generation": config.enable_terminology_generation,
            "enable_thought_experiments": config.enable_thought_experiments,
            "enable_humor": config.enable_humor,
            "humor_factor": config.humor_factor,
            "amusement_threshold": config.amusement_threshold,
            "enable_reflection": config.enable_reflection,
            "reflection_iterations": config.reflection_iterations,
            "enable_self_critique": config.enable_self_critique,
            "enable_external_validation": config.enable_external_validation,
            "use_philpapers_api": config.use_philpapers_api,
            "api_timeout": config.api_timeout,
            "max_retries": config.max_retries,
            "philosophical_temperature": config.philosophical_temperature,
            "creativity_boost": config.creativity_boost,
            "coherence_weight": config.coherence_weight,
            "novelty_preference": config.novelty_preference,
            "include_metadata": config.include_metadata,
            "show_reasoning_process": config.show_reasoning_process,
            "track_originality": config.track_originality,
            "avoid_harmful_conclusions": config.avoid_harmful_conclusions,
            "maintain_intellectual_humility": config.maintain_intellectual_humility
        }
    
    def validate_config(self, config: PhilosophicalSystemConfig) -> Dict[str, Any]:
        """Validate configuration and return validation report"""
        warnings = []
        errors = []
        
        # Check required parameters
        if not isinstance(config.enable_philosophy, bool):
            errors.append("enable_philosophy must be boolean")
        
        if config.inner_monologue_depth < 0 or config.inner_monologue_depth > 10:
            warnings.append("inner_monologue_depth should be between 0-10")
        
        if config.reflection_iterations < 0 or config.reflection_iterations > 5:
            warnings.append("reflection_iterations should be between 0-5")
        
        if not (0.0 <= config.nihiltheism_weight <= 1.0):
            errors.append("nihiltheism_weight must be between 0.0 and 1.0")
        
        if not (0.0 <= config.humor_factor <= 1.0):
            errors.append("humor_factor must be between 0.0 and 1.0")
        
        if config.philosophical_temperature <= 0:
            errors.append("philosophical_temperature must be positive")
        
        if config.api_timeout <= 0:
            warnings.append("api_timeout should be positive")
        
        # Check mode compatibility
        if config.philosophy_integration_mode not in ["off", "partial", "full"]:
            errors.append("philosophy_integration_mode must be 'off', 'partial', or 'full'")
        
        if config.philosophy_integration_mode == "off" and config.enable_philosophy:
            warnings.append("enable_philosophy=True with mode='off' is contradictory")
        
        # Performance warnings
        if (config.inner_monologue_depth > 5 and 
            config.reflection_iterations > 3 and 
            config.enable_terminology_generation and 
            config.enable_thought_experiments):
            warnings.append("High computational load configuration - consider reducing parameters")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "config_summary": {
                "philosophy_enabled": config.enable_philosophy,
                "integration_mode": config.philosophy_integration_mode,
                "computational_complexity": self._estimate_complexity(config)
            }
        }
    
    def _estimate_complexity(self, config: PhilosophicalSystemConfig) -> str:
        """Estimate computational complexity of configuration"""
        complexity_score = 0
        
        if config.enable_philosophy:
            complexity_score += config.inner_monologue_depth * 2
            complexity_score += config.reflection_iterations * 3
            
            if config.enable_terminology_generation:
                complexity_score += 5
            if config.enable_thought_experiments:
                complexity_score += 4
            if config.enable_external_validation:
                complexity_score += 6
        
        if complexity_score <= 10:
            return "low"
        elif complexity_score <= 25:
            return "medium"
        else:
            return "high"
    
    def save_config(self, config: PhilosophicalSystemConfig, filename: str):
        """Save configuration to file"""
        config_dict = {
            "philosophical_system_config": self._system_config_to_dict(config),
            "metadata": {
                "created_by": "ConfigurationLoader",
                "config_version": "1.0.0",
                "validation_report": self.validate_config(config)
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(config_dict, f, indent=2)
    
    def get_available_presets(self) -> Dict[str, str]:
        """Get list of available preset configurations with descriptions"""
        preset_descriptions = {
            "minimalist": "Basic philosophical capabilities with minimal overhead",
            "standard": "Balanced approach suitable for most applications", 
            "comprehensive": "Full philosophical reasoning with all features enabled",
            "research": "Academic-focused configuration with validation and citations"
        }
        
        available = {}
        for preset_name in self.presets.keys():
            description = preset_descriptions.get(preset_name, "Custom preset configuration")
            available[preset_name] = description
        
        return available

# Convenience functions
def load_philosophical_config(preset: str = "standard", 
                            config_file: str = None,
                            overrides: Dict[str, Any] = None) -> PhilosophicalSystemConfig:
    """
    Convenient function to load philosophical configuration
    
    Args:
        preset: Name of preset configuration to load
        config_file: Path to custom configuration file (overrides preset)
        overrides: Dictionary of specific parameters to override
    
    Returns:
        PhilosophicalSystemConfig: Loaded configuration
    """
    loader = ConfigurationLoader()
    
    if config_file:
        config = loader.load_custom_config(config_file)
    else:
        config = loader.load_preset(preset)
    
    if overrides:
        config_dict = loader._system_config_to_dict(config)
        config_dict.update(overrides)
        config = loader._create_system_config(config_dict)
    
    return config

def validate_philosophical_config(config: PhilosophicalSystemConfig) -> bool:
    """
    Validate philosophical configuration
    
    Args:
        config: Configuration to validate
        
    Returns:
        bool: True if configuration is valid
    """
    loader = ConfigurationLoader()
    validation_result = loader.validate_config(config)
    
    if validation_result["warnings"]:
        print("Configuration warnings:")
        for warning in validation_result["warnings"]:
            print(f"  - {warning}")
    
    if validation_result["errors"]:
        print("Configuration errors:")
        for error in validation_result["errors"]:
            print(f"  - {error}")
    
    return validation_result["valid"]

def get_preset_configurations() -> Dict[str, str]:
    """Get available preset configurations with descriptions"""
    loader = ConfigurationLoader()
    return loader.get_available_presets()

# Example usage
if __name__ == "__main__":
    # Demonstrate configuration loading
    print("Philosophical AI Configuration Loader Demo")
    print("=" * 50)
    
    # Show available presets
    print("Available presets:")
    presets = get_preset_configurations()
    for name, description in presets.items():
        print(f"  {name}: {description}")
    
    # Load standard preset
    print("\nLoading standard preset...")
    config = load_philosophical_config(preset="standard")
    print(f"Philosophy enabled: {config.enable_philosophy}")
    print(f"Inner monologue depth: {config.inner_monologue_depth}")
    print(f"Nihiltheism weight: {config.nihiltheism_weight}")
    
    # Load with overrides
    print("\nLoading with custom overrides...")
    custom_config = load_philosophical_config(
        preset="standard",
        overrides={
            "humor_factor": 0.8,
            "inner_monologue_depth": 5,
            "enable_external_validation": False
        }
    )
    print(f"Humor factor: {custom_config.humor_factor}")
    print(f"Inner monologue depth: {custom_config.inner_monologue_depth}")
    
    # Validate configuration
    print("\nValidating configuration...")
    is_valid = validate_philosophical_config(custom_config)
    print(f"Configuration valid: {is_valid}")
    
    # Convert to core config
    print("\nConverting to core philosophical config...")
    core_config = custom_config.to_philosophical_config()
    print(f"Core config created: {type(core_config).__name__}")
    
    print("\nConfiguration demo completed!")
