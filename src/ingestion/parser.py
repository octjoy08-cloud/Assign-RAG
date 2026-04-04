import fitz  # PyMuPDF
import os
from PIL import Image


def parse_pdf(file_path: str, output_dir="temp_images"):
    doc = fitz.open(file_path)

    os.makedirs(output_dir, exist_ok=True)

    parsed_data = []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        tables = page.get_text("blocks")  # approximation

        # Extract images
        image_list = page.get_images(full=True)
        image_paths = []

        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image_path = f"{output_dir}/page{page_num}_img{img_index}.png"
            with open(image_path, "wb") as f:
                f.write(image_bytes)

            image_paths.append(image_path)

        parsed_data.append({
            "page": page_num,
            "text": text,
            "images": image_paths
        })

    return parsed_data
