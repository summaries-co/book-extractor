# book-extractor

# Setup
This project utilizes Poetry for dependency management and packaging.

## Prerequisites

- Python 3.9.2
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


