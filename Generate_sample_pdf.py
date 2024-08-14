""" Generate long Fake-PDF data representative of a real-world scenario
    - machine-readable vs not machine-readable
    - rotated vs not rotated
    - 5 different document types """

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import black, red, blue, green, orange, purple
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import random

def create_image_with_text(text: str, width: int, height: int) -> Image.Image:
    """Create an image with the given text."""
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((10, 10), text, font=font, fill='black')
    return image

def add_colored_border(pdf, color):
    """Add a colored border to the page."""
    pdf.setStrokeColor(color)
    pdf.setLineWidth(10)
    pdf.rect(5, 5, letter[0]-10, letter[1]-10, fill=0, stroke=1)

def add_watermark(pdf, text):
    """Add a watermark to the page."""
    pdf.saveState()
    pdf.setFont("Helvetica", 60)
    pdf.setFillColor(blue, alpha=0.3)
    pdf.translate(letter[0]/2, letter[1]/2)
    pdf.rotate(45)
    pdf.drawCentredString(0, 0, text)
    pdf.restoreState()

def add_header(pdf, text, color):
    """Add a colored header to the page."""
    pdf.setFillColor(color)
    pdf.rect(0, letter[1] - 0.5*inch, letter[0], 0.5*inch, fill=1, stroke=0)
    pdf.setFillColor(black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(0.5*inch, letter[1] - 0.3*inch, text)

def add_footer(pdf, text, color):
    """Add a colored footer to the page."""
    pdf.setFillColor(color)
    pdf.rect(0, 0, letter[0], 0.5*inch, fill=1, stroke=0)
    pdf.setFillColor(black)
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(0.5*inch, 0.2*inch, text)

def create_rotated_text_pdf(filename: str) -> None:
    """
    Create a PDF with 15 pages, visually grouped into five documents.
    :param filename: str, the name of the output PDF file
    """
    pdf = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Document 1: Pages 1-3 (Colored border)
    for page in range(3):
        add_colored_border(pdf, red)
        
        if page == 0:
            # First page with logo
            logo_path = "./logo.png"
            pdf.drawImage(logo_path, 0.5*inch, 0.5*inch, width=width-inch, height=height-inch, preserveAspectRatio=True, anchor='c')
        else:
            text = f"This is page {page + 1} of Document 1"
            rotation = random.randint(0, 359)
            pdf.setFont("Helvetica", 14)
            pdf.setFillColor(black)
            x, y = width / 2, height / 2
            pdf.saveState()
            pdf.translate(x, y)
            pdf.rotate(rotation)
            pdf.drawString(-100, 0, text)
            pdf.restoreState()
        
        pdf.drawString(0.5*inch, 0.25*inch, f"Document 1 - Page {page + 1}")
        pdf.showPage()

    # Document 2: Pages 4-6 (Watermark)
    for page in range(3):
        add_watermark(pdf, "Document 2")
        
        text = f"This is page {page + 1} of Document 2"
        rotation = random.randint(0, 359)
        img = create_image_with_text(text, int(width), int(height))
        img = img.rotate(rotation, expand=1)
        img_reader = ImageReader(img)
        pdf.drawImage(img_reader, 0, 0, width=width, height=height)
        
        pdf.setFillColor(black)
        pdf.drawString(0.5*inch, 0.25*inch, f"Document 2 - Page {page + 1}")
        pdf.showPage()

    # Document 3: Pages 7-9 (Colored background)
    for page in range(3):
        pdf.setFillColor(green, alpha=0.1)
        pdf.rect(0, 0, width, height, fill=1, stroke=0)
        
        text = f"This is page {page + 1} of Document 3"
        rotation = random.randint(0, 359)
        pdf.setFont("Helvetica", 14)
        pdf.setFillColor(black)
        x, y = width / 2, height / 2
        pdf.saveState()
        pdf.translate(x, y)
        pdf.rotate(rotation)
        pdf.drawString(-100, 0, text)
        pdf.restoreState()
        
        pdf.drawString(0.5*inch, 0.25*inch, f"Document 3 - Page {page + 1}")
        pdf.showPage()

    # Document 4: Pages 10-12 (Colored header)
    for page in range(3):
        add_header(pdf, f"Document 4 - Page {page + 1}", orange)
        
        text = f"This is page {page + 1} of Document 4"
        rotation = random.randint(0, 359)
        pdf.setFont("Helvetica", 14)
        pdf.setFillColor(black)
        x, y = width / 2, height / 2
        pdf.saveState()
        pdf.translate(x, y)
        pdf.rotate(rotation)
        pdf.drawString(-100, 0, text)
        pdf.restoreState()
        
        pdf.showPage()

    # Document 5: Pages 13-15 (Colored footer)
    for page in range(3):
        add_footer(pdf, f"Document 5 - Page {page + 1}", purple)
        
        text = f"This is page {page + 1} of Document 5"
        rotation = random.randint(0, 359)
        pdf.setFont("Helvetica", 14)
        pdf.setFillColor(black)
        x, y = width / 2, height / 2
        pdf.saveState()
        pdf.translate(x, y)
        pdf.rotate(rotation)
        pdf.drawString(-100, 0, text)
        pdf.restoreState()
        
        pdf.showPage()
        
    # Document 6: Pages 15-17 (Watermark)
    for page in range(3):
        add_watermark(pdf, "Document 2")
        
        text = f"This is page {page + 1} of Document 2"
        rotation = random.randint(0, 359)
        img = create_image_with_text(text, int(width), int(height))
        img = img.rotate(rotation, expand=1)
        img_reader = ImageReader(img)
        pdf.drawImage(img_reader, 0, 0, width=width, height=height)
        
        pdf.setFillColor(black)
        pdf.drawString(0.5*inch, 0.25*inch, f"Document 2 - Page {page + 1}")
        pdf.showPage()

    pdf.save()

output_pdf = "grouped_documents.pdf"
create_rotated_text_pdf(output_pdf)
print(f"PDF '{output_pdf}' has been created with 17 pages grouped into five visually distinct documents.")
