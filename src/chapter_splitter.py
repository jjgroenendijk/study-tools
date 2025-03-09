from pathlib import Path
from typing import List, Tuple
import logging
from docling_core.types.doc import DoclingDocument, TextItem, NodeItem

class ChapterSplitter:
    def __init__(self, output_dir: Path):
        self.chapters_dir = output_dir / "chapters"
        self.logger = logging.getLogger(__name__)
        
    def split_document(
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
        self.logger.info("Starting document splitting process")
        chapters = []
        current_chapter = []
        current_title = "Introduction"

        def is_heading(item: TextItem) -> bool:
            """Check if item is a heading at the specified level."""
            if not getattr(item, "style", {}).get("is_heading", False):
                return False
            # Count '#' characters at start of text to determine heading level
            text = item.text.strip()
            if text.startswith('#'):
                level = text.split(' ')[0].count('#')
                is_target = level == heading_level
                if is_target:
                    self.logger.debug(f"Found heading at target level {heading_level}: {text}")
                return is_target
            return False

        def get_word_count(text: str) -> int:
            """Get word count from text, stripping markdown formatting."""
            # Simple word count - could be improved for accuracy
            return len(text.split())

        def split_by_subheadings(content: str, title: str, level: int) -> List[Tuple[str, str]]:
            """Recursively split content by next heading level."""
            if level >= 6:  # Max heading level
                self.logger.debug(f"Reached max heading level for {title}, splitting by paragraphs")
                # Split by paragraphs as fallback
                paragraphs = content.split('\n\n')
                result = []
                current_content = []
                current_words = 0
                
                for p in paragraphs:
                    p_words = get_word_count(p)
                    if current_words + p_words > max_words:
                        if current_content:
                            part_num = len(result) + 1
                            self.logger.debug(f"Creating new part {part_num} for {title} due to word limit")
                            result.append((f"{title} (Part {part_num})", 
                                         '\n\n'.join(current_content)))
                        current_content = [p]
                        current_words = p_words
                    else:
                        current_content.append(p)
                        current_words += p_words
                
                if current_content:
                    result.append((f"{title} (Part {len(result)+1})", 
                                 '\n\n'.join(current_content)))
                return result
            
            # Create new processor with increased heading level
            temp_chapters = []
            current_content = []
            current_subtitle = title
            
            lines = content.split('\n')
            for line in lines:
                if line.strip().startswith('#' * (level + 1) + ' '):
                    if current_content:
                        temp_chapters.append((current_subtitle, '\n'.join(current_content)))
                        current_content = []
                    current_subtitle = line.strip('#').strip()
                current_content.append(line)
                
            if current_content:
                temp_chapters.append((current_subtitle, '\n'.join(current_content)))
            
            return temp_chapters

        def process_node(node: NodeItem):
            nonlocal current_chapter, current_title
            
            # Handle nodes without children attribute (e.g., RefItem)
            if not hasattr(node, 'children'):
                if isinstance(node, TextItem):
                    current_chapter.append(node.text)
                return
            
            for child in node.children:
                if isinstance(child, TextItem):
                    if is_heading(child):
                        # Save previous chapter if it has content
                        if current_chapter:
                            chapter_content = "\n\n".join(current_chapter)
                            chapters.append((current_title, chapter_content))
                            current_chapter = []
                        current_title = child.text
                    current_chapter.append(child.text)
                else:
                    process_node(child)

        # Process document body
        process_node(doc.body)

        # Save last chapter
        if current_chapter:
            chapters.append((current_title, "\n\n".join(current_chapter)))

        # Process chapters based on word count limits
        self.logger.info(f"Processing {len(chapters)} raw chapters")
        processed_chapters = []
        for title, content in chapters:
            word_count = get_word_count(content)
            self.logger.debug(f"Chapter '{title}' has {word_count} words")
        
            if word_count < min_words:
                # Skip chapters that are too short
                self.logger.debug(f"Skipping chapter '{title}' - too short ({word_count} words)")
                continue
            elif word_count > max_words:
                # Split large chapters by subheadings
                self.logger.debug(f"Splitting chapter '{title}' - too large ({word_count} words)")
                subchapters = split_by_subheadings(content, title, heading_level + 1)
                for sub_title, sub_content in subchapters:
                    sub_words = get_word_count(sub_content)
                    if sub_words >= min_words:
                        processed_chapters.append((sub_title, sub_content))
            else:
                processed_chapters.append((title, content))

        # Create chapters directory
        self.chapters_dir.mkdir(parents=True, exist_ok=True)

        # Write chapters to files and collect paths
        self.logger.info(f"Writing {len(processed_chapters)} final chapters to disk")
        result = []
        for idx, (title, content) in enumerate(processed_chapters):
            chapter_filename = f"{idx+1:02d}_{self._sanitize_filename(title)}.md"
            chapter_path = self.chapters_dir / chapter_filename
            self.logger.debug(f"Writing chapter {idx+1}: {chapter_path}")
            chapter_path.write_text(content)
            result.append((title, content, chapter_path))

        return result

    def _sanitize_filename(self, filename: str) -> str:
        """Convert string to valid filename."""
        valid_chars = "-_() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        filename = "".join(c if c in valid_chars else "_" for c in filename)
        return filename.strip().lower().replace(" ", "_")
