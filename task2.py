import fitz  # PyMuPDF
import numpy as np
import pytesseract
from typing import List


def classify_all_pages(input_pdf: str) -> List[int]:
    """
    Analyze all pages in the input PDF and determine the class of the pdf page

    Args:
    input_pdf (str): The file path of the input PDF.

    Returns:
    List[int]: A list of classes for each page.
            0: machine-readable
            1: non-machine readable but OCR-able
            2: non-machine readable and not OCR-able
    """
    doc = fitz.open(input_pdf)
    classes = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)

        page_class = classify_page(page)
        classes.append(page_class)
    doc.close()
    return classes


def classify_page(page) -> int:
    """
    Determine the class of the pdf page.

    Args:
    page (PdfReader.PageObject): A single page from a PDF.

    Returns:
    int: The page is
        0: machine-readable
        1: non-machine readable but OCR-able
        2: non-machine readable and not OCR-able
    """
    # Get the page dimensions
    header_height = 100
    footer_height = 100
    rect = page.rect
    page_width = rect.width
    page_height = rect.height
    # Calculate the new cropping rectangle
    new_rect = fitz.Rect(0, header_height, page_width, page_height - footer_height)

    # Apply the crop to the page
    page.set_cropbox(new_rect)

    text = page.get_text("text")
    pix = page.get_pixmap()
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)

    # Heuristic checks
    print(text.strip())
    if text.strip() != "":
        return 0
    else:
        try:
            # Attempt OCR
            _ = pytesseract.image_to_string(img)
            return 1
        except:
            return 2



"""
# It should be noted that the pdf have been machine generated via the template.
# As such all of them will be classified as machine-readable pdf
# Although the first file in grouped_pdf is an image it contains header and footer
# Hence, I have removed the header and footer to better identify the class for this example pdf.
"""
# Example usage
pdf_path: str = r'grouped_documents.pdf'
page_classes: List[int] = classify_all_pages(pdf_path)
print(f"Classes for each page: {page_classes}")
