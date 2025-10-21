#!/usr/bin/env python3
"""
Image Transformation Tool
Transforms images into halftone, dithered, or posterized versions.
"""

import argparse
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw


def halftone(image_path, output_path, dot_size=8, scale=1):
    """
    Create halftone dots effect (newsprint/risograph style).

    Args:
        image_path: Input image path
        output_path: Output image path
        dot_size: Size of halftone dots in pixels
        scale: Output scale factor
    """
    # Load and convert to grayscale
    img = Image.open(image_path).convert('L')
    width, height = img.size

    # Create output image
    output_width = width * scale
    output_height = height * scale
    output = Image.new('L', (output_width, output_height), 255)
    draw = ImageDraw.Draw(output)

    # Sample the image at dot intervals
    for y in range(0, height, dot_size):
        for x in range(0, width, dot_size):
            # Get average brightness of the region
            region = img.crop((
                x,
                y,
                min(x + dot_size, width),
                min(y + dot_size, height)
            ))
            avg_brightness = np.array(region).mean()

            # Calculate dot radius based on brightness (darker = larger dot)
            # Invert: 0 (black) -> large dot, 255 (white) -> small/no dot
            dot_radius = ((255 - avg_brightness) / 255) * (dot_size * scale / 2)

            if dot_radius > 0.5:
                # Draw the dot centered in the cell
                center_x = (x + dot_size / 2) * scale
                center_y = (y + dot_size / 2) * scale

                draw.ellipse([
                    center_x - dot_radius,
                    center_y - dot_radius,
                    center_x + dot_radius,
                    center_y + dot_radius
                ], fill=0)

    output.save(output_path)
    print(f"Halftone image saved to {output_path}")


def bayer_dither(image_path, output_path):
    """
    Apply 1-bit dithering using Bayer 8x8 matrix.

    Args:
        image_path: Input image path
        output_path: Output image path
    """
    # Bayer 8x8 threshold matrix (normalized to 0-255)
    bayer_matrix = np.array([
        [ 0, 32,  8, 40,  2, 34, 10, 42],
        [48, 16, 56, 24, 50, 18, 58, 26],
        [12, 44,  4, 36, 14, 46,  6, 38],
        [60, 28, 52, 20, 62, 30, 54, 22],
        [ 3, 35, 11, 43,  1, 33,  9, 41],
        [51, 19, 59, 27, 49, 17, 57, 25],
        [15, 47,  7, 39, 13, 45,  5, 37],
        [63, 31, 55, 23, 61, 29, 53, 21]
    ], dtype=float)

    # Normalize to 0-255 range
    bayer_matrix = (bayer_matrix / 64.0) * 255.0

    # Load and convert to grayscale
    img = Image.open(image_path).convert('L')
    img_array = np.array(img, dtype=float)

    height, width = img_array.shape
    output_array = np.zeros((height, width), dtype=np.uint8)

    # Apply Bayer dithering
    for y in range(height):
        for x in range(width):
            threshold = bayer_matrix[y % 8, x % 8]
            output_array[y, x] = 255 if img_array[y, x] > threshold else 0

    output = Image.fromarray(output_array, mode='L')
    output.save(output_path)
    print(f"Dithered image saved to {output_path}")


def posterize(image_path, output_path, threshold=128):
    """
    Create 2-tone posterized image (stencil/pochoir style).

    Args:
        image_path: Input image path
        output_path: Output image path
        threshold: Threshold value (0-255) for black/white split
    """
    # Load and convert to grayscale
    img = Image.open(image_path).convert('L')
    img_array = np.array(img)

    # Apply threshold to create 2-tone image
    output_array = np.where(img_array > threshold, 255, 0).astype(np.uint8)

    output = Image.fromarray(output_array, mode='L')
    output.save(output_path)
    print(f"Posterized image saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Transform images into halftone, dithered, or posterized versions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -i input.jpg -o output.png --halftone
  %(prog)s -i input.jpg -o output.png --dither
  %(prog)s -i input.jpg -o output.png --posterize
  %(prog)s -i input.jpg -o output.png --halftone --dot-size 10
  %(prog)s -i input.jpg -o output.png --posterize --threshold 140
        """
    )

    parser.add_argument('-i', '--input', required=True, help='Input image path')
    parser.add_argument('-o', '--output', required=True, help='Output image path')

    # Mode selection
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument('--halftone', action='store_true',
                           help='Apply halftone dots effect (newsprint/riso style)')
    mode_group.add_argument('--dither', action='store_true',
                           help='Apply 1-bit Bayer 8×8 dithering')
    mode_group.add_argument('--posterize', action='store_true',
                           help='Apply 2-tone posterization (stencil style)')

    # Mode-specific options
    parser.add_argument('--dot-size', type=int, default=8,
                       help='Dot size for halftone (default: 8)')
    parser.add_argument('--scale', type=int, default=1,
                       help='Output scale factor for halftone (default: 1)')
    parser.add_argument('--threshold', type=int, default=128,
                       help='Threshold for posterization, 0-255 (default: 128)')

    args = parser.parse_args()

    # Check input file exists
    if not Path(args.input).exists():
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)

    # Create output directory if needed
    output_dir = Path(args.output).parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    try:
        if args.halftone:
            halftone(args.input, args.output, args.dot_size, args.scale)
        elif args.dither:
            bayer_dither(args.input, args.output)
        elif args.posterize:
            posterize(args.input, args.output, args.threshold)
    except Exception as e:
        print(f"Error processing image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
