"""
Integration Test Suite for Philosophical AI System
Tests the integration between language model and philosophical reasoning components
"""

import unittest
import sys
import os
import json
import tempfile
from unittest.mock import Mock, patch
import torch
import torch.nn as nn

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from ai_philosopher_core import (
    PhilosophicalConfig,
    PhilosophicalInquiryGenerator,
    AIPhilosopherCore,
    create_philosopher_config
)
from nihiltheism_framework import (
    NihiltheismFramework,
    HumorousNihilismEngine,
    ThoughtExperimentGenerator,
    NihiltheismTerminologyGenerator
)

class MockGPTModel(nn.Module):
    """Mock GPT model for testing"""
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.embed_dim = getattr(config, 'n_embd', 384)
        self.linear = nn.Linear(self.embed_dim, self.embed_dim)
    
    def forward(self, x):
        return self.linear(x), None
    
    def generate(self, idx, max_new_tokens, **kwargs):
        # Mock generation - just return extended input
        batch_size, seq_len = idx.shape
        new_tokens = torch.randint(0, 1000, (batch_size, max_new_tokens))
        return torch.cat([idx, new_tokens], dim=1)

class TestPhilosophicalConfig(unittest.TestCase):
    """Test philosophical configuration"""
    
    def test_default_config_creation(self):
        """Test default configuration creation"""
        config = create_philosopher_config()
        
        self.assertTrue(config.enable_philosophy)
        self.assertEqual(config.inner_monologue_depth, 3)
        self.assertEqual(config.reflection_iterations, 2)
        self.assertEqual(config.nihiltheism_weight, 0.5)
        self.assertEqual(config.humor_factor, 0.3)
    
    def test_custom_config_creation(self):
        """Test custom configuration creation"""
        config = create_philosopher_config(
            enable_philosophy=False,
            inner_monologue_depth=5,
            reflection_iterations=3,
            nihiltheism_weight=0.8,
            humor_factor=0.6
        )
        
        self.assertFalse(config.enable_philosophy)
        self.assertEqual(config.inner_monologue_depth, 5)
        self.assertEqual(config.reflection_iterations, 3)
        self.assertEqual(config.nihiltheism_weight, 0.8)
        self.assertEqual(config.humor_factor, 0.6)

class TestPhilosophicalInquiryGenerator(unittest.TestCase):
    """Test philosophical inquiry generation"""
    
    def setUp(self):
        self.config = create_philosopher_config()
        self.generator = PhilosophicalInquiryGenerator(self.config)
    
    def test_inner_monologue_generation(self):
        """Test inner monologue generation"""
        context = "Test context"
        inquiry = "Test inquiry"
        
        monologue = self.generator.generate_inner_monologue(context, inquiry)
        
        self.assertIsInstance(monologue, str)
        self.assertIn("INNER MONOLOGUE", monologue)
        self.assertIn(context, monologue)
        self.assertIn(inquiry, monologue)
    
    def test_nihiltheistic_synthesis(self):
        """Test Nihiltheistic synthesis generation"""
        nihilistic_premise = "Test nihilistic premise"
        theistic_element = "Test theistic element"
        synthesis_target = "Test synthesis target"
        
        synthesis = self.generator.generate_nihiltheistic_synthesis(
            nihilistic_premise, theistic_element, synthesis_target
        )
        
        self.assertIsInstance(synthesis, str)
        self.assertIn("Nihiltheistic Synthesis", synthesis)
        self.assertIn(nihilistic_premise, synthesis)
        self.assertIn(theistic_element, synthesis)
        self.assertIn(synthesis_target, synthesis)
    
    def test_humorous_nihilism_application(self):
        """Test humorous nihilism application"""
        incongruity = "Test incongruity"
        traditional_response = "Test traditional response"
        
        humor_result = self.generator.apply_humorous_nihilism(
            incongruity, traditional_response
        )
        
        self.assertIsInstance(humor_result, str)
        self.assertIn("Humorous Nihilism", humor_result)
        self.assertIn(incongruity, humor_result)
        self.assertIn(traditional_response, humor_result)
    
    def test_complete_philosophical_inquiry(self):
        """Test complete philosophical inquiry processing"""
        base_prompt = "What is the meaning of existence?"
        context = "Existential philosophy"
        
        result = self.generator.process_philosophical_inquiry(base_prompt, context)
        
        self.assertIsInstance(result, dict)
        self.assertIn("base_prompt", result)
        self.assertIn("inner_monologue", result)
        self.assertIn("nihiltheistic_synthesis", result)
        self.assertIn("humorous_perspective", result)
        self.assertIn("originality_score", result)
        self.assertIn("timestamp", result)
        
        self.assertEqual(result["base_prompt"], base_prompt)
        self.assertIsInstance(result["originality_score"], float)
        self.assertGreaterEqual(result["originality_score"], 0.0)
        self.assertLessEqual(result["originality_score"], 1.0)

