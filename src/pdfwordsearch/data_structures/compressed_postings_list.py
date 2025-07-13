from typing import Iterator, Dict, Tuple, Optional

from pdfwordsearch.data_structures.abstract_postings_list import AbstractPostingsList
from pdfwordsearch.data_structures.vint import VIntWriter, VIntReader
import pymupdf
import json
import re
import string
from pymupdf import Document

class CompressedPostingsList(AbstractPostingsList):
    def __init__(self, info: Optional[dict] = None):
        self.postings_list: Dict[str, bytearray] = dict()
        self.docid_prev: Dict[str, int] = dict()
        super().__init__(info)

    def get_words(self) -> Iterator[str]:
        """

        Returns an iterator over the words in the compressed postings list.
        -------

        """
        return iter(self.postings_list.keys())

    def _add_word(self, word: str, word_count: int, docid: int):
        """
        Add word, word count and docid to postings list.
        Note: The word and docid should be unique. Meaning all occurences of the word should be counted before being
        added to the postings list.

        Parameters
        ----------
        word : word to add to the postings list
        word_count : occurences of the word
        docid : document id where word is found

        Returns None
        -------

        """
        if word not in self.postings_list:
            self.postings_list[word] = bytearray()
            self.docid_prev[word] = 0

        VIntWriter.write(self.postings_list[word], word_count)
        VIntWriter.write(self.postings_list[word], docid - self.docid_prev[word])
        self.docid_prev[word] = docid

    def get_locations(self, word: str) -> Iterator[Tuple[int, int]]:
        """

        Parameters
        ----------
        word : word to get the locations for

        Returns an iterator over the word_count and docids of the word
        -------

        """
        docid_prev = 0
        if word not in self.postings_list:
            yield from ()
            return

        results = VIntReader.read(self.postings_list[word])
        while (word_count := next(results, None)) is not None:
            delta_docid = next(results)

            docid = delta_docid + docid_prev
            docid_prev = docid
            yield word_count, docid

    @classmethod
    def pdf_convert_to_abl(cls, file_position: str, encode: str = "utf8", save: Optional[str] = None, scan_param: Dict = {}):
            """
            Convert a pdf file to an AbstractPostingsList
            Parameters
            ----------
            file_position : str
                Location of the pdf file
            encode : str
                Encoding method of the pdf
            save : Optional[str]
                Save to the given location, not save if pass in as None
            scan_param : Dict
                Parameter options for the pdfInfo Get.

            Returns
            -------
            An instance of AbstractPostingsList containing the words and their counts.
            """
            instance = cls()

            def pdf_info_get(file_path = None, ignore_page = None, encode="utf8", save = None, file_stream = None, file: Document = None):
                """  
                get the information from pdf (table and image not implement yet) and 
                    export as dictionary. 
                filePath: string => readFile from this location
                ignore: list(...int...) => page to ignore
                encode: str => page encoding method 
                save: str | None => save read into json. 
                """
                store = {}

                if ignore_page is None:
                    ignore_page = []


                if file_path:
                    doc = pymupdf.open(file_path)
                elif file_stream:
                    doc = pymupdf.Document(stream=file_path)
                elif file:
                    doc = file
                else:
                    raise ValueError("Either file_path, file_stream or file must be provided")

                i = 0
                for page in doc:
                    if page not in ignore_page:
                        txt = page.get_text("dict")
                        lst = []
                        for block in txt["blocks"]:
                            if "lines" in block:
                                for line in block["lines"]:
                                    aStr = " ".join([span["text"] for span in line["spans"]])
                                    nStr = re.sub(r"[^\w\s]", " ", aStr) # no weird stuff
                                    lst.append(nStr)
                    store[i] = lst
                    i = i + 1
                if save:
                    with open(save, "w", encoding=encode) as f:
                        json.dump(store, f, indent=4)
                return store

            def createPostingListFrompdf(filePosition: str, encode : str = "utf8" , save : str | None = None, scanParam = {}):
                """ 
                CreatePostingListFromPdf: creating a posting list from the pdf
                filePostion: str => location of the file
                encoode: str => encoding method of the pdf
                save: str | None => save to the given location, not save if pass in as None
                scanParam: dic => parameter option for the pdfInfo Get. 
                
                """
                df = pdf_info_get(filePosition, **scanParam)
                store = {}
                for key, val in df.items():
                    word_count = {}
                    for sentence in val:
                        translator = str.maketrans('', '', string.punctuation)
                        words = sentence.translate(translator).split()
                        for word in words:
                            w = word.lower() 
                            word_count[w] = word_count.get(w, 0) + 1
                    store[key] = word_count

                for key, val in store.items():
                    docid = key
                    secVal = val
                    for word, count in secVal.items():
                        instance._add_word(word, count, docid)

                if save:
                    with open(save, "w", encoding=encode) as f:
                        json.dump(instance.postings_list, f, indent=4)
            createPostingListFrompdf(file_position, encode, save, scan_param)
            return instance
