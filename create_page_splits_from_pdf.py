from pypdf import PdfReader
import pprint
import os
import json

'''
{
    isbn
    page_number
    contents
    contains_images
    word_count
}

'''

def clean_contents(contents):
    cleaned_contents = contents.strip()
    return cleaned_contents

def count_words(text):
    """
    Count words in a string using regular expressions.

    This function utilizes a regular expression (`\b\w+\b`) to count words more accurately than
    simple space-based splitting. It identifies words as sequences of alphanumeric characters
    separated by word boundaries, ensuring accurate word counts in texts with punctuation,
    spaces, or special characters.
    These changes will alter the result, can they be made?
        words = re.findall(r'\b\w+\b', text)
     return len(words)
    """
    return len(text.split(" "))

def read_pdf(pdf_path, isbn):
    pages_array = []
    reader = PdfReader(pdf_path)
    pages = reader.pages

    for page in pages:

        contents = page.extract_text()
        #contents = clean_contents(contents)
        page_number = page.page_number + 1
        contains_images = True if page.images else False
        page_information = {
            "isbn": isbn,
            "page_number": page_number,
            "contents": contents,
            "contains_images": contains_images,
            "word_count": count_words(contents)
        }

        print(contents)
        pages_array.append(page_information)
        
   
    return pages_array
    

def write_output(isbn, output_directory):
    output_file_path = os.path.join(
        output_directory, f"{isbn}_page_autosplits.json"
    )
    return output_file_path

def array_to_json_file(array, file_name):
    """
    Saves a list of dictionaries to a JSON file.
    """
    try:
        with open(file_name, "w", encoding="utf-8") as json_file:
            json.dump(array, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print('error', e)

if __name__ == "__main__":
    isbn = "1626813582"
    pdf_path = f"test_data/{isbn}.pdf"
    pages = read_pdf(pdf_path, isbn)
    output_file_path = write_output(isbn, 'test_data/')
    array_to_json_file(pages, output_file_path)