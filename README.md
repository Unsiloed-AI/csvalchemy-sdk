# CSVAlchemy

A  Python SDK for processing and analyzing spreadsheets using LLMs.

## Installation

```bash
pip install CSVAlchemy-sdk
```

## Overview

CSVAlchemy provides Excel processing capabilities. The library helps you efficiently process, analyze, and extract insights from spreadsheet data.

## Features

* **Spreadsheet Processing** - Handle Excel and CSV files with advanced features
* **Data Extraction** - Extract structured data from complex spreadsheets
* **Formula Extraction** - Extract all the formula's from you spreadsheets
* **Pivot Table Support** - Process and analyze pivot tables
* **Chart Analysis** - Extract and encode chart data
* **Conditional Formatting** - Capture conditional formatting rules
* **API Client** - Easy-to-use client for the CSVAlchemy API

## CSVAlchemy Feature Comparison

| Feature                          | Support                                        |
|----------------------------------|------------------------------------------------|
| Excel (.xlsx) Processing         | ✓                                              |
| Formula Extraction               | ✓                                              |
| Merged Cell Detection            | ✓                                              |
| Header Detection                 | ✓ (configurable)                               |
| Structural Anchor Extraction     | ✓                                              |
| Python SDK                       | ✓                                              |
| Customizable Configuration       | ✓                                              |
| Error Handling Modes             | ✓ (configurable)                               |
| Parallel Processing              | ✓ (configurable)                               |
| Memory Optimization              | ✓ (chunking configurable)                      |
| Comprehensive Logging            | ✓                                              |
| Open Source                      | ✓ (MIT License)                                |

## Usage

```python
from CSValchemy_sdk.core import encode_workbook
from CSValchemy_sdk.utils import load_workbook_from_file
from CSValchemy_sdk.config import get_config

# Process spreadsheets
workbook = load_workbook_from_file("Company_Financial_Data_For_PE.xlsx")
config = get_config()
encoded_data = encode_workbook(workbook, config)

# Now use the encoded data in your application
print("encoded_sheets ",encoded_data)
print(f"Processed {len(encoded_data['sheets'])} sheets")
```

<!-- ## Advanced Configuration

CSVAlchemy offers extensive configuration options:

```python
from CSValchemy_sdk import encode_workbook
from CSValchemy_sdk.config import get_config

# Get default configuration
config = get_config()

# Customize configuration
config["features"]["pivot_tables"] = True
config["error_handling"]["log_level"] = "DEBUG"

# Process with custom configuration
encoded = encode_workbook("your_spreadsheet.xlsx", config=config)
``` -->



## API Documentation

Full API documentation is available at:
- Interactive API docs: `/docs`
- ReDoc API docs: `/redoc`

## Contributing to CSVAlchemy

We welcome contributions from the community! This guide will help you set up your local development environment and understand our contribution process.

### Local Development Setup

1. **Fork and Clone the Repository**

   ```bash
   git clone https://github.com/Unsiloed-ai/spreadsheet-llm.git
   cd spreadsheet-llm
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**

   ```bash
   pip install -e ".[dev]"
   ```

5. **Run Tests to Verify Setup**

   ```bash
   pytest
   ```

### Development Workflow

1. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   
   - Write code following our style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Run Tests and Linting**

   ```bash
   # Run tests
   pytest
   
   # Run linting
   flake8
   
   # Run formatter
   black .
   ```

4. **Commit Your Changes**

   ```bash
   git add .
   git commit -m "Add a descriptive commit message"
   ```

5. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   
   Go to the [original repository](https://github.com/Unsiloed-AI/spreadsheet-llm) and create a pull request from your fork.

### Code Style Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) standards
- Use [Black](https://black.readthedocs.io/) for code formatting
- Write docstrings for all functions, classes, and methods
- Include type hints according to [PEP 484](https://peps.python.org/pep-0484/)

### Pull Request Process

1. Ensure all tests pass and code is properly formatted
2. Update documentation if necessary
3. Link any related issues in your PR description
4. Wait for review from maintainers
5. Address any requested changes
6. Once approved, your PR will be merged

### Running the API Locally

To run the API server locally during development:

```bash
python run.py
```

The API will be available at http://localhost:8000 with interactive documentation at http://localhost:8000/docs.

### Building the Package Locally

To build the package locally:

```bash
python -m build
```

### Contact

If you have questions or need help, please:
- Open an issue on GitHub
- Contact the maintainers at hello@unsiloed-ai.com

Thank you for contributing to CSVAlchemy!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## About

Developed by [Unsiloed AI](https://unsiloed-ai.com)
