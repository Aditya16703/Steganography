import os
import importlib

try:
    setuptools = importlib.import_module("setuptools")
    setup = setuptools.setup
    find_packages = setuptools.find_packages
except Exception:
    raise RuntimeError(
        "setuptools is required to run this setup script; please install it (e.g., pip install setuptools)"
    )

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="steganoguard-pro",
    version="2.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Advanced Secure Steganography Application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/SteganoGuard-Pro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "steganoguard=main:main",
        ],
    },
    include_package_data=True,
)