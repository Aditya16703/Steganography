Steganography Project (Python)

A Python-based tool that securely hides sensitive information using image, audio, and text steganography techniques. The project demonstrates how data can be embedded inside different media formats without visibly altering their original structure.

Features
1. Image Steganography

Embeds secret messages into image pixels using LSB (Least Significant Bit) manipulation.

Ensures the visual quality of the image remains unchanged.

2. Audio Steganography

Encodes data into audio files by modifying frequency components.

Maintains the natural sound quality while carrying hidden information.

3. Text Steganography

Hides data within structured text using pattern-based techniques.

Produces readable text while secretly embedding the message.

Tech Stack

Python 3

Libraries: Pillow, wave, numpy, os


Project Structure
steganographyProject/
│── src/
│   ├── image_stego.py
│   ├── audio_stego.py
│   ├── text_stego.py
│── tests/
│── docs/
│── run.py
│── setup.py
│── README.md




Usage

Run the main script:

python run.py



Select:

Image Steganography

Audio Steganography

Text Steganography

Follow the on-screen instructions to hide or extract data

Created as a practical demonstration of steganography techniques for learning and security research.
