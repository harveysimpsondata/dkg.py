import fitz  # PyMuPDF
import base64
import os

filename = os.path.join(os.path.dirname(__file__), '..', 'pdfs', 'Verifiable_Internet_for_Artificial_Intelligence_whitepaper.pdf')
doc = fitz.open(filename)


# Create a directory to save the images
output_dir = "/Users/leesimpson/Desktop/extracted_images"
os.makedirs(output_dir, exist_ok=True)

base64_images = []
image_files = []

for i, page in enumerate(doc):
    for image_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_format = base_image["ext"]
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        base64_images.append((encoded_image, image_format))

        # Decode the base64 string back to bytes
        decoded_image_bytes = base64.b64decode(encoded_image)

        # Save the bytes back to an image file
        output_image_filename = f'image_{i}_{image_index}.{image_format}'
        output_image_path = os.path.join(output_dir, output_image_filename)
        with open(output_image_path, 'wb') as image_file:
            image_file.write(decoded_image_bytes)

        image_files.append(output_image_path)

if image_files:
    print(f"All images have been extracted and saved in the directory: {output_dir}")
    print("Please check each file to confirm the integrity of the images.")
else:
    print("No images were found in the document.")
