from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
import os
from typing import List, Dict, Any


def parse_pdf(file_path: str, output_dir="temp_images") -> List[Dict[str, Any]]:
    """
    Parse PDF using Docling to extract text, tables, and images as separate chunks.

    Returns a list of chunks with metadata for each type.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Configure Docling pipeline
    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True  # Enable OCR for better text extraction
    pipeline_options.do_table_structure = True  # Extract table structure

    doc_converter = DocumentConverter(
        format_options={InputFormat.PDF: pipeline_options}
    )

    # Convert document
    result = doc_converter.convert(file_path)
    doc = result.document

    chunks = []

    # Process each item in the document
    for item, level in doc.iterate_items():
        chunk_data = {
            "content": item.text,
            "type": item.__class__.__name__.lower(),
            "page": getattr(item, 'page_no', 0),
            "metadata": {}
        }

        # Handle different item types
        if hasattr(item, 'image') and item.image:
            # Image chunk
            chunk_data["type"] = "image"
            # Save image to file
            image_filename = f"{output_dir}/page{chunk_data['page']}_img_{len(chunks)}.png"
            with open(image_filename, "wb") as f:
                item.image.save(f, format="PNG")
            chunk_data["image_path"] = image_filename
            chunk_data["metadata"]["image_size"] = getattr(item.image, 'size', None)

        elif hasattr(item, 'table_data') and item.table_data:
            # Table chunk
            chunk_data["type"] = "table"
            # Convert table to markdown format
            if hasattr(item, 'export_to_markdown'):
                chunk_data["content"] = item.export_to_markdown()
            chunk_data["metadata"]["table_rows"] = len(item.table_data) if item.table_data else 0
            chunk_data["metadata"]["table_cols"] = len(item.table_data[0]) if item.table_data and item.table_data[0] else 0

        else:
            # Text chunk
            chunk_data["type"] = "text"
            chunk_data["metadata"]["text_length"] = len(item.text)

        chunks.append(chunk_data)

    return chunks
