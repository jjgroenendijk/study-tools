# Development Guide

This guide provides information for developers who want to contribute to the Study Tools project.

## Project Structure

```
study-tools/
├── docs/              # Documentation
├── logs/              # Application logs
├── output/            # Processed document output
├── src/               # Source code
│   ├── app.py         # Main Streamlit application
│   ├── chapter_splitter.py # Document splitting logic
│   ├── logger.py      # Logging configuration
│   └── processor.py   # Document processing logic
├── temp/              # Temporary files during processing
├── pyproject.toml     # Project configuration
└── README.md          # Project overview
```

## Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/jjgroenendijk/study-tools.git
   cd study-tools
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

The project uses Ruff for code formatting and linting, configured in pyproject.toml. To run:

```bash
ruff format src/
ruff check src/
```

## Key Components

### DocumentProcessor (processor.py)

Responsible for:
- Splitting documents into chapters
- Processing images and updating their paths
- Coordinating the overall document processing

### ChapterSplitter (chapter_splitter.py)

Handles:
- Extracting chapters from documents based on heading levels
- Managing word count constraints for chapters
- Generating markdown files for each chapter

### Streamlit UI (app.py)

Provides:
- User interface for uploading documents
- Configuration options for processing
- Display of processing results

### Logging (logger.py)

Manages:
- Application-level logging
- File and console output
- Log rotation

## Testing

Tests can be run using pytest:

```bash
pytest
```

## Common Issues

### Image Processing

Images are expected to have either a `source_path`, `path`, or `image_path` attribute, or binary data. Images without these are skipped.

### Chapter Splitting

Chapter splitting relies on heading detection, which works through:
1. Style attributes that indicate headings
2. Markdown-style headers (e.g., "# Heading")

If chapter splitting isn't working, check if headers are properly formatted.

## Contributing

1. Create a branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Run code formatting and linting:
   ```bash
   ruff format src/
   ruff check src/
   ```

4. Commit with descriptive messages
5. Push and create a pull request against the development branch

## Release Process

1. Merge changes into the development branch
2. Test thoroughly
3. Update version number in pyproject.toml
4. Create a pull request to merge development into main
5. Tag the release in git
