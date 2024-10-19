import cv2
import numpy as np
from PIL import Image
import pytesseract

# Load the image from file
image = cv2.imread('label_image_sample.jpeg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur to remove noise
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply Otsu's thresholding to binarize the image
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Rotate the image to deskew text (if necessary)
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]
if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle

# Rotate the image back to align the text
(h, w) = thresh.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(thresh, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# Save the preprocessed image for checking
cv2.imwrite('preprocessed_label_image.jpg', rotated)

# Perform OCR using pytesseract
text = pytesseract.image_to_string(Image.open('preprocessed_label_image.jpg'))

# Print the extracted text
print("Extracted Text:\n", text)

# Example of cleaning the text to extract specific information
import re

# Extract brand (assuming the text has "Brand: XYZ")
brand_match = re.search(r'Brand:\s*([A-Za-z]+)', text)
if brand_match:
    brand = brand_match.group(1)
    print("Brand:", brand)

# Extract size (assuming the text has "Size: 250ml")
size_match = re.search(r'Size:\s*(\d+ml)', text)
if size_match:
    size = size_match.group(1)
    print("Size:", size)
