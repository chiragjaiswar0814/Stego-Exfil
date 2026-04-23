#!/usr/bin/env python3
"""
LSB Steganography Tool - Hide and retrieve secret messages in PNG images.
"""

import sys
import hashlib
from PIL import Image


def calculate_md5(filepath: str) -> str:
    """Calculate MD5 hash of a file."""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()


def text_to_binary(text: str) -> str:
    """Convert text to binary string."""
    return ''.join(format(ord(char), '08b') for char in text)


def binary_to_text(binary: str) -> str:
    """Convert binary string to text."""
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(char, 2)) for char in chars)


def encode_message(image_path: str, message: str, output_path: str) -> None:
    """
    Hide a secret message in an image using LSB steganography.
    """
    # Calculate original MD5
    original_md5 = calculate_md5(image_path)
    print(f"[INFO] Original MD5: {original_md5}")

    # Load image
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    pixels = list(img.getdata())
    width, height = img.size

    # Prepare binary message (add delimiter)
    delimiter = '###'
    full_message = message + delimiter
    binary_message = text_to_binary(full_message)

    # Check capacity
    max_bits = len(pixels) * 3  # 3 channels per pixel
    if len(binary_message) > max_bits:
        raise ValueError(f"Message too long. Max characters: {max_bits // 8}")

    print(f"[INFO] Encoding {len(message)} characters ({len(binary_message)} bits)")

    # Encode message into LSB of pixels
    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        r, g, b = pixel
        if bit_index < len(binary_message):
            r = (r & ~1) | int(binary_message[bit_index])
            bit_index += 1
        if bit_index < len(binary_message):
            g = (g & ~1) | int(binary_message[bit_index])
            bit_index += 1
        if bit_index < len(binary_message):
            b = (b & ~1) | int(binary_message[bit_index])
            bit_index += 1
        new_pixels.append((r, g, b))

    # Create new image with modified pixels
    new_img = Image.new('RGB', (width, height))
    new_img.putdata(new_pixels)
    new_img.save(output_path, 'PNG')

    # Calculate new MD5
    new_md5 = calculate_md5(output_path)
    print(f"[INFO] Modified MD5: {new_md5}")
    print(f"[INFO] MD5 Changed: {original_md5 != new_md5}")
    print(f"[SUCCESS] Message hidden in: {output_path}")


def decode_message(image_path: str) -> str:
    """
    Extract a hidden message from an image using LSB steganography.
    """
    # Load image
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    pixels = list(img.getdata())

    # Extract LSB from all channels
    binary_data = ''
    for pixel in pixels:
        r, g, b = pixel
        binary_data += str(r & 1)
        binary_data += str(g & 1)
        binary_data += str(b & 1)

    # Convert to text
    delimiter = '###'
    message = binary_to_text(binary_data)

    # Find delimiter
    if delimiter in message:
        return message.split(delimiter)[0]
    else:
        raise ValueError("No hidden message found or image not encoded by this tool")


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Encode: python stego.py encode <image.png> <'secret message'> [output.png]")
        print("  Decode: python stego.py decode <image.png>")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'encode':
        if len(sys.argv) < 4:
            print("Error: encode requires image path and message")
            sys.exit(1)
        image_path = sys.argv[2]
        message = sys.argv[3]
        output_path = sys.argv[4] if len(sys.argv) > 4 else 'output.png'
        encode_message(image_path, message, output_path)

    elif command == 'decode':
        image_path = sys.argv[2]
        try:
            message = decode_message(image_path)
            print(f"[SUCCESS] Hidden message: {message}")
        except ValueError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
