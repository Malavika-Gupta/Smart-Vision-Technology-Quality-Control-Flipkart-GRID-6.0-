import easyocr
import cv2
import re

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

def capture_image_from_camera():
    # Open the camera (0 refers to the default camera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return None

    # Capture a single frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not capture image.")
        return None

    # Release the camera
    cap.release()

    # Display the captured image
    cv2.imshow('Captured Image', frame)
    cv2.waitKey(1000)  # Wait for 1 second (adjust as needed)

    # Save the captured image to a file
    image_path = 'captured_image.jpg'
    cv2.imwrite(image_path, frame)

    # Close all OpenCV windows
    cv2.destroyAllWindows()

    return image_path

def extract_text_from_image(image_path):
    results = reader.readtext(image_path)
    
    # Join all detected text
    text = ' '.join([result[1] for result in results])
    return text

def find_expiry_date(text):
    date_pattern = r'\b(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}-\d{1,2}-\d{2,4})\b'
    matches = re.findall(date_pattern, text)
    
    if matches:
        return matches
    return "No expiry date found"

# Capture image from the camera
image_path = capture_image_from_camera()

if image_path:
    # Extract text from the captured image
    text = extract_text_from_image(image_path)
    print("Extracted Text:", text)

    # Find and print the expiry date
    expiry_dates = find_expiry_date(text)
    print("Expiry Dates Found:", expiry_dates)
