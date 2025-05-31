pygpmfparser
A Python package for parsing GoPro Metadata Format (GPMF) data from GoPro videos. Built on top of the GoPro GPMF-parser library, it provides a Pythonic interface to extract telemetry data such as accelerometer (ACCL), GPS (GPS5), and gyroscope (GYRO) data, using pybind11 for C++ bindings.
Features

Extract GPMF telemetry data from GoPro MP4 files.
Pythonic interface with iterator and context manager support.
Validates GPMF data integrity.
Compatible with Poetry for dependency management and distribution.

Installation
From PyPI
If the package is published to PyPI:
poetry add pygpmfparser

Or with pip:
pip install pygpmfparser

From Source

Clone the repository with submodules:
git clone --recursive https://github.com/yourusername/pygpmfparser.git
cd pygpmfparser

If the gpmf-parser/ directory is empty, initialize submodules:
git submodule update --init --recursive


Install Poetry (if not already installed):
pip install poetry


Install dependencies and build the package:
poetry install



Prerequisites

Python: 3.8 or higher
C++ Compiler:
Linux: gcc or clang (sudo apt-get install build-essential)
macOS: Xcode Command Line Tools (xcode-select --install)
Windows: Microsoft Visual C++ Build Tools (Visual Studio 2022, C++ development workload)


Git: For cloning the repository and submodules
Dependencies: pybind11>=2.6 (automatically installed by Poetry)

Usage
The GoProTelemetryExtractor class provides an easy-to-use interface for parsing GPMF data from GoPro MP4 files.
Example
from pygpmfparser.gopro_telemetry_extractor import GoProTelemetryExtractor

# Initialize extractor with a GoPro MP4 file
filepath = "path/to/your/video.mp4"

# Validate GPMF data
with GoProTelemetryExtractor(filepath) as extractor:
    if extractor.validate():
        print("GPMF data is valid")

    # Iterate over samples
    for sample in extractor:
        if sample.key == "ACCL":
            print(f"Accelerometer Sample: {sample}")
        elif sample.key == "GPS5":
            print(f"GPS Sample: {sample}")

# Get all samples as a list
extractor = GoProTelemetryExtractor(filepath)
samples = extractor.get_all_samples()
print(f"Total samples: {len(samples)}")

Parsing Raw Data
The GPMFSample class provides raw data in bytes. To parse it (e.g., for accelerometer data as floats):
import struct
from pygpmfparser.gopro_telemetry_extractor import GoProTelemetryExtractor

with GoProTelemetryExtractor("video.mp4") as extractor:
    for sample in extractor:
        if sample.key == "ACCL" and sample.type_char == "f":
            floats = struct.unpack(f"<{sample.repeat * sample.samples}f", sample.raw_data)
            print(f"Accelerometer values: {floats}")

Project Structure
pygpmfparser/
├── pygpmfparser/
│   ├── __init__.py
│   ├── gpmf_sample.py
│   ├── gopro_telemetry_extractor.py
│   ├── gpmf_bindings.cpp
├── gpmf-parser/  # GoPro GPMF-parser submodule
├── tests/
│   ├── __init__.py
│   ├── test_gpmf_parser.py
├── pyproject.toml
├── build.py
├── README.md
├── LICENSE

Building from Source
Ensure gpmf-parser/ submodule is initialized:
git submodule update --init --recursive

Build the package:
poetry build

Run tests:
poetry run pytest

Publishing to PyPI
To publish the package to PyPI:
poetry publish --build

Configure your PyPI token first:
poetry config pypi-token.pypi <your-token>

Troubleshooting

Submodule missing: If gpmf-parser/ is empty, run git submodule update --init --recursive.
Compilation errors:
Ensure a C++ compiler is installed (see Prerequisites).
On Windows, remove -std=c++11 from build.py or use MSVC-compatible flags.


Test failures: Ensure a valid GoPro MP4 file is available (e.g., gpmf-parser/samples/max-heromode.mp4).

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contributing
Contributions are welcome! Please submit issues or pull requests to the GitHub repository.
