

from pdfwordsearch.scan.pdf_scan import pdf_to_dict


def test_pdf_scan():
    with open('../resources/lovely.pdf', 'rb') as pdf:
        actual = pdf_to_dict(pdf)
        assert actual == {}

