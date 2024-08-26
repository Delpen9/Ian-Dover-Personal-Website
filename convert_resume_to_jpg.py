from pdf2image import convert_from_path
import os


def pdf_to_jpg(pdf_path, output_folder):
    pdf_filename_without_extension = pdf_path.split("/")[-1].replace(".pdf", "")

    # Convert PDF to a list of PIL images, one per page
    images = convert_from_path(pdf_path)

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save each page as a JPEG image
    for i, image in enumerate(images):
        output_path = os.path.join(
            output_folder, f"{pdf_filename_without_extension}_page_{i + 1}.jpg"
        )
        image.save(output_path, "JPEG")
        print(f"Saved {output_path}")


if __name__ == "__main__":
    pdf_path = "myportfolio/static/content/resume/Ian_Dover_Resume.pdf"
    output_folder = "myportfolio/static/content/resume/"
    pdf_to_jpg(pdf_path, output_folder)
