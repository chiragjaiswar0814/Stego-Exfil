# Stego-Exfil

A forensic-grade steganography tool for hiding and retrieving secret messages within PNG images using Least Significant Bit (LSB) encoding.

## Overview

This tool implements LSB steganography to embed text data imperceptibly within image files. The technique modifies only the least significant bits of pixel color channels, preserving the visual appearance while encoding hidden information.

## Features

- **LSB Encoding**: Hide text in RGB channels (3 bits per pixel)
- **LSB Decoding**: Extract hidden messages from stego-images
- **Delimiter-based Framing**: Automatic message boundary detection using `###` delimiter
- **Forensic Verification**: MD5 hash comparison before/after encoding
- **CLI Interface**: Simple command-line interface for encoding/decoding
- **Demo Script**: Automated demonstration of full workflow

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Command Line

**Encode a message:**
```bash
python stego.py encode <input.png> "<secret message>" [output.png]
```

**Decode a message:**
```bash
python stego.py decode <stego_image.png>
```

### Examples

```bash
# Hide a secret message
python stego.py encode photo.png "Meeting at 14:00" secret.png

# Retrieve the hidden message
python stego.py decode secret.png
# Output: [SUCCESS] Hidden message: Meeting at 14:00
```

### Demo

Run the automated demo to see the full workflow:

```bash
python demo.py
```

The demo will:
1. Generate a test image
2. Encode a secret message
3. Compare MD5 hashes
4. Decode and verify the message

## How It Works

### Encoding Process

1. Convert the message to binary (8 bits per character)
2. Append `###` delimiter for boundary detection
3. Iterate through pixels, modifying LSB of R, G, B channels
4. Save the modified image as PNG

### Decoding Process

1. Extract LSB from each RGB channel
2. Reconstruct binary data stream
3. Convert binary to text
4. Search for `###` delimiter to locate message end

### Capacity

Maximum message size depends on image dimensions:
- **Formula**: `(width × height × 3) / 8` characters
- **Example**: 100×100 image = ~3,750 characters

## Forensic Analysis

| Metric | Observation |
|--------|-------------|
| **Visual Appearance** | Identical to original |
| **File Size** | Unchanged (LSB modification doesn't affect compression) |
| **MD5 Hash** | Changes (detectable by hashing) |
| **Statistical Analysis** | May show subtle anomalies in chi-square tests |

## Technical Details

- **Library**: Pillow (PIL) for image manipulation
- **Delimiter**: `###` marks end of hidden message
- **Channels Used**: Red, Green, Blue (3 bits per pixel)
- **Supported Formats**: PNG (lossless compression required)

## Limitations

- Works best with PNG files (lossless compression)
- JPEG encoding will corrupt hidden data due to lossy compression
- Very small images have limited capacity
- MD5 hash changes make detection possible with forensic tools

## File Structure

```
Stego-Exfil/
├── stego.py          # Core steganography library
├── demo.py           # Demonstration script
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## License

Educational use only. For forensic research and authorized security testing.
