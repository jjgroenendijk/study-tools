# User Guide

This guide will help you understand how to use the Study Tools application.

## Overview

Study Tools is an application that processes documents (PDF, DOCX, images) and:

1. Extracts and formats the document content
2. Splits the content into chapters based on headings
3. Processes and saves images from the document
4. Converts everything to markdown format for easy study and reference

## Getting Started

After [installing](installation.md) the application, launch it with:

```bash
streamlit run src/app.py
```

This will open the web interface in your browser.

## Using the Application

### Document Upload

1. Click the "Choose a file" button to upload your document (PDF, DOCX, JPG, PNG)
2. Wait for the document to be processed

### Processing Options

The sidebar contains several options to customize processing:

#### Document Processing

- **Enable OCR**: Turn on Optical Character Recognition for images and scanned documents
- **Process Tables**: Extract tables from the document
- **OCR Languages**: Specify languages for OCR (comma-separated, e.g., "en,fr,de")
- **Accelerator Device**: Choose processing hardware (AUTO, CPU, GPU)

#### Chapter Configuration

- **Enable Chapter Splitting**: Split the document into chapters
- **Heading Level for Splitting**: Choose which heading level to split at (1=H1, 2=H2, etc.)
- **Minimum Words per Chapter**: Chapters with fewer words will be discarded
- **Maximum Words per Chapter**: Chapters exceeding this will be split at the next heading level

### Output

After processing, the application will:

1. Display processing statistics
2. Create a structured output directory with:
   - A main markdown file containing the full document
   - A "chapters" subdirectory with individual chapter files
   - An "images" subdirectory with all extracted images

Output is saved to the `output/[document-name]/` directory.

## Tips for Best Results

- For PDFs, enable OCR if you have scanned documents
- Choose appropriate heading levels for meaningful chapter splitting
- For documents with images, all images will be extracted and saved
- Adjust min/max word counts to get chapter sizes that work for your study needs

## Troubleshooting

If you encounter issues:

- Check the log files in the `logs/` directory
- Ensure your document is not corrupted
- Verify that the document has proper headings if using chapter splitting
