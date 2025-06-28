import argparse
import time
from typing import List, Tuple

from pdfwordsearch.data_structures.compressed_postings_list import CompressedPostingsList
from pdfwordsearch.data_structures.postings_list import PostingsList
from pdfwordsearch.scan.pdf_scan import pdf_info_get
from pdfwordsearch.scan.pdf_to_pl import pdf_to_pl


class IOCoordinator:
    @staticmethod
    def _print_results(scores: List[Tuple[int, float]], nb_results_to_print: int, elapsed_time: float):
        print(f"Found {len(scores)} result(s) in {elapsed_time} seconds.")
        if len(scores) != 0:
            print(f"Printing top {nb_results_to_print} results")
        for i in range(min(nb_results_to_print, len(scores))):

            print(scores[i])

    @staticmethod
    def run():
        parser = argparse.ArgumentParser(
            prog="pdfwordsearch",
            description="smart pdf querying",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        parser.add_argument("pdf", help="pdf path")
        parser.add_argument("-q", "--query", default=None, help="search query")
        parser.add_argument(
            "-c", "--count", type=int, default=10, help="max number of matches to output"
        )
        parser.add_argument(
            "-i", "--image", action="store_true", help="search images for text"
        )
        parser.add_argument(
            "-r", "--range", type=str, default="all", help="specify page range"
        )
        parser.add_argument(
            "-s", "--sensitive", action="store_true", help="case insensitive search"
        )
        parser.add_argument(
            "-u", "--unoptimized", action="store_true", help="use an unoptimized postings list"
        )
        args = parser.parse_args()

        start = time.time()
        pdf_info = pdf_info_get(args.pdf)


        postings_list = pdf_to_pl(pdf_info, PostingsList if args.unoptimized else CompressedPostingsList)
        end = time.time()
        print(f"Loaded file in {end - start} seconds")

        if args.query:
            start = time.time()

            scores = postings_list.execute_query(args.query)
            end = time.time()

            IOCoordinator._print_results(scores, args.count, end - start)


        else:
            while True:
                try:
                    query = input("please specify a query to search:\n")
                except EOFError:
                    break
                start = time.time()
                scores = postings_list.execute_query(query)
                end = time.time()

                IOCoordinator._print_results(scores, args.count, end - start)




