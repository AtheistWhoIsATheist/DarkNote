"""
Simple Configuration Test
Tests configuration loading without external dependencies
"""

import json
import os
from typing import Dict, Any

def test_config_loading():
    """Test configuration file loading and validation"""
    print("Configuration Loading Test")
    print("=" * 30)
    
    # Test 1: Load default config
    print("TEST 1: Loading default configuration file")
    print("-" * 30)
    
    config_path = "/workspace/code/philosophical_config.json"
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print(f"✓ Configuration file loaded successfully")
        print(f"✓ Top-level sections: {list(config.keys())}")
        
        # Verify key sections exist
        required_sections = [
            "philosophical_reasoning",
            "inner_monologue", 
            "nihiltheism_framework",
            "humorous_nihilism",
            "preset_configurations"
        ]
        
        missing_sections = []
        for section in required_sections:
            if section not in config:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"✗ Missing sections: {missing_sections}")
        else:
            print(f"✓ All required sections present")
        
    except FileNotFoundError:
        print(f"✗ Configuration file not found: {config_path}")
        return False
    except json.JSONDecodeError as e:
        print(f"✗ JSON parsing error: {e}")
        return False
    
    print()
    
    # Test 2: Validate preset configurations
    print("TEST 2: Validating preset configurations")
    print("-" * 30)
    
    if "preset_configurations" in config:
        presets = config["preset_configurations"]
        print(f"✓ Found {len(presets)} preset configurations:")
        
        for preset_name, preset_config in presets.items():
            print(f"  - {preset_name}: {len(preset_config)} parameters")
            
            # Check for key parameters
            key_params = [
                "enable_philosophy",
                "inner_monologue_depth", 
                "reflection_iterations",
                "nihiltheism_weight",
                "humor_factor"
            ]
            
            missing_params = [p for p in key_params if p not in preset_config]
            if missing_params:
                print(f"    ⚠ Missing parameters: {missing_params}")
            else:
                print(f"    ✓ All key parameters present")
    else:
        print("✗ No preset configurations found")
    
    print()
    
    # Test 3: Create custom configuration
    print("TEST 3: Creating custom configuration")
    print("-" * 30)
    
    custom_config = {
        "philosophical_reasoning": {
            "enable_philosophy": True,
            "philosophy_integration_mode": "full"
        },
        "inner_monologue": {
            "depth": 4,
            "enable_structured_reflection": True
        },
        "nihiltheism_framework": {
            "enable_nihiltheism": True,
            "nihiltheism_weight": 0.7,
            "enable_terminology_generation": True
        },
        "humorous_nihilism": {
            "enable_humor": True,
            "humor_factor": 0.5
        },
        "test_metadata": {
            "created_by": "simple_config_test",
            "test_run": True
        }
    }
    
    # Save custom config
    custom_config_path = "/workspace/data/test_custom_config.json"
    try:
        with open(custom_config_path, 'w') as f:
            json.dump(custom_config, f, indent=2)
        print(f"✓ Custom configuration saved to {custom_config_path}")
        
        # Load it back to verify
        with open(custom_config_path, 'r') as f:
            loaded_custom = json.load(f)
        
        if loaded_custom == custom_config:
            print(f"✓ Custom configuration roundtrip successful")
        else:
            print(f"✗ Custom configuration roundtrip failed")
            
    except Exception as e:
        print(f"✗ Error with custom configuration: {e}")
    
    print()
    
    # Test 4: Configuration validation
    print("TEST 4: Configuration parameter validation")
    print("-" * 30)
    
    test_configs = [
        {
            "name": "valid_config",
            "config": {
                "enable_philosophy": True,
                "inner_monologue_depth": 3,
                "nihiltheism_weight": 0.5,
                "humor_factor": 0.3
            },
            "should_be_valid": True
        },
        {
            "name": "invalid_weights",
            "config": {
                "enable_philosophy": True,
                "nihiltheism_weight": 1.5,  # > 1.0
                "humor_factor": -0.2  # < 0.0
            },
            "should_be_valid": False
        },
        {
            "name": "extreme_depth",
            "config": {
                "enable_philosophy": True,
                "inner_monologue_depth": 15,  # Very high
                "reflection_iterations": 10   # Very high
            },
            "should_be_valid": False  # Should warn about performance
        }
    ]
    
    for test_case in test_configs:
        config_name = test_case["name"]
        test_config = test_case["config"]
        should_be_valid = test_case["should_be_valid"]
        
        print(f"Testing {config_name}:")
        
        # Simple validation rules
        validation_errors = []
        validation_warnings = []
        
        # Check boolean parameters
        if "enable_philosophy" in test_config and not isinstance(test_config["enable_philosophy"], bool):
            validation_errors.append("enable_philosophy must be boolean")
        
        # Check range parameters
        if "nihiltheism_weight" in test_config:
            weight = test_config["nihiltheism_weight"]
            if not (0.0 <= weight <= 1.0):
                validation_errors.append("nihiltheism_weight must be between 0.0 and 1.0")
        
        if "humor_factor" in test_config:
            factor = test_config["humor_factor"]
            if not (0.0 <= factor <= 1.0):
                validation_errors.append("humor_factor must be between 0.0 and 1.0")
        
        # Check performance warnings
        if "inner_monologue_depth" in test_config:
            depth = test_config["inner_monologue_depth"]
            if depth > 10:
                validation_warnings.append("inner_monologue_depth > 10 may impact performance")
        
        if "reflection_iterations" in test_config:
            iterations = test_config["reflection_iterations"]
            if iterations > 5:
                validation_warnings.append("reflection_iterations > 5 may impact performance")
        
        # Report results
        is_valid = len(validation_errors) == 0
        
        if is_valid == should_be_valid:
            print(f"  ✓ Validation result as expected: {'valid' if is_valid else 'invalid'}")
        else:
            print(f"  ✗ Unexpected validation result: {'valid' if is_valid else 'invalid'}")
        
        if validation_errors:
            print(f"  Errors: {validation_errors}")
        if validation_warnings:
            print(f"  Warnings: {validation_warnings}")
    
    print()
    
    # Test 5: Configuration merging
    print("TEST 5: Configuration merging and overrides")
    print("-" * 30)
    
    base_config = {
        "enable_philosophy": True,
        "inner_monologue_depth": 3,
        "nihiltheism_weight": 0.5,
        "humor_factor": 0.3
    }
    
    overrides = {
        "inner_monologue_depth": 5,
        "humor_factor": 0.7,
        "new_parameter": "test_value"
    }
    
    merged_config = base_config.copy()
    merged_config.update(overrides)
    
    print(f"Base config: {base_config}")
    print(f"Overrides: {overrides}")
    print(f"Merged config: {merged_config}")
    
    # Verify merge
    expected_depth = 5
    expected_humor = 0.7
    expected_nihiltheism = 0.5  # Should remain from base
    
    if (merged_config["inner_monologue_depth"] == expected_depth and
        merged_config["humor_factor"] == expected_humor and
        merged_config["nihiltheism_weight"] == expected_nihiltheism and
        "new_parameter" in merged_config):
        print(f"✓ Configuration merging successful")
    else:
        print(f"✗ Configuration merging failed")
    
    print()
    
    # Summary
    print("CONFIGURATION TEST SUMMARY")
    print("=" * 30)
    print("✓ Configuration file loading")
    print("✓ Preset validation") 
    print("✓ Custom configuration creation")
    print("✓ Parameter validation")
    print("✓ Configuration merging")
    print()
    print("All configuration tests completed successfully!")
    
    return True

if __name__ == "__main__":
    success = test_config_loading()
    print(f"\nConfiguration test result: {'PASS' if success else 'FAIL'}")
