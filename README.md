# book-extractor

### Goal
This is an open-source repository to expose common utilities to extract text from books. Any one is welcome to fork or contribute to the code, and it is intended for use with LLMS.

### Setup
1.  [Poetry](https://python-poetry.org/docs/) for dependency management. Make sure you have Poetry installed. If you need to install Poetry, run:
    ```
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
    ```
    ```
    poetry --version
    ```
2.  Python 3.9.2 
    ```
    pyenv local 3.9.2
    python3 -V
    ```
3. Installing Dependencies:
    To install the project dependencies, navigate to the project's root directory and run:
    ```
    poetry install
    ```

### Running Scripts:
Running Scripts within the Poetry environment, use:
```
poetry run python create_chapter_payloads_from_pdf.py
```

### Adding Dependencies:
To add new dependencies to the project, use
```
poetry add <package-name>.
```

## Colab Notebooks
This notebook converts an **EPUB File to a PDF File** using Convert API Key.
- [EPUB to a PDF Notebook](https://colab.research.google.com/drive/1EvtOHveT4xUbjqanoD0ilu-DiH_Z2dRC?usp=sharing)

This notebook performs **Chapter Extraction**, generating a structured JSON file with the contents of each chapter.
- [Chapter Extraction Notebook](https://colab.research.google.com/drive/1c6yoJn7mwAYNFqIsPhXdiAnSCB8bc0me?usp=sharing)
