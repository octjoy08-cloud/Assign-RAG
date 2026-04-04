import fitz  # PyMuPDF
import os
from PIL import Image
from typing import List, Dict, Any


def parse_pdf(file_path: str, output_dir="temp_images") -> List[Dict[str, Any]]:
    """
    Parse PDF to extract text, tables, and images as separate chunks.
    Uses PyMuPDF as fallback when Docling is not available.

    Returns a list of chunks with metadata for each type.
    """
    doc = fitz.open(file_path)
    os.makedirs(output_dir, exist_ok=True)

    chunks = []

    for page_num, page in enumerate(doc):
        # Extract text content
        text = page.get_text()
        if text.strip():
            # Split text into reasonable chunks
            text_chunks = _chunk_text(text, chunk_size=500)
            for i, text_chunk in enumerate(text_chunks):
                chunks.append({
                    "content": text_chunk,
                    "type": "text",
                    "page": page_num,
                    "metadata": {
                        "text_length": len(text_chunk),
                        "chunk_index": i
                    }
                })

        # Extract images
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image_path = f"{output_dir}/page{page_num}_img{img_index}.png"
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            chunks.append({
                "content": "",  # Will be filled with description during embedding
                "type": "image",
                "page": page_num,
                "image_path": image_path,
                "metadata": {
                    "image_index": img_index,
                    "image_format": base_image.get("ext", "png")
                }
            })

        # Extract tables (basic approximation using text blocks)
        try:
            # Get text blocks which might contain table data
            blocks = page.get_text("dict")["blocks"]
            table_blocks = []

            for block in blocks:
                if "lines" in block:
                    # Check if this looks like a table (multiple lines with similar structure)
                    lines = block["lines"]
                    if len(lines) > 2:  # At least 3 lines for a table
                        table_text = ""
                        for line in lines:
                            line_text = ""
                            for span in line["spans"]:
                                line_text += span["text"] + " "
                            table_text += line_text.strip() + "\n"

                        if table_text.strip():
                            table_blocks.append(table_text.strip())

            # Add table chunks
            for i, table_text in enumerate(table_blocks):
                chunks.append({
                    "content": table_text,
                    "type": "table",
                    "page": page_num,
                    "metadata": {
                        "table_index": i,
                        "estimated_rows": table_text.count('\n') + 1
                    }
                })

        except Exception as e:
            # If table extraction fails, continue without tables
            pass

    return chunks


def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split text into chunks of approximately chunk_size characters with overlap.
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to end at a sentence boundary
        if end < len(text):
            # Look for sentence endings within the last 100 characters
            search_end = min(end + 100, len(text))
            sentence_end = text.rfind('.', end, search_end)
            if sentence_end == -1:
                sentence_end = text.rfind('!', end, search_end)
            if sentence_end == -1:
                sentence_end = text.rfind('?', end, search_end)
            if sentence_end != -1:
                end = sentence_end + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move start position with overlap
        start = max(start + 1, end - overlap)

        # Avoid infinite loop
        if start >= len(text):
            break

    return chunks
