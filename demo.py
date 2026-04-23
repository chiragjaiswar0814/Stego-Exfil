#!/usr/bin/env python3
"""
Demo script showcasing the steganography tool functionality.
"""

from PIL import Image
import os
from stego import encode_message, decode_message, calculate_md5


def create_test_image(filename: str, size: tuple = (100, 100)):
    """Create a simple test image with random colors."""
    import random
    img = Image.new('RGB', size)
    pixels = [(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
              for _ in range(size[0] * size[1])]
    img.putdata(pixels)
    img.save(filename)
    return filename


def main():
    print("=" * 60)
    print("LSB STEGANOGRAPHY DEMO")
    print("=" * 60)

    # Create test image
    test_image = 'test_image.png'
    print(f"\n[1] Creating test image: {test_image}")
    create_test_image(test_image)
    print(f"    Size: {os.path.getsize(test_image)} bytes")

    # Secret message
    secret = "This is a secret message hidden in the image!"
    print(f"\n[2] Secret message to hide:")
    print(f"    '{secret}'")

    # Encode
    output_image = 'stego_image.png'
    print(f"\n[3] Encoding message into {output_image}...")
    encode_message(test_image, secret, output_image)
    print(f"    Size after encoding: {os.path.getsize(output_image)} bytes")

    # Compare file sizes
    original_size = os.path.getsize(test_image)
    stego_size = os.path.getsize(output_image)
    print(f"\n[4] File Size Analysis:")
    print(f"    Original:  {original_size} bytes")
    print(f"    Stego:     {stego_size} bytes")
    print(f"    Difference: {stego_size - original_size} bytes")

    # Decode
    print(f"\n[5] Decoding message from {output_image}...")
    decoded = decode_message(output_image)
    print(f"    Decoded: '{decoded}'")

    # Verify
    print(f"\n[6] Verification:")
    print(f"    Message matches: {secret == decoded}")

    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
