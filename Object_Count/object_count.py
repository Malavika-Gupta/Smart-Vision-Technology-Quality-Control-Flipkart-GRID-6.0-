import cv2
import numpy as np

# Load the image
image = cv2.imread('Object_Count/image.jpg')

# Check if the image loaded successfully
if image is None:
    print("Error: Could not load image.")
    exit()

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply GaussianBlur to reduce noise
blurred = cv2.GaussianBlur(gray, (11, 11), 0)

# Apply adaptive thresholding to create a binary image
thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY_INV, 11, 2)

# Find contours in the thresholded image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours based on area to count objects of interest (apples)
min_contour_area = 1000  # Adjust based on image scale
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]

# Draw contours around detected apples
cv2.drawContours(image, filtered_contours, -1, (0, 255, 0), 3)

# Display the number of apples detected
print(f'Number of apples found: {len(filtered_contours)}')

# Show the resulting images
cv2.imshow('Threshold', thresh)
cv2.imshow('Detected Apples', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
