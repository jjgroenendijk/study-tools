# Study Tools

A Python application for processing educational documents, splitting them into chapters, and extracting images to make study materials more accessible.

## Features

- Process PDF, DOCX, and image files
- Split documents into chapters based on headings
- Extract and organize embedded images
- Convert documents to clean markdown format
- Configure chapter splitting based on heading levels and word counts
- Streamlit-based web interface for easy use

## Installation

```bash
# Clone the repository
git clone https://github.com/jjgroenendijk/study-tools.git
cd study-tools

# Install the package
pip install -e .
```

See the [Installation Guide](docs/installation.md) for more detailed instructions.

## Usage

The recommended way to run the application is with our custom launcher script:

```bash
python run_app.py
```

Alternatively, you can run the Streamlit app directly:

```bash
streamlit run src/app.py
```

See the [User Guide](docs/user_guide.md) for instructions on using the application.

## Documentation

- [Installation Guide](docs/installation.md)
- [User Guide](docs/user_guide.md)
- [Development Guide](docs/development.md)
- [Troubleshooting Guide](docs/troubleshooting.md)

## Known Issues

There's a known issue with Streamlit and PyTorch that can cause errors when running the application directly with `streamlit run`. If you encounter this, please use our custom launcher script (`python run_app.py`) or see the [Troubleshooting Guide](docs/troubleshooting.md) for solutions.

## Development

See the [Development Guide](docs/development.md) for details on the project structure and how to contribute.

## License

This project is licensed under the MIT License.