class TestNihiltheismFramework(unittest.TestCase):
    """Test Nihiltheism framework components"""
    
    def setUp(self):
        self.framework = NihiltheismFramework()
    
    def test_terminology_generation(self):
        """Test novel terminology generation"""
        concept_focus = "test_concept"
        num_terms = 3
        
        terms = self.framework.terminology_generator.create_novel_terminology(
            concept_focus, num_terms
        )
        
        self.assertEqual(len(terms), num_terms)
        for term in terms:
            self.assertIsInstance(term.term, str)
            self.assertIsInstance(term.definition, str)
            self.assertIsInstance(term.etymology, list)
            self.assertIsInstance(term.usage_example, str)
            self.assertIsInstance(term.originality_score, float)
            self.assertGreaterEqual(term.originality_score, 0.0)
            self.assertLessEqual(term.originality_score, 1.0)
    
    def test_humor_engine(self):
        """Test humorous nihilism engine"""
        incongruity = "Test philosophical incongruity"
        traditional_responses = ["despair", "resolution"]
        
        humor_analysis = self.framework.humor_engine.apply_humor_to_incongruity(
            incongruity, traditional_responses
        )
        
        self.assertIsInstance(humor_analysis, dict)
        self.assertIn("original_incongruity", humor_analysis)
        self.assertIn("traditional_responses", humor_analysis)
        self.assertIn("humor_techniques_applied", humor_analysis)
        self.assertIn("amusing_perspectives", humor_analysis)
        self.assertIn("comedic_insights", humor_analysis)
        self.assertIn("final_humorous_synthesis", humor_analysis)
        
        self.assertEqual(humor_analysis["original_incongruity"], incongruity)
        self.assertEqual(humor_analysis["traditional_responses"], traditional_responses)
    
    def test_thought_experiment_generation(self):
        """Test thought experiment generation"""
        template = "AI_consciousness_meaninglessness"
        
        experiment = self.framework.experiment_generator.generate_nihiltheistic_experiment(
            template
        )
        
        self.assertIsInstance(experiment.title, str)
        self.assertIsInstance(experiment.scenario, str)
        self.assertIsInstance(experiment.key_questions, list)
        self.assertIsInstance(experiment.nihilistic_perspective, str)
        self.assertIsInstance(experiment.theistic_perspective, str)
        self.assertIsInstance(experiment.synthesis_opportunity, str)
        self.assertIsInstance(experiment.expected_insights, list)
        self.assertIsInstance(experiment.humor_potential, str)
    
    def test_concept_development(self):
        """Test complete concept development"""
        concept_name = "test_concept"
        philosophical_problem = "test problem"
        
        result = self.framework.develop_nihiltheistic_concept(
            concept_name, philosophical_problem
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("concept_name", result)
        self.assertIn("philosophical_problem", result)
        self.assertIn("components", result)
        self.assertIn("nihiltheistic_synthesis", result)
        self.assertIn("timestamp", result)
        
        self.assertEqual(result["concept_name"], concept_name)
        self.assertEqual(result["philosophical_problem"], philosophical_problem)
    
    def test_framework_export(self):
        """Test framework development export"""
        # Develop a concept first
        self.framework.develop_nihiltheistic_concept(
            "test_concept", "test problem"
        )
        
        # Test export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_filename = f.name
        
        try:
            self.framework.export_framework_development(temp_filename)
            
            # Verify file was created and contains expected data
            self.assertTrue(os.path.exists(temp_filename))
            
            with open(temp_filename, 'r') as f:
                exported_data = json.load(f)
            
            self.assertIn("framework_name", exported_data)
            self.assertIn("development_history", exported_data)
            self.assertIn("total_concepts_developed", exported_data)
            self.assertEqual(exported_data["framework_name"], "Nihiltheism")
            self.assertEqual(exported_data["total_concepts_developed"], 1)
            
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)

