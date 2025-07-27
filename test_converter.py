#!/usr/bin/env python3
"""
Test script for the Mind Map Converter Agent

This script tests the converter with the provided example files
and generates sample outputs in all supported formats.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path so we can import the converter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from mind_map_converter import MindMapConverter, OutputFormat
    print("✓ Successfully imported mind_map_converter")
except ImportError as e:
    print(f"✗ Failed to import mind_map_converter: {e}")
    print("Make sure all dependencies are installed: pip install -r requirements.txt")
    sys.exit(1)


def test_conversion(input_file, output_base_name):
    """Test conversion of a mind map file to all supported formats."""
    print(f"\n🧪 Testing conversion of {input_file}")
    
    if not os.path.exists(input_file):
        print(f"✗ Input file not found: {input_file}")
        return False
    
    converter = MindMapConverter()
    success_count = 0
    total_formats = len(OutputFormat)
    
    for output_format in OutputFormat:
        try:
            output_file = f"test_outputs/{output_base_name}.{output_format.value}"
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            converter.convert(input_file, output_file, output_format)
            print(f"  ✓ {output_format.value.upper()}: {output_file}")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ {output_format.value.upper()}: {e}")
    
    print(f"  📊 Success: {success_count}/{total_formats} formats")
    return success_count == total_formats


def main():
    """Run all tests."""
    print("🚀 Starting Mind Map Converter Tests")
    print("=" * 50)
    
    # Test files
    test_files = [
        ("examples/sample_mindmap.json", "ai_overview"),
        ("examples/sample_mindmap.xml", "project_management"),
        ("examples/sample_mindmap.txt", "web_development")
    ]
    
    total_tests = len(test_files)
    passed_tests = 0
    
    for input_file, output_base in test_files:
        if test_conversion(input_file, output_base):
            passed_tests += 1
    
    print("\n" + "=" * 50)
    print(f"📈 Test Results: {passed_tests}/{total_tests} test files passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! The converter is working correctly.")
        print("\n📁 Check the 'test_outputs/' directory for generated files:")
        
        # List generated files
        output_dir = Path("test_outputs")
        if output_dir.exists():
            for file_path in sorted(output_dir.iterdir()):
                if file_path.is_file():
                    size = file_path.stat().st_size
                    print(f"   📄 {file_path.name} ({size} bytes)")
    else:
        print("❌ Some tests failed. Check the error messages above.")
        sys.exit(1)


if __name__ == "__main__":
    main()