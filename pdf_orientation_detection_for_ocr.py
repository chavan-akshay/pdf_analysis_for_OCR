import cv2
import numpy as np
import fitz
from typing import List, Tuple
from PIL import Image


def rotate(img, angle):
    rows, cols = img.shape[:2]
    matrix = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    dst = cv2.warpAffine(img, matrix, (cols, rows))
    return dst


def calculate_zebra_pattern_score(image):
    row_sums = np.sum(image, axis=1)
    zebra_score = np.var(row_sums)
    return zebra_score


def rotate_all_pages_upright(input_pdf: str) -> List[int]:
    """
    Analyze all pages in the input PDF and determine the rotation angle needed for each page.

    Args:
    input_pdf (str): The file path of the input PDF.

    Returns:
    A list of rotation angles (in degrees) for each page.
               The angles are normalized to be in the range [0, 359].
               0 means no rotation needed, 90 means 90 degrees clockwise, etc.
    """
    doc = fitz.open(input_pdf)

    angles = []
    rotated_images = []
    for page in doc:
        pix = page.get_pixmap()

        # Convert the pixmap to an OpenCV image format (numpy array)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)  # 3 is the number of channels

        rotation_angle, rotated_image = determine_rotation_angle(img)
        angles.append(rotation_angle)
        rotated_images.append(Image.fromarray(rotated_image))
        rotated_images[0].save('grouped_documents_rotated.pdf', save_all=True, append_images=rotated_images[1:])

    return angles


def determine_rotation_angle(image_og: np.ndarray) -> Tuple[int, np.ndarray]:
    """
    Determine the rotation angle needed to make the page upright. To achieve this
    we compare the processed image to exhibit a clear pattern of alternating
    light and dark rows i.e. "Zebra Pattern".
    By this method we are able to achieve the rotation angle.

    Args:
    page (PdfReader.PageObject): A single page from a PDF.

    Returns:
    int:  The rotation angle in degrees (e.g. 0, 90, 210).
          The rotation angle is  normalized to be in the range [0, 359].
          0 means the page is already upright, 90 means 90 degrees clockwise, etc.
    """
    # TODO: Implement the logic to determine the rotation angle of the pdf pag
    image = cv2.cvtColor(image_og, cv2.COLOR_RGB2GRAY)
    image_bin = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Edge detection
    image_bin = cv2.Canny(image_bin, 50, 150)

    # Apply dilation and erosion to enhance text
    kernel = np.ones((3, 3), np.uint8)
    image_bin = cv2.dilate(image_bin, kernel, iterations=1)
    image_bin = cv2.erode(image_bin, kernel, iterations=2)

    # Rotate the image around in a circle
    best_angle = 0
    best_score = float('-inf')
    angle = 0
    while angle < 360:
        # Rotate the source image
        img = rotate(image_bin, angle)

        score = calculate_zebra_pattern_score(img)

        # High score --> Zebra stripes
        if score > best_score:
            best_score = score
            best_angle = angle

        # Increment angle
        angle += 1
    cv2.destroyAllWindows()
    # best_angle = 360 - best_angle
    rotated_image = rotate(image_og, best_angle)
    return best_angle, rotated_image


input_pdf: str = r"grouped_documents.pdf"
rotation_angles: List[float] = rotate_all_pages_upright(input_pdf)
print(f"Rotation angles for each page: {rotation_angles}")