class TestAIPhilosopherCore(unittest.TestCase):
    """Test AI Philosopher core integration"""
    
    def setUp(self):
        self.config = create_philosopher_config()
        
        # Create mock model config
        model_config = Mock()
        model_config.n_embd = 384
        
        self.mock_model = MockGPTModel(model_config)
        self.philosopher = AIPhilosopherCore(self.mock_model, self.config)
    
    def test_philosopher_initialization(self):
        """Test philosopher core initialization"""
        self.assertIsNotNone(self.philosopher.model)
        self.assertIsNotNone(self.philosopher.inquiry_generator)
        self.assertTrue(self.philosopher.philosophy_enabled)
    
    def test_prompt_enhancement(self):
        """Test prompt enhancement with philosophy"""
        base_prompt = "What is consciousness?"
        
        enhanced = self.philosopher.enhance_prompt_with_philosophy(
            base_prompt, enable_inner_monologue=True, enable_nihiltheism=True
        )
        
        self.assertIsInstance(enhanced, str)
        self.assertIn(base_prompt, enhanced)
        self.assertIn("PHILOSOPHICAL REFLECTION", enhanced)
        self.assertIn("NIHILTHEISTIC SYNTHESIS", enhanced)
    
    def test_philosophical_response_generation(self):
        """Test philosophical response generation"""
        prompt = "What is the meaning of life?"
        
        response = self.philosopher.generate_philosophical_response(
            prompt, max_new_tokens=100, enable_reflection=False
        )
        
        self.assertIsInstance(response, dict)
        self.assertIn("original_prompt", response)
        self.assertIn("enhanced_prompt", response)
        self.assertIn("philosophical_analysis", response)
        self.assertIn("generation_params", response)
        
        self.assertEqual(response["original_prompt"], prompt)
    
    def test_disabled_philosophy(self):
        """Test behavior when philosophy is disabled"""
        disabled_config = create_philosopher_config(enable_philosophy=False)
        disabled_philosopher = AIPhilosopherCore(self.mock_model, disabled_config)
        
        base_prompt = "Test prompt"
        enhanced = disabled_philosopher.enhance_prompt_with_philosophy(base_prompt)
        
        self.assertEqual(enhanced, base_prompt)  # Should be unchanged
        
        response = disabled_philosopher.generate_philosophical_response("test")
        self.assertIn("error", response)

