import easyocr
from PIL import Image
import re

import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

reader = easyocr.Reader(['en'])  

def extract_text_from_image(image_path):
    image = Image.open('sample.jpeg')
    results = reader.readtext(image_path)
    
    text = ' '.join([result[1] for result in results])
    return text

def find_expiry_date(text):
    date_pattern = r'\b(?:\d{1,2}/\d{1,2}/\d{2,4}|\d{1,2}-\d{1,2}-\d{2,4})\b'
    matches = re.findall(date_pattern, text)
    
    if matches:
        return matches
    return "No expiry date found"

image_path = 'sample.jpeg'

# Extract text from the image
text = extract_text_from_image(image_path)
print("Extracted Text:", text)

# Find and print the expiry date
expiry_dates = find_expiry_date(text)
print("Expiry Dates Found:", expiry_dates)
