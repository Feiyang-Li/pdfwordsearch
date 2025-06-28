from typing import Optional, Tuple, List

from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList
from pdfwordsearch.data_structures.compressed_postings_list import CompressedPostingsList
from pdfwordsearch.data_structures.postings_list import PostingsList
from pdfwordsearch.scan.pdf_scan import pdf_info_get
from pdfwordsearch.scan.pdf_to_pl import pdf_to_pl


class GUICoordinator:
    def __init__(self):
        self.postings_list: Optional[AbstractPostingsList] = None
        self.file_path = None
    
    def load_file(self, file_path, unoptimized=False):
        self.file_path = file_path
        pdf_info = pdf_info_get(file_path)
        self.postings_list = pdf_to_pl(pdf_info, PostingsList if unoptimized else CompressedPostingsList)

    def query(self, query: str) -> List[Tuple[int, float]]:
        if self.postings_list is None:
            raise Exception('postings list has not been loaded')

        return self.postings_list.execute_query(query)