class TestIntegrationScenarios(unittest.TestCase):
    """Test integration scenarios between components"""
    
    def setUp(self):
        self.config = create_philosopher_config()
        model_config = Mock()
        model_config.n_embd = 384
        self.mock_model = MockGPTModel(model_config)
        self.philosopher = AIPhilosopherCore(self.mock_model, self.config)
        self.framework = NihiltheismFramework()
    
    def test_end_to_end_philosophical_analysis(self):
        """Test complete end-to-end philosophical analysis"""
        prompt = "How does artificial intelligence challenge human understanding of consciousness?"
        
        # Generate philosophical response
        phil_response = self.philosopher.generate_philosophical_response(
            prompt, enable_reflection=False
        )
        
        # Develop Nihiltheistic concept
        nihil_analysis = self.framework.develop_nihiltheistic_concept(
            "AI_consciousness_challenge",
            prompt
        )
        
        # Verify both components work together
        self.assertIsInstance(phil_response, dict)
        self.assertIsInstance(nihil_analysis, dict)
        
        self.assertIn("philosophical_analysis", phil_response)
        self.assertIn("nihiltheistic_synthesis", nihil_analysis)
    
    def test_terminology_integration(self):
        """Test integration of terminology generation with inquiry processing"""
        # Generate terminology
        terms = self.framework.terminology_generator.create_novel_terminology(
            "consciousness_AI", 2
        )
        
        # Use generated terms in philosophical inquiry
        term_names = [term.term for term in terms]
        inquiry_text = f"How do the concepts {', '.join(term_names)} relate to consciousness?"
        
        inquiry_result = self.philosopher.inquiry_generator.process_philosophical_inquiry(
            inquiry_text, "AI consciousness with novel terminology"
        )
        
        self.assertIsInstance(inquiry_result, dict)
        self.assertIn("base_prompt", inquiry_result)
        # Terms should be mentioned in the inquiry
        for term_name in term_names:
            self.assertIn(term_name, inquiry_result["base_prompt"])
    
    def test_humor_and_synthesis_integration(self):
        """Test integration of humor engine with synthesis generation"""
        incongruity = "AI seeks to understand human consciousness while humans debate AI consciousness"
        
        # Apply humor analysis
        humor_result = self.framework.humor_engine.apply_humor_to_incongruity(
            incongruity, ["confusion", "circular reasoning"]
        )
        
        # Generate synthesis incorporating humor
        synthesis = self.philosopher.inquiry_generator.generate_nihiltheistic_synthesis(
            "Consciousness is fundamentally unknowable",
            "Yet we persistently seek understanding",
            f"Exploring: {incongruity}"
        )
        
        self.assertIsInstance(humor_result, dict)
        self.assertIsInstance(synthesis, str)
        self.assertIn("final_humorous_synthesis", humor_result)
        self.assertIn("Nihiltheistic Synthesis", synthesis)

class TestErrorHandling(unittest.TestCase):
    """Test error handling and edge cases"""
    
    def test_empty_input_handling(self):
        """Test handling of empty inputs"""
        config = create_philosopher_config()
        generator = PhilosophicalInquiryGenerator(config)
        
        # Test with empty strings
        monologue = generator.generate_inner_monologue("", "")
        self.assertIsInstance(monologue, str)
        
        synthesis = generator.generate_nihiltheistic_synthesis("", "", "")
        self.assertIsInstance(synthesis, str)
    
    def test_invalid_config_handling(self):
        """Test handling of invalid configurations"""
        # Test with extreme values
        config = PhilosophicalConfig(
            inner_monologue_depth=0,
            reflection_iterations=-1,
            nihiltheism_weight=2.0,  # > 1.0
            humor_factor=-0.5  # < 0.0
        )
        
        generator = PhilosophicalInquiryGenerator(config)
        
        # Should handle gracefully without crashing
        result = generator.process_philosophical_inquiry("test", "test")
        self.assertIsInstance(result, dict)
    
    def test_large_input_handling(self):
        """Test handling of very large inputs"""
        config = create_philosopher_config()
        generator = PhilosophicalInquiryGenerator(config)
        
        # Create very long input
        long_prompt = "test " * 1000
        
        result = generator.process_philosophical_inquiry(long_prompt, "context")
        self.assertIsInstance(result, dict)
        self.assertIn("base_prompt", result)

def run_integration_tests():
    """Run all integration tests"""
    print("Running Philosophical AI Integration Tests")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestPhilosophicalConfig,
        TestPhilosophicalInquiryGenerator,
        TestNihiltheismFramework,
        TestAIPhilosopherCore,
        TestIntegrationScenarios,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 50)
    print("INTEGRATION TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    print(f"\nOverall: {'PASS' if success else 'FAIL'}")
    
    return success, result

if __name__ == "__main__":
    success, test_result = run_integration_tests()
    
    # Save test results
    results_data = {
        "test_run_timestamp": time.time(),
        "tests_run": test_result.testsRun,
        "failures": len(test_result.failures),
        "errors": len(test_result.errors),
        "success_rate": ((test_result.testsRun - len(test_result.failures) - len(test_result.errors)) / test_result.testsRun * 100),
        "overall_success": success
    }
    
    with open("/workspace/data/integration_test_results.json", 'w') as f:
        json.dump(results_data, f, indent=2)
    
    print(f"\nTest results saved to /workspace/data/integration_test_results.json")
    
    sys.exit(0 if success else 1)
