import cv2
import numpy as np
import fitz
import matplotlib.pyplot as plt


input_pdf: str = r"Sample2.pdf"


def rotate(img, angle):
    rows,cols, _ = img.shape
    M = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
    dst = cv2.warpAffine(img,M,(cols,rows))
    return dst


def rotate_all_pages_upright(input_pdf: str):
    """
    Analyze all pages in the input PDF and determine the rotation angle needed for each page.

    Args:
    input_pdf (str): The file path of the input PDF.

    Returns:
    List[int]: A list of rotation angles (in degrees) for each page.
               The angles are normalized to be in the range [0, 359].
               0 means no rotation needed, 90 means 90 degrees clockwise, etc.
    """
    # reader = PdfReader(input_pdf)
    # writer = PdfWriter()
    doc = fitz.open(input_pdf)

    angles = []
    for i, page in enumerate(doc):
        print("page number ", i+1)
        # current_page = reader.pages[page_number]
        pix = page.get_pixmap()
        # Convert the pixmap to an OpenCV image format (numpy array)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)  # 3 is the number of channels
        # Converting image to RGB (OpenCV uses BGR by default)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        rotation_angle = determine_rotation_angle(img)
        angles.append(rotation_angle)

    return angles


def determine_rotation_angle(image_og):
    """
    Determine the rotation angle needed to make the page upright.

    Args:
    page (PdfReader.PageObject): A single page from a PDF.

    Returns:
    int:  The rotation angle in degrees (e.g. 0, 90, 210).
          The rotation angle is  normalized to be in the range [0, 359].
          0 means the page is already upright, 90 means 90 degrees clockwise, etc.
    """
    # TODO: Implement the logic to determine the rotation angle of the pdf pag
    image = cv2.cvtColor(image_og, cv2.COLOR_BGR2GRAY)
    image_bin = cv2.threshold(image, 60, 255, cv2.THRESH_BINARY_INV)[1]
    # Apply adaptive thresholding
    image_bin = cv2.adaptiveThreshold(image_bin, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Apply dilation and erosion to enhance text
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    dilated = cv2.dilate(image_bin, kernel, iterations=1)
    image_bin = cv2.erode(dilated, kernel, iterations=1)
    cv2.imshow('image_bin', image_bin)
    # Find contours in the image
    contours, _ = cv2.findContours(image_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_rect = None
    max_length = 0
    angle = 0
    for i, contour in enumerate(contours):
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.intp(box)
        cv2.polylines(image_og, [box], isClosed=True, color=(0, 255, 0), thickness=2)
        _, (w, h), _ = rect
        length = max(w, h)
        width = min(w, h)
        if length > max_length:
            if width < length/2:
                max_length = length
                max_rect = rect


    # Extract the angle of the longest side
    if max_rect is not None:
        _, _, angle = max_rect

    # Correct the angle (angle of rotated rectangle returned by minAreaRect can be negative)
    if angle < -45:
        angle = 90 + angle
    # image_og = rotate(image_og, 360 - angle)

    height, width, _ = image_og.shape
    y = height // 2  # Position the line in the middle of the image
    cv2.line(image_og, (0, y), (width, y), color=(255, 0, 0), thickness=2)
    cv2.imshow("Original", image_og)
    cv2.waitKey(0)
    return angle


rotation_angles = rotate_all_pages_upright(input_pdf)
