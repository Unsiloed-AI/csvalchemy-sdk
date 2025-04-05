# CSVAlchemy

A Python SDK for processing spreadsheets.

## Installation

```bash
pip install CSVAlchemy-sdk
```

## Overview

CSVAlchemy provides tools for processing Excel and potentially other spreadsheet formats. The library helps you extract data from spreadsheet files.

## Features

* **Spreadsheet Processing** - Handles Excel (.xlsx) files.
* **Data Extraction** - Extracts data from spreadsheet cells.
* **Configurable Parsing** - Allows customization of parsing behavior via configuration.

## Usage

```python
# Example usage (assuming functionality based on existing files)
# Note: Actual function names and usage might differ based on implementation details
# in spreadsheet_parser.py and excel.py

# Likely involves loading a workbook and then parsing it
# from CSVAlchemy.utils import load_workbook # Hypothetical import
# from CSVAlchemy.core import parse_spreadsheet # Hypothetical import
# from CSVAlchemy.config import get_config

# config = get_config()
# workbook = load_workbook("your_spreadsheet.xlsx")
# parsed_data = parse_spreadsheet(workbook, config)

# print(parsed_data)

# Please replace with actual usage examples once core functionality is confirmed.
print("Please update this section with actual usage examples.")
```

## Contributing to CSVAlchemy

We welcome contributions from the community!

### Local Development Setup

1.  **Fork and Clone the Repository**

    ```bash
    git clone https://github.com/Unsiloed-AI/csvalchemy-sdk.git # Replace YOUR_USERNAME
    cd csvalchemy-sdk
    ```

2.  **Set Up a Virtual Environment**

    We recommend using `uv` for package management.

    ```bash
    # Install uv if you haven't already: https://github.com/astral-sh/uv
    uv venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Development Dependencies**

    ```bash
    uv pip install -e ".[dev]"
    ```

4.  **(Optional) Set Up Environment Variables**

    If specific environment variables are needed (e.g., for external services, though none seem required currently), create a `.env` file in the project root.

5.  **Run Tests to Verify Setup**

    ```bash
    pytest
    ```

### Development Workflow

1.  **Create a Feature Branch**

    ```bash
    git checkout -b feature/your-feature-name
    ```

2.  **Make Your Changes**

    - Write code following style guidelines.
    - Add tests for new functionality.
    - Update documentation as needed.

3.  **Run Tests and Linting**

    ```bash
    # Run tests
    pytest

    # Run linting (assuming flake8 is used, adjust if different)
    # flake8 CSVAlchemy tests

    # Run formatter (assuming black is used, adjust if different)
    # black CSVAlchemy tests
    ```
    *(Note: Please configure and add specific linting/formatting tools to `pyproject.toml`)*

4.  **Commit Your Changes**

    Use relevant emojis at the start of your commit messages (e.g., ✨ feat: Add new parser feature).

    ```bash
    git add .
    git commit -m "✨ feat: Describe your change"
    ```

5.  **Push to Your Fork**

    ```bash
    git push origin feature/your-feature-name
    ```

6.  **Create a Pull Request**

    Go to the original repository and create a pull request from your fork.

### Code Style Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) standards.
- Use a consistent code formatter (e.g., [Black](https://black.readthedocs.io/)).
- Write docstrings for public modules, functions, classes, and methods.
- Include type hints according to [PEP 484](https://peps.python.org/pep-0484/).

### Pull Request Process

1.  Ensure all tests pass and code is properly formatted/linted.
2.  Update documentation if necessary.
3.  Link any related issues in your PR description.
4.  Wait for review from maintainers.
5.  Address any requested changes.
6.  Once approved, your PR will be merged.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

