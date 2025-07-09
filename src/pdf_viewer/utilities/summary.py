from pymupdf import Document

ELLIPSIS = "..."

def summary(pdf: Document, page_num: int, max_length: int = 50) -> str:
    """
    Summarizes a page from a PDF.
    Parameters
    ----------
    max_length : number of characters in the summary.
    page_num : page number of the page to summarize
    pdf :

    Returns a summary of the page
    -------

    """
    text: str = pdf[page_num].get_text()

    text = text.strip()
    length_ellipse = len(ELLIPSIS)

    if len(text) > max_length:
        num_chars = max_length - length_ellipse
        if num_chars < 0:
            num_chars = 0
        text = text[:num_chars] + ELLIPSIS

    return text