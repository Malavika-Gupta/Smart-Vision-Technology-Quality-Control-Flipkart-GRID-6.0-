import cv2
import numpy as np
from PIL import Image
import pytesseract

# Load image
image = cv2.imread('label_image.jpg')

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply noise reduction
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# Apply thresholding to convert the image to binary
_, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Detect and correct skew (if any)
coords = np.column_stack(np.where(thresh > 0))
angle = cv2.minAreaRect(coords)[-1]
if angle < -45:
    angle = -(90 + angle)
else:
    angle = -angle

(h, w) = gray.shape[:2]
center = (w // 2, h // 2)
M = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(thresh, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

# Save the preprocessed image and use it for OCR
cv2.imwrite('preprocessed_label_image.jpg', rotated)
