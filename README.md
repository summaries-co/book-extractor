# book-extractor

# Setup
This project utilizes Poetry for dependency management and packaging.

## Prerequisites

### Python 3.9.2
Make sure you have python 3.9.2 running
```
pyenv local 3.9.2
python3 -V
```


- [Poetry](https://python-poetry.org/docs/)

Make sure you have Poetry installed. If you need to install Poetry, run:
```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

To verify that Poetry is installed correctly, run:
```
poetry --version
```

### Installing Dependencies:
To install the project dependencies, navigate to the project's root directory and run:
```
poetry install
```

### Activating/Exiting the Poetry Shell Environment:
```
poetry shell
```

```
exit
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

This notebook performs **Chapter Extraction**, generating a structured JSON file with the contents of each chapter.
- [Chapter Extraction Notebook](https://colab.research.google.com/drive/1c6yoJn7mwAYNFqIsPhXdiAnSCB8bc0me?usp=sharing#scrollTo=WIQN6rMj5iKV)

This notebook creates a **30-minute Summary** from raw chapter text using OpenAI's API.
- [Thirty-minute Summary Notebook](https://colab.research.google.com/drive/1kMwwJ2VKhjh7-MFB49fSK3o8TGgmrYLm?usp=sharing#scrollTo=E6bObSuDlfnI)

This notebook generates **Key Takeaways** summary for each chapter of a book using OpenAI's API
- [Key Takeaways Notebook](https://colab.research.google.com/drive/1h-v53KFcFiDl3wpt_SnXqaCDoZWotyK7?usp=sharing#scrollTo=xTPWB-BkmDUC)

This notebook converts an **EPUB File to a PDF File** using Convert API Key.
- [EPUB to a PDF Notebook](https://colab.research.google.com/drive/1EvtOHveT4xUbjqanoD0ilu-DiH_Z2dRC?usp=sharing#scrollTo=M5l8w5jzcDFG)

This notebook creates a **One-Pager Summary** from an ISBN using OpenAI's API.
- [One Pager Summary Notebook](https://colab.research.google.com/drive/18X6H0N-yhz7cVZVUVvlNLNTYg7d-WXC1?usp=sharing#scrollTo=cU88K8HFjq7z)
