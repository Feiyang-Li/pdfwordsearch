import pymupdf
import re

from pymupdf import Document


def any_to_pdf(
    file_path=None, file_stream=None, file: Document = None
):
    if file_path:
        return pymupdf.open(file_path)
    elif file_stream:
        return pymupdf.Document(stream=file_path)
    elif file:
        return file
    else:
        raise ValueError("Either file_path, file_stream or file must be provided")


def pdf_to_words(file: Document):
    """
    Converts a pdf file to a list of words page by page
    Parameters
    ----------
    file :

    Returns
    -------

    """
    for page in file:
        words = dict()
        txt = page.get_text()  # type: ignore
        for word in re.split(r"[?.,\s()\[\]]+", txt):
            if word == "":
                continue
            word = word.lower()
            words[word] = words.get(word, 0) + 1
        yield words
