# Troubleshooting Guide

This guide addresses common issues you might encounter when using the Study Tools application.

## Streamlit and PyTorch Compatibility Issue

### Symptoms

When running the application with `streamlit run src/app.py`, you might see errors like:

```
RuntimeError: Tried to instantiate class '__path__._path', but it does not exist! Ensure that it is registered via torch::class_
```

This is caused by Streamlit's file watcher trying to monitor PyTorch modules.

### Solution 1: Use the Custom Launcher Script

We've provided a custom launcher script that sets the necessary environment variables to avoid this issue:

```bash
python run_app.py
```

### Solution 2: Use the Streamlit Configuration

A `.streamlit/config.toml` file has been included in the repository that configures Streamlit to avoid watching problematic modules. This should be automatically used when running the application.

### Solution 3: Set Environment Variables Manually

If you're still experiencing issues, you can set these environment variables before running Streamlit:

```bash
# On Linux/macOS
export STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true
export STREAMLIT_GLOBAL_DEVELOPMENT_MODE=false
streamlit run src/app.py

# On Windows PowerShell
$env:STREAMLIT_SERVER_ENABLE_STATIC_SERVING="true"
$env:STREAMLIT_GLOBAL_DEVELOPMENT_MODE="false"
streamlit run src/app.py
```

## No Chapters Being Detected

### Symptoms

If the application processes your document but doesn't create any chapters, this might be due to:

1. No proper headings in the document
2. Using a heading style that isn't recognized

### Solution

Ensure your document has proper headings. The application recognizes:

- Markdown-style headings (e.g., "# Heading")
- HTML-style headings (h1, h2, etc.)
- Word document headings (when using the Heading styles)

You can adjust the "Heading Level for Splitting" option in the sidebar to match the level of headings in your document.

## Images Not Being Processed

### Symptoms

If images from your document aren't being extracted, check:

1. The log for messages about image paths
2. Whether the document format supports embedded images

### Solution

- For PDF documents, ensure OCR is enabled for image extraction
- For DOCX documents, images should be embedded rather than linked
- Check the logs (in the logs/ directory) for specific error messages

## General Debugging

If you encounter other issues:

1. Check the log files in the `logs/` directory
2. Increase logging verbosity in `.streamlit/config.toml`:
   ```toml
   [logger]
   level = "debug"
   ```
3. Run the application with additional Streamlit debugging:
   ```bash
   streamlit run --logger.level=debug src/app.py
   ```
