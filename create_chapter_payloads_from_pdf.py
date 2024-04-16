from typing import Dict, Union
from pypdf import PdfReader
import json
import pprint
import os
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')


def bookmark_dict(
    bookmark_list, reader: PdfReader, use_labels: bool = False,
) -> Dict[Union[str, int], str]:
    """
    Extract all bookmarks as a flat dictionary.

    Args:
        bookmark_list: The reader. outline or a recursive call
        use_labels: If true, use page labels. If False, use page indices.

    Returns:
        A dictionary mapping page labels (or page indices) to their title

    Examples:
        Download the PDF from https://zenodo.org/record/50395 to give it a try
    """
    result = {}
    for item in bookmark_list:
        if isinstance(item, list):
            # recursive call
            result.update(bookmark_dict(item, reader))
        else:
            page_index = reader.get_destination_page_number(item)
            page_label = reader.page_labels[page_index]
            if use_labels:
                result[page_label] = item.title
            else:
                result[page_index] = item.title
    return result


def array_to_json_file(array, file_name):
    """
    Saves a list of dictionaries to a JSON file.
    """
    try:
        with open(file_name, 'w', encoding='utf-8') as json_file:
            json.dump(array, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Error saving JSON: {e}")


def construct_page_splits_array(reader, bms):
    last_page = len(reader.pages)
    split_at_list = list(bms.keys())
    split_at_list.append(last_page)
    return split_at_list


def construct_start_and_end_arrays(split_at_pages):
    start = 0
    end = 0
    splits = []
    for i in range(len(split_at_pages)):
        if i == 0:
            start = 1
            end = split_at_pages[i]
        else:
            start = split_at_pages[i - 1]
            end = split_at_pages[i]
        print(f"Start: {start}, End: {end}")
        splits.append((start, end))
    return splits


def get_chapter(split, reader, bms):
    content = []
    # print(split)
    start, end = split
    # print(start, end)
    t = type(start)
    name = bms.get(start, '')
    print(f'Search for {start} as type {t} and found {name}')

    for page_nb in range(int(start), int(end)):
        page_text = reader.pages[page_nb].extract_text()
        content.append(page_text)
    chapter_content = ''.join(content)
    return {
        'name': name,
        'contents': chapter_content,
        'type_of_name': t.__name__  # keep .__name__ this here
    }


def get_chapter_name_from_contents(contents):
    first_part = contents[0:1000]
    print(first_part)
    pass


def count_words(text):
    return len(text.split(' '))


# get all files in a directory
def get_files_in_directory(directory):
    files = os.listdir(directory)
    return files


def extract_pdf_chapters(book_name, pdf_file_path):
    # book_name = '1626813582'

    reader = PdfReader(pdf_file_path)
    bms = bookmark_dict(reader.outline, reader, use_labels=True)
    print(bms.keys())
    print(bms.values())

    for page_nb, title in sorted(bms.items(), key=lambda n: f"{str(n[0]):>5}"):
        print(f"{page_nb:>3}: {title}")
        pass

    sequence = construct_page_splits_array(reader, bms)
    splits = construct_start_and_end_arrays(sequence)
    splits_excluding_first = splits[1:]

    chapters = []
    for index, split in enumerate(splits_excluding_first):
        chapter = get_chapter(split, reader, bms)
        chapter['sequence_index'] = index
        chapter['part'] = ''
        chapters.append(chapter)

    return chapters


def exclude_fluff_from_request_bodies(json_data):
        """
        request_bodies = {
                    "isbn_ten": isbn_ten,
                    "name": chapter_name,
                    "sequence_index": index,
                    "contents": contents,
                    "part": chapter_part,
                }
        """
        # given a list of request bodies, exclude the ones that are too small or have keywords
        exclude_keywords = [
            "acknowledgement",
            "acknowledgment",
            "reference",
            "appendix",
            "bibliography",
            "glossary",
            "copyright",
            "author's note",
            "note on",
            "publisher's note",
            "about the author",
            "list of collaborators",
            "notes",
            "praise for",
            "praise",
            "thanks",
            "cover",
            "index",
            "resources",
            "sources",
            "table of contents",
            "title page",
            "penguin books",
            "further readings",
            "illustration credits",
            "photo insert",
            "about the publisher",
            "author"
        ]
        exclude_indices = []
        for index, request_body in enumerate(json_data):
            try:
                chapter_contents = request_body["contents"]

                if "chapter" in request_body["name"].lower():
                    print(
                        "CHAPTER DOES NOT NEED TO BE FILTERED: ", request_body["name"]
                    )
                    continue
                # Exclude chapters with exclusionary keywords
                if any(
                    [
                        keyword in request_body["name"].lower()
                        for keyword in exclude_keywords
                    ]
                ):
                    exclude_indices.append(index)
                    print("\tEXCLUDED CHAPTER - KEYWORDS FLUFF", request_body["name"])
                    continue
                # Exclude if chapters not big enough
                if count_words(chapter_contents) < 1000:
                    exclude_indices.append(index)
                    print(
                        "\tEXCLUDED CHAPTER - TOO SMALL",
                        request_body["name"],
                        count_words(chapter_contents),
                        " characters",
                    )
                    continue
                else:
                    print(
                        "CHAPTER DOES NOT NEED TO BE FILTERED: ", request_body["name"]
                    )
            except:
                print("something went wrong in chapter fluff filtering")
        try:
            included_request_bodies = [
                request_body
                for index, request_body in enumerate(json_data)
                if index not in exclude_indices
            ]
            print("\nCHAPTERS INCLUDED: ")
            for request_body in included_request_bodies:
                print(request_body["name"])
            filtered_request_bodies = included_request_bodies
            return filtered_request_bodies
        except Exception as e:
            print("Failed to exclude fluff from request bodies")
            return None
        
def analyze_raw_extraction(data):
    chapter_count = len(data)
    total_word_count = 0

    for index, chapter in enumerate(data):
        words = count_words(chapter['contents'])
        print(f"{chapter['name']} has {words} words")
        total_word_count += words

    filtered_data = exclude_fluff_from_request_bodies(data)
    number_of_excluded_chapters = chapter_count - len(filtered_data)

    filtered_total_word_count = 0
    filtered_chapters_with_count = ''
    for index, chapter in enumerate(filtered_data):
        words = count_words(chapter['contents'])
        # print(f"{chapter['name']} has {words} words")
        filtered_total_word_count += words
        filtered_chapters_with_count += f"{chapter['name']} -- {words} words\n"

    return {
        'chapter_count': chapter_count,
        'total_word_count': total_word_count,
        "number_of_excluded_chapters": number_of_excluded_chapters,
        "filtered_chapter_count": len(filtered_data),
        "filtered_total_word_count": filtered_total_word_count,
        "filtered_chapters_with_count": filtered_chapters_with_count
    }


def is_pdf(file):
    return file.endswith('.pdf')


def propagate_name_to_part(arr):
    propagate_name = None
    for i, obj in enumerate(arr):
        # If contents are blank and no name is currently being propagated, start propagation
        if obj["contents"] == "" and propagate_name is None:
            propagate_name = obj["name"]
        # If contents are blank and a name is being propagated, stop propagation before updating this object
        elif obj["contents"] == "" and propagate_name is not None:
            propagate_name = obj["name"]  # We've encountered another empty "contents", reset the name
        # Propagate the name to the part key if needed
        elif propagate_name is not None and obj["type_of_name"] == "int":
            arr[i]["part"] = propagate_name
    return arr


def remove_empty_chapters(arr):
    return [obj for obj in arr if obj["contents"] != ""]


def re_sequence_chapters(arr):
    for i, obj in enumerate(arr):
        arr[i]["sequence_index"] = i
    return arr

def inject_isbn_to_chapters(arr, isbn):
    for i, obj in enumerate(arr):
        arr[i]["isbn"] = isbn
    return arr


def remove_type_of_name_helper(arr):
    for i, obj in enumerate(arr):
        arr[i].pop("type_of_name", None)
    return arr

def process_pdf(pdf_file_path, output_directory=None):
    """
        Main function to process the PDF file, extract chapters based on bookmarks,
        and save the extracted chapters as a JSON file after applying various transformations.
        """
    try:
        book_name = os.path.basename(pdf_file_path).split('.')[0]
        logging.info(f"Processing PDF: {pdf_file_path}")

        chapters = extract_pdf_chapters(book_name, pdf_file_path)

        filter_chapters = exclude_fluff_from_request_bodies(chapters)
        chapters_with_part_info = propagate_name_to_part(filter_chapters)
        chapters_without_empty = remove_empty_chapters(chapters_with_part_info)
        chapters_resequenced = re_sequence_chapters(chapters_without_empty)
        chapters_with_isbn = inject_isbn_to_chapters(chapters_resequenced, book_name)
        chapters_without_type_of_name = remove_type_of_name_helper(chapters_with_isbn)

        results = analyze_raw_extraction(chapters)
        pprint.pprint(results)

        if chapters_without_type_of_name:
            output_file_path = os.path.join(output_directory, f"{book_name}_autosplits.json")
            array_to_json_file(chapters_without_type_of_name, output_file_path)
            logging.info(f"Data saved to {output_file_path}")
        else:
            logging.error("No chapters were processed.")
    except Exception as e:
        logging.error(f"Error processing {pdf_file_path}: {e}")


def get_chapter_payloads_from_pdf(isbn, pdf_file_path):
    """
    Extract and process chapters from PDF specified by its ISBN and file path,
    returning the chapters data after transformations.
    """
    try:
        logging.info(f"Extracting chapters from PDF: {pdf_file_path} with ISBN: {isbn}")
        chapters = extract_pdf_chapters(isbn, pdf_file_path)

        filter_chapters = exclude_fluff_from_request_bodies(chapters)
        chapters_with_part_info = propagate_name_to_part(filter_chapters)
        chapters_without_empty = remove_empty_chapters(chapters_with_part_info)
        chapters_resequenced = re_sequence_chapters(chapters_without_empty)
        chapters_with_isbn = inject_isbn_to_chapters(chapters_resequenced, isbn)
        chapters_without_type_of_name = remove_type_of_name_helper(chapters_with_isbn)

        logging.info(f"Processed {len(chapters_without_type_of_name)} chapters.")
        return chapters_without_type_of_name
    except Exception as e:
        logging.error(f"Failed processing PDF {pdf_file_path} with ISBN {isbn}: {e}")
        raise e


if __name__ == "__main__":
    isbn = '9354990517'
    pdf_path = f'data/{isbn}.pdf'
    data_path = 'data'
    process_pdf(pdf_path, data_path)