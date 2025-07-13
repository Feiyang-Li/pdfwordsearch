from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Iterator, Tuple, List, Dict, Optional

from pdfwordsearch.match_score_rank.word_match import word_synonyms
from pdfwordsearch.query.term import tokens_to_terms, Term, NegativeTerm
from pdfwordsearch.query.tokenizer import tokenize
import math
from collections import Counter
import pymupdf
import json
import re
import string

class AbstractPostingsList(ABC):
    def __init__(self, pdf: Optional[Dict[int, List[str]]] = None):
        if pdf is None:
            return
        for key, val in pdf.items():
            words = []
            for v in val:
                words.extend(wd.lower().strip() for wd in v.split())
            word_count = Counter(words)
            for w, count in word_count.items():
                self._add_word(w, count, key)

    @abstractmethod
    def _add_word(self, word: str, word_count: int, docid: int) -> None:
        """
        Words must be added in non-decreasing order.
        Parameters
        ----------
        word : a word found in the document
        word_count : number of words encountered in the document or page
        docid : the id of the document

        Returns
        -------

        """
        raise NotImplementedError()

    @abstractmethod
    def get_locations(self, word: str) -> Iterator[Tuple[int, int]]:
        """

        Parameters
        ----------
        word : a word found in the document

        Returns
        -------

        """
        raise NotImplementedError()

    @abstractmethod
    def get_words(self) -> Iterator[str]:
        """

        Returns
        -------
        All words encountered in the document
        """
        raise NotImplementedError()

    @abstractmethod
    def pdf_convert_to_abl(self, file_position: str, encode: str = "utf8", save: Optional[str] = None, scan_param: Dict = {}) -> 'AbstractPostingsList':
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
            pl = self.__init__()
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
                    pl._add_word(word, count, docid)

            if save:
                with open(save, "w", encoding=encode) as f:
                    json.dump(pl.postings_list, f, indent=4)
            return pl
        return createPostingListFrompdf(file_position, encode, save, scan_param)


    def execute_query(
            self,
            query: str,
            term_match_modifier: float = 1.5,
            syn_match_modifier: float = 0.5,
    ) -> List[Tuple[int, float]]:
        """

        Parameters
        ----------
        syn_match_modifier :
        term_match_modifier :
        query :

        Returns an ordered list of docids and scores.
        -------

        """
        terms = tokens_to_terms(tokenize(query))

        result: Dict[int, float] = defaultdict(lambda: 0)

        for term in terms:
            match term:
                case Term(value=value):
                    for docid, word_count in self.get_locations(value):
                        result[docid] += math.log(word_count + 1) * term_match_modifier

                    try:
                        syns = word_synonyms(value)

                        for syn in syns:
                            for docid, word_count in self.get_locations(syn):
                                result[docid] += math.log(word_count + 1) * syn_match_modifier
                    except LookupError:
                        print("nltk package not installed. Ignoring synonyms")

                case NegativeTerm(value=value):
                    for docid, word_count in self.get_locations(value):
                        result[docid] -= math.log(word_count + 1) * term_match_modifier
                case _:
                    raise RuntimeError(f"Unknown term type {type(term)} with value {term}")
        return sorted(result.items(), key=lambda value: value[1], reverse=True)
