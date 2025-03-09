from pathlib import Path
from typing import List, Tuple
import logging
from docling.document_converter import DocumentConverter
from docling_core.types.doc import DoclingDocument
from chapter_splitter import ChapterSplitter

class DocumentProcessor:
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.images_dir = output_dir / "images"
        self.chapters_dir = output_dir / "chapters"
        self.chapter_splitter = ChapterSplitter(output_dir)
        self.logger = logging.getLogger(__name__)

    def split_into_chapters(
        self, 
        doc: DoclingDocument, 
        heading_level: int = 1, 
        min_words: int = 500, 
        max_words: int = 8000
    ) -> List[Tuple[str, str, Path]]:
        """
        Split document into chapters based on heading levels with word count constraints.
        Returns list of tuples containing (title, content, file_path).
        
        Args:
            doc: Document to split
            heading_level: Level of headings to split on (1-6)
            min_words: Minimum words per chapter (chapters below this are discarded)
            max_words: Maximum words per chapter (chapters above this are split further)
        """
        self.logger.debug(
            f"Splitting document into chapters. Heading level: {heading_level}, "
            f"Min words: {min_words}, Max words: {max_words}"
        )
        result = self.chapter_splitter.split_document(doc, heading_level, min_words, max_words)
        self.logger.info(f"Split document into {len(result)} chapters")
        return result

    def update_image_links(self, doc: DoclingDocument) -> DoclingDocument:
        """Update image links to use relative paths."""
        self.logger.debug(f"Processing {len(doc.pictures)} images")
        for idx, picture in enumerate(doc.pictures):
            # Copy image to images directory
            # Access the image path using the correct attribute
            if hasattr(picture, 'source_path') and picture.source_path:
                source_path = Path(picture.source_path)
            elif hasattr(picture, 'path') and picture.path:
                source_path = Path(picture.path)
            else:
                self.logger.warning(f"Image {idx} has no valid source path, skipping")
                continue

            new_filename = f"image_{idx}{source_path.suffix}"
            new_path = self.images_dir / new_filename
            
            if source_path.exists():
                self.logger.debug(f"Copying image {idx} from {source_path} to {new_path}")
                new_path.parent.mkdir(parents=True, exist_ok=True)
                new_path.write_bytes(source_path.read_bytes())
                
                # Update path in document using corresponding attribute
                if hasattr(picture, 'source_path'):
                    picture.source_path = f"images/{new_filename}"
                    self.logger.debug(f"Updated source_path for image {idx}")
                if hasattr(picture, 'path'):
                    picture.path = f"images/{new_filename}"
                    self.logger.debug(f"Updated path for image {idx}")

        return doc
