import easyocr
import cv2
import re

# Path to your car image
IMAGE_PATH = "car.jpg"
# Read the image
image = cv2.imread(IMAGE_PATH)
if image is None:
    print("Image not found at the path!")
    exit()

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

# Perform OCR
results = reader.readtext(IMAGE_PATH)

# Regex pattern for Indian number plates (adjust if needed)
plate_pattern = r"[A-Z]{2}[0-9]{1,2}[A-Z]{1,2}[0-9]{1,4}"

detected_plate = None

for (bbox, text, prob) in results:
    text = text.replace(" ", "").upper()  # Remove spaces and uppercase
    if re.fullmatch(plate_pattern, text):
        detected_plate = text
        # Draw rectangle around detected plate
        (top_left, top_right, bottom_right, bottom_left) = bbox
        top_left = tuple([int(val) for val in top_left])
        bottom_right = tuple([int(val) for val in bottom_right])
        cv2.rectangle(image, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(image, text, (top_left[0], top_left[1]-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        print(f"Detected Number Plate: {text}, Confidence: {prob:.2f}")
        break  # Stop after first probable plate

if detected_plate:
    cv2.imshow("Number Plate Detected", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    OUTPUT_PATH = "car_plate_detected.jpg"
    cv2.imwrite(OUTPUT_PATH, image)
    print(f"Output image saved at {OUTPUT_PATH}")
else:
    print("No number plate detected")

