import streamlit as st
from pathlib import Path
import shutil
import time
import logging
from logger import configure_logging
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorDevice, AcceleratorOptions
from processor import DocumentProcessor

def setup_directories(doc_name: str) -> Path:
    """Create output directory structure for a document."""
    output_dir = Path("output") / doc_name
    (output_dir / "images").mkdir(parents=True, exist_ok=True)
    (output_dir / "chapters").mkdir(parents=True, exist_ok=True)
    return output_dir

def process_document(uploaded_file, output_dir: Path, pipeline_settings: dict):
    """Process document and save results in the structured output directory."""
    logger = logging.getLogger(__name__)
    
    # Save uploaded file temporarily
    temp_path = Path("temp") / uploaded_file.name
    temp_path.parent.mkdir(exist_ok=True)
    logger.debug(f"Created temporary file at: {temp_path}")
    
    with temp_path.open("wb") as f:
        shutil.copyfileobj(uploaded_file, f)
    
    try:
        # Initialize processor
        processor = DocumentProcessor(output_dir)
        logger.debug(f"Initialized DocumentProcessor with output directory: {output_dir}")
        
        # Configure document converter
        logger.debug("Configuring document converter pipeline")
        pipeline_options = PdfPipelineOptions()
        pipeline_options.do_ocr = pipeline_settings['do_ocr']
        pipeline_options.do_table_structure = pipeline_settings['do_table_structure']
        
        # Set OCR languages if provided
        if pipeline_settings['ocr_lang']:
            pipeline_options.ocr_options.lang = [
                lang.strip() for lang in pipeline_settings['ocr_lang'].split(',')
            ]
        
        # Configure accelerator
        device = getattr(AcceleratorDevice, pipeline_settings['accelerator_device'])
        pipeline_options.accelerator_options = AcceleratorOptions(
            device=device,
            num_threads=4  # Default to 4 threads
        )
        
        doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
                InputFormat.DOCX: {},  # Default options for DOCX
                InputFormat.IMAGE: {"ocr_options": {"do_ocr": pipeline_settings['do_ocr']}}
            }
        )
        
        # Convert document
        logger.info("Starting document conversion")
        result = doc_converter.convert(temp_path)
        doc = result.document
        logger.info("Document conversion completed")
        
        # Process document
        doc = processor.update_image_links(doc)
        chapters = []
        
        # Split into chapters if enabled
        if pipeline_settings['enable_chapters']:
            logger.debug("Starting chapter splitting process")
            chapters = processor.split_into_chapters(
                doc,
                heading_level=pipeline_settings['heading_level'],
                min_words=pipeline_settings['min_words'],
                max_words=pipeline_settings['max_words']
            )
            
            # Save main markdown file with chapter links
            logger.debug(f"Created {len(chapters)} chapters")
            main_md = ["# " + temp_path.stem + "\n"]
            main_md.append("## Chapters\n")
            
            for title, _, path in chapters:
                main_md.append(f"- [{title}](chapters/{path.name})")
            
            main_md.append("\n" + doc.export_to_markdown())
            main_content = "\n".join(main_md)
        else:
            # Just save the document without chapters
            logger.debug("Chapter splitting disabled, saving single document")
            main_content = doc.export_to_markdown()
            
        (output_dir / f"{temp_path.stem}.md").write_text(main_content)
        return "Success", main_content, chapters
        
    except Exception as e:
        logger.exception("Document processing failed")
        return f"Error: {str(e)}", None, []
    finally:
        # Cleanup
        temp_path.unlink(missing_ok=True)
        logger.debug("Cleaned up temporary files")

def main():
    # Initialize logging
    configure_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting Document Processor application")
    
    st.title("Document Processor")
    
    # Pipeline options in sidebar
    st.sidebar.header("Processing Options")
    
    # OCR and Table Options
    st.sidebar.subheader("Document Processing")
    do_ocr = st.sidebar.checkbox("Enable OCR", value=True)
    do_table_structure = st.sidebar.checkbox("Process Tables", value=True)
    ocr_lang = st.sidebar.text_input("OCR Languages (comma-sep)", value="en")
    accelerator_device = st.sidebar.selectbox(
        "Accelerator Device", ["AUTO", "CPU", "GPU"], index=0
    )
    
    # Chapter Splitting Options
    st.sidebar.subheader("Chapter Configuration")
    enable_chapters = st.sidebar.checkbox("Enable Chapter Splitting", value=True)
    
    # Initialize chapter settings with defaults
    heading_level = 1
    min_words = 500
    max_words = 8000
    
    # Only show chapter configuration if enabled
    if enable_chapters:
        heading_level = st.sidebar.number_input(
            "Heading Level for Splitting",
            min_value=1,
            max_value=6,
            value=1,
            help="Split chapters at this heading level (1=H1, 2=H2, etc)"
        )
        min_words = st.sidebar.number_input(
            "Minimum Words per Chapter",
            min_value=100,
            max_value=5000,
            value=500,
            help="Chapters with fewer words will be discarded"
        )
        max_words = st.sidebar.number_input(
            "Maximum Words per Chapter",
            min_value=1000,
            max_value=20000,
            value=8000,
            help="Chapters exceeding this limit will be split at the next heading level"
        )
        
        # Validate word count ranges
        if min_words >= max_words:
            st.sidebar.error("Maximum words must be greater than minimum words")
            return
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["pdf", "docx", "jpg", "jpeg", "png"]
    )
    
    if uploaded_file:
        with st.spinner("Processing document..."):
            # Setup directory structure
            doc_name = Path(uploaded_file.name).stem
            logger.info(f"Processing document: {doc_name}")
            output_dir = setup_directories(doc_name)
            
            # Collect pipeline settings
            pipeline_settings = {
                'do_ocr': do_ocr,
                'do_table_structure': do_table_structure,
                'ocr_lang': ocr_lang,
                'accelerator_device': accelerator_device,
                'enable_chapters': enable_chapters,
                'heading_level': heading_level,
                'min_words': min_words,
                'max_words': max_words
            }
            
            # Process document with timing
            start_time = time.time()
            logger.debug(f"Starting document processing with settings: {pipeline_settings}")
            status, markdown, chapters = process_document(
                uploaded_file, output_dir, pipeline_settings
            )
            end_time = time.time() - start_time
            logger.info(f"Document processing completed in {end_time:.2f} seconds")
            
            # Show results
            if "Error" in status:
                logger.error(f"Processing failed: {status}")
                st.error(status)
            else:
                logger.info("Document processed successfully")
                st.success(f"Document processed successfully!")
                
                # Show statistics
                stats = [f"Time taken: {end_time:.2f} seconds"]
                
                if enable_chapters and chapters:
                    total_chapters = len(chapters)
                    total_words = sum(len(content.split()) for _, content, _ in chapters)
                    stats.extend([
                        f"Total chapters: {total_chapters}",
                        f"Total words: {total_words:,}",
                        f"Average words per chapter: {total_words/total_chapters:,.0f}"
                    ])
                
                st.info("\n".join([
                    "Processing Statistics:",
                    *[f"- {stat}" for stat in stats]
                ]))

if __name__ == "__main__":
    main()
