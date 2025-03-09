#!/usr/bin/env python3
"""
Custom launcher script for Study Tools application.
Disables Streamlit's file watcher for PyTorch modules to avoid errors.
"""
import os
import subprocess
import sys

if __name__ == "__main__":
    # Set environment variables to disable file watching for problematic modules
    os.environ["STREAMLIT_SERVER_ENABLE_STATIC_SERVING"] = "true"
    os.environ["STREAMLIT_GLOBAL_DEVELOPMENT_MODE"] = "false"
    
    # Run streamlit with our app
    cmd = [sys.executable, "-m", "streamlit", "run", "src/app.py"]
    subprocess.run(cmd)
