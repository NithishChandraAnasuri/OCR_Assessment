Certainly! Here is the `README.md` content extracted from the previous chat:

```markdown
# OCR Assessment Project

This project automates the extraction of data from patient assessment forms using Optical Character Recognition (OCR) and stores the structured data in a PostgreSQL database.

## Features

- Extracts text from images using Tesseract OCR.
- Converts extracted text into structured JSON format.
- Stores JSON data in a PostgreSQL database.

## Setup Instructions

### Prerequisites

- Python 3.x
- Tesseract OCR (install from [here](https://github.com/tesseract-ocr/tesseract))
- PostgreSQL (install from [here](https://www.postgresql.org/download/))

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/NithishChandraAnasuri/OCR_Assessment.git
   cd OCR_Assessment
   ```

2. Install the required Python packages:
   ```bash
   pip install pytesseract opencv-python psycopg2
   ```

3. Set up the PostgreSQL database:
   ```sql
   CREATE DATABASE intern_db;


   CREATE TABLE patients (
       id SERIAL PRIMARY KEY,
       name VARCHAR(255),
       dob DATE
   );

   CREATE TABLE forms_data (
       id SERIAL PRIMARY KEY,
       patient_id INT REFERENCES patients(id),
       form_json JSONB,
       created_at TIMESTAMP DEFAULT NOW()
   );
   ```

### Usage

1. Place your patient assessment form image in the project directory.
2. Update the `image_path` variable in the `ocr_extractor.py` script with the path to your image.
3. Run the script:
   ```bash
   python ocr_extractor.py
   ```

### Sample Output

The script will output the extracted JSON data and confirm that it has been stored in the database.


