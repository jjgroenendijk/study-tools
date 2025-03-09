# Document Processor

A Streamlit application that processes PDF, DOCX, and image files to create structured markdown documents with chapter splitting and image extraction.

## Features

- Upload PDF, DOCX, and image files
- Convert documents to Markdown format
- Split documents into chapters
- Extract and organize images
- OCR support for images and PDFs
- Clean directory structure for outputs

## Output Structure

```
output/
├── document-name/
│   ├── images/
│   │   └── extracted-images
│   ├── chapters/
│   │   └── split-content
│   └── document-name.md
```

## Requirements

- Python 3.11 or higher
- Docling library
- Streamlit

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install .
   ```

## Running the Application

Start the Streamlit app:
```bash
streamlit run src/app.py
```

## Usage

1. Open the application in your web browser
2. Upload a document using the file picker
3. Wait for processing to complete
4. Browse the generated markdown files and extracted images
5. Use the chapter navigation to view split content

## Document Processing Features

- OCR for scanned documents and images
- Table structure detection
- Chapter detection and splitting
- Image extraction and linking
- Markdown conversion with proper formatting
