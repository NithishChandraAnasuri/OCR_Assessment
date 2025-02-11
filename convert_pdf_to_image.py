from pdf2image import convert_from_path

# Path to your PDF file
pdf_path = r"D:\Projects\oaksol\assessment_form.pdf"  # Change to your file path
output_folder = r"D:\Projects\oaksol\form_sample"  # Save images in the same folder

# Convert PDF to images
images = convert_from_path(pdf_path)

# Save first page as an image
image_path = f"{output_folder}form_sample.jpg"
images[0].save(image_path, "JPEG")
print(f"✅ Image saved as: {image_path}")
