#!/usr/bin/env python3
"""
Test script for image transformation tool
Creates a test image and applies all transformations
"""

from PIL import Image, ImageDraw
import subprocess
import sys
from pathlib import Path


def create_test_image(path, size=(400, 400)):
    """Create a test image with gradients and shapes."""
    img = Image.new('L', size, 255)
    draw = ImageDraw.Draw(img)

    # Create gradient background
    for y in range(size[1]):
        brightness = int((y / size[1]) * 255)
        draw.rectangle([0, y, size[0], y + 1], fill=brightness)

    # Add some shapes
    draw.ellipse([50, 50, 150, 150], fill=50)
    draw.rectangle([200, 50, 300, 150], fill=100)
    draw.ellipse([50, 200, 150, 300], fill=150)
    draw.rectangle([200, 200, 300, 300], fill=200)

    # Add text
    draw.text((150, 350), "TEST", fill=0)

    img.save(path)
    print(f"Created test image: {path}")


def run_test(test_name, mode, args=[]):
    """Run transformation test."""
    output = f"test_output_{test_name}.png"
    cmd = [
        sys.executable,
        "imgtransform.py",
        "-i", "test_input.png",
        "-o", output,
        f"--{mode}"
    ] + args

    print(f"\nTesting {test_name}...")
    print(f"Command: {' '.join(cmd)}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✓ {test_name} test passed")
        return True
    else:
        print(f"✗ {test_name} test failed")
        print(f"Error: {result.stderr}")
        return False


def main():
    print("Image Transform Tool - Test Suite")
    print("=" * 50)

    # Create output directory
    Path("test_output").mkdir(exist_ok=True)

    # Create test image
    print("\n1. Creating test image...")
    create_test_image("test_input.png")

    # Run tests
    print("\n2. Running transformation tests...")
    tests_passed = 0
    tests_total = 0

    tests = [
        ("halftone", "halftone", []),
        ("halftone_large", "halftone", ["--dot-size", "12"]),
        ("dither", "dither", []),
        ("posterize", "posterize", []),
        ("posterize_dark", "posterize", ["--threshold", "180"]),
    ]

    for test_name, mode, args in tests:
        tests_total += 1
        if run_test(test_name, mode, args):
            tests_passed += 1

    # Summary
    print("\n" + "=" * 50)
    print(f"Tests passed: {tests_passed}/{tests_total}")

    if tests_passed == tests_total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
