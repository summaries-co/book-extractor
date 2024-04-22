import os
import logging
from PyPDF2 import PdfReader, PdfWriter

# Configure logging to capture important information and errors
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_output_folder(isbn):
    """
    Creates a directory for saving individual PDF page files. The folder is named based on the ISBN.

    Args:
        isbn (str): The ISBN number which is used to name the folder.

    Returns:
        str: The path of the created output folder.
    """
    output_folder = f"{data_path}/{isbn}_pages"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    return output_folder


def save_page_as_pdf(page, output_filename):
    """
    Saves a single PDF page to a file.

    Args:
        page (PageObject): A single page from a PDF file.
        output_filename (str): Full path where the PDF page will be saved.
    """
    writer = PdfWriter()
    writer.add_page(page)
    with open(output_filename, 'wb') as output_pdf:
        writer.write(output_pdf)


def split_pdf_into_pages(pdf_path):
    """
    Splits a given PDF file into individual pages and saves each as a separate PDF file.

    Args:
        pdf_path (str): The path to the PDF file to be processed.
    """
    isbn = os.path.basename(pdf_path).split('.')[0]
    output_folder = create_output_folder(isbn)

    reader = PdfReader(pdf_path)
    number_of_pages = len(reader.pages)

    for page_number in range(number_of_pages):
        output_filename = os.path.join(output_folder, f"{isbn}_{page_number + 1}.pdf")
        save_page_as_pdf(reader.pages[page_number], output_filename)

        logging.info(f"Page {page_number + 1}/{number_of_pages} saved to {output_filename}")


def create_individual_pdf_pages(pdf_file_path):
    """
    Processes a PDF file by reading it, splitting into pages, and saving those pages as individual PDF files.
    This is the main driver function that utilizes other functions to decompose a PDF into its constituent pages.

    Args:
        pdf_file_path (str): The path to the PDF file to be processed.
    """
    try:
        split_pdf_into_pages(pdf_file_path)
        logging.info("PDF has been split and individual pages have been saved successfully.")
    except Exception as e:
        logging.error(f"Error during PDF page splitting: {e}")


if __name__ == "__main__":
    # Set the ISBN of your PDF file here. Ensure the file is named in the format '{ISBN}.pdf'.
    # Adjust 'data_path' to the directory where your PDF file is located.
    # The script will create a folder with individual PDFs for each page of the specified document.
    isbn = '9354990517'
    data_path = 'data'
    pdf_path = f'{data_path}/{isbn}.pdf'
    create_individual_pdf_pages(pdf_path)

