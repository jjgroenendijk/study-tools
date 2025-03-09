# Installation Guide

The Study Tools package can be installed using pip or directly from source.

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git (for installation from source)

## Installation from PyPI

```bash
pip install study-tools
```

## Installation from Source

```bash
# Clone the repository
git clone https://github.com/jjgroenendijk/study-tools.git
cd study-tools

# Install the package in development mode
pip install -e .
```

## Dependencies

The following dependencies will be automatically installed:

- docling: Document processing library
- docling_core: Core components for document processing
- streamlit: Web UI framework
- pydantic: Data validation and settings management
- ruff: Code formatting and linting

## Running the Application

After installation, you can start the application with:

```bash
streamlit run src/app.py
```

This will launch the web UI in your default browser.
