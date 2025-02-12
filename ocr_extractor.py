import pytesseract
import cv2
import json
import re
import psycopg2

# Set path for Tesseract-OCR (Update this path if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#  Function to Extract Text from Image
def extract_text_from_image(image_path):
    try:
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        extracted_text = pytesseract.image_to_string(gray)
        return extracted_text.strip()
    except Exception as e:
        print(" Error extracting text:", e)
        return ""

#  Function to Clean & Convert Extracted Text to JSON
def parse_text_to_json(extracted_text):
    try:
        extracted_text = extracted_text.replace("“", '"').replace("”", '"')  # Fix curly quotes
        extracted_text = extracted_text.replace("\n", " ")  # Remove line breaks

        #  Remove "Format Example:" if present
        extracted_text = re.sub(r'Format Example:\s*', '', extracted_text)

        #  Remove unwanted trailing data (anything after last `}`)
        extracted_text = extracted_text[: extracted_text.rfind("}") + 1]

        json_data = json.loads(extracted_text)  # Convert string to JSON

        return json_data
    except json.JSONDecodeError as e:
        print(" Error parsing JSON:", e)
        return {}

#  Function to Store Data in PostgreSQL Database
def store_in_db(json_data):
    try:
        conn = psycopg2.connect(
            dbname="intern_db",
            user="postgres",
            password="Okiwont",  # 
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO patients (name, dob) VALUES (%s, %s) RETURNING id",
            (json_data.get("patient_name", "Unknown"), json_data.get("dob", "Unknown"))
        )
        patient_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO forms_data (patient_id, form_json) VALUES (%s, %s)",
            (patient_id, json.dumps(json_data))
        )

        conn.commit()
        cur.close()
        conn.close()

        print(" Data stored successfully in the database!")
    except psycopg2.Error as e:
        print(" Database error:", e)

#  Main Execution: Extract, Parse, and Store Data
if __name__ == "__main__":
    image_path = r"D:\Projects\oaksol\form_sample.jpg"  # Update with your actual image path
    extracted_text = extract_text_from_image(image_path)

    print(" Raw Extracted Text:\n", extracted_text)

    if extracted_text:
        json_data = parse_text_to_json(extracted_text)
        print("\n Extracted JSON:\n", json.dumps(json_data, indent=4))

        if json_data:
            store_in_db(json_data)
        else:
            print(" JSON data is empty! Check parse_text_to_json function.")
    else:
        print(" No text extracted! Check if the image path is correct.")
