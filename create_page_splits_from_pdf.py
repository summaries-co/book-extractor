import re
import json
import os
import logging
from pypdf import PdfReader

# Set up basic configuration for logging to capture important messages and errors.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def clean_contents(contents):
    """
    Strips the given content string of leading and trailing whitespace.

    Args:
        contents (str): The content string to be cleaned.

    Returns:
        str: The cleaned content string.
    """
    return contents.strip() if contents else ''


def count_words(text):
    """
    Counts the number of words in the given text using a regular expression that matches word boundaries.

    Args:
        text (str): The text in which to count words.

    Returns:
        int: The number of words found in the text.
    """
    return len(re.findall(r'\b\w+\b', text))


def extract_page_data(page, isbn):
    """
    Extracts metadata from a single PDF page.

    Args:
        page (PageObject): A PyPDF2 PageObject from which to extract data.
        isbn (str): The ISBN number of the PDF document.

    Returns:
        dict: A dictionary containing metadata of the PDF page.
    """
    contents = clean_contents(page.extract_text())
    contains_images = bool(page.images)  # Converts list to a boolean, True if images are present, otherwise False.
    return {
        "isbn": isbn,
        "page_number": page.page_number + 1,  # Adding 1 to make the page number human-readable (1-indexed).
        "contents": contents,
        "contains_images": contains_images,
        "word_count": count_words(contents)
    }


def read_pdf_and_extract_data(pdf_path, isbn):
    """
    Reads a PDF file and extracts metadata for each page.

    Args:
        pdf_path (str): The file path to the PDF.
        isbn (str): The ISBN number of the PDF document.

    Returns:
        list: A list of dictionaries, each containing metadata for a single page.
    """
    try:
        reader = PdfReader(pdf_path)
        return [extract_page_data(page, isbn) for page in reader.pages]
    except Exception as e:
        logging.error(f"Failed to read or process PDF {pdf_path}: {e}")
        return []  # Return an empty list in case of failure.


def ensure_directory_exists(directory_path):
    """
    Ensures that the specified directory exists, creating it if necessary.

    Args:
        directory_path (str): The path of the directory to check or create.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        logging.info(f"Created directory: {directory_path}")


def write_json_output(pages_data, isbn, output_directory):
    """
    Writes the extracted page data to a JSON file.

    Args:
        pages_data (list): List of dictionaries containing page data.
        isbn (str): The ISBN number used to name the output file.
        output_directory (str): Directory where the output file will be saved.
    """
    ensure_directory_exists(output_directory)

    output_file_path = os.path.join(output_directory, f"{isbn}_page_metadata.json")

    try:
        with open(output_file_path, "w", encoding="utf-8") as json_file:
            json.dump(pages_data, json_file, ensure_ascii=False, indent=4)
        logging.info(f"Metadata JSON file created at {output_file_path}")
    except Exception as e:
        logging.error(f"Failed to write output JSON file: {e}")


if __name__ == "__main__":
    # This script extracts metadata from each page of the PDF and saves this data to a JSON file.

    # Set the ISBN of the PDF file and ensure the file follows the '{ISBN}.pdf' naming format.
    # Define the directory path where your PDF file is stored.
    isbn = '9354990517'
    data_path = 'data'
    pdf_path = f'{data_path}/{isbn}.pdf'
    try:
        pages_metadata = read_pdf_and_extract_data(pdf_path, isbn)
        write_json_output(pages_metadata, isbn, data_path)
    except Exception as e:
        logging.error(f"An error occurred: {e}")