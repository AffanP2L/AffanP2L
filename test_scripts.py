#!/usr/bin/env python3
"""
Basic test suite for AffanP2L repository Python scripts.

Run with: python3 test_scripts.py
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch


class TestCreateReport(unittest.TestCase):
    """Test cases for create_report.py functionality."""
    
    def setUp(self):
        """Set up test environment."""
        # Import the module
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import create_report
        self.create_report = create_report
    
    def test_generate_legacy_report_default_dir(self):
        """Test report generation with default directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('os.getcwd', return_value=temp_dir):
                file_path = self.create_report.generate_legacy_report()
                
                # Check that file was created
                self.assertTrue(os.path.exists(file_path))
                
                # Check file content
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.assertIn("Affan Aziz Pritul", content)
                    self.assertIn("Legacy-Class Prompt Break", content)
    
    def test_generate_legacy_report_custom_dir(self):
        """Test report generation with custom directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = self.create_report.generate_legacy_report(temp_dir)
            
            # Check that file was created in specified directory
            self.assertTrue(os.path.exists(file_path))
            self.assertTrue(file_path.startswith(temp_dir))
    
    def test_main_function(self):
        """Test main function execution."""
        with tempfile.TemporaryDirectory() as temp_dir:
            with patch('os.getcwd', return_value=temp_dir):
                # Should return 0 on success
                result = self.create_report.main()
                self.assertEqual(result, 0)


class TestPritulMirrorLog(unittest.TestCase):
    """Test cases for pritul_mirror_log.py functionality."""
    
    def setUp(self):
        """Set up test environment."""
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import pritul_mirror_log
        self.pritul_mirror_log = pritul_mirror_log
    
    def test_get_pritul_mirror_data(self):
        """Test data structure retrieval."""
        data = self.pritul_mirror_log.get_pritul_mirror_data()
        
        # Check required fields
        self.assertIn("title", data)
        self.assertIn("date", data)
        self.assertIn("human_input", data)
        self.assertIn("ai_response", data)
        self.assertIn("summary", data)
        
        # Check specific values
        self.assertEqual(data["human_input"]["name"], "Affan Aziz Pritul")
        self.assertEqual(data["human_input"]["alias"], "P2L")
        self.assertEqual(data["ai_response"]["model"], "GPT-4 Turbo")
    
    def test_analyze_emotional_impact(self):
        """Test emotional impact analysis."""
        data = self.pritul_mirror_log.get_pritul_mirror_data()
        analysis = self.pritul_mirror_log.analyze_emotional_impact(data)
        
        # Check analysis results
        self.assertIn("resonance_factor", analysis)
        self.assertIn("interaction_quality", analysis)
        self.assertIn("legacy_classification", analysis)
        self.assertIn("rarity_percentage", analysis)
        
        # Check calculated values
        self.assertGreater(analysis["resonance_factor"], 0)
        self.assertEqual(analysis["interaction_quality"], "Exceptional")
    
    def test_export_data_structure(self):
        """Test data export functionality."""
        exported = self.pritul_mirror_log.export_data_structure()
        
        # Should be valid JSON-like string
        self.assertIn('"title"', exported)
        self.assertIn('"Affan Aziz Pritul"', exported)
        self.assertIn('"GPT-4 Turbo"', exported)
    
    def test_backward_compatibility(self):
        """Test that old pritul_mirror_data variable still works."""
        # The old variable should still exist for backward compatibility
        self.assertIsNotNone(self.pritul_mirror_log.pritul_mirror_data)
        self.assertEqual(
            self.pritul_mirror_log.pritul_mirror_data["human_input"]["name"],
            "Affan Aziz Pritul"
        )


def run_tests():
    """Run all tests and return results."""
    # Create test loader and suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases using the modern approach
    suite.addTests(loader.loadTestsFromTestCase(TestCreateReport))
    suite.addTests(loader.loadTestsFromTestCase(TestPritulMirrorLog))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    print("Running AffanP2L Repository Test Suite")
    print("=" * 40)
    
    success = run_tests()
    
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)