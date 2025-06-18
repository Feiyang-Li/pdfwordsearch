import argparse

from pdfwordsearch.data_structures.compressed_postings_list import CompressedPostingsList
from pdfwordsearch.match_score_rank.execute_query import execute_query
from pdfwordsearch.scan.pdf_scan import pdf_info_get
from pdfwordsearch.scan.pdf_to_pl import pdf_to_pl


class IOCoordinator:
    @staticmethod
    def run():
        parser = argparse.ArgumentParser(
            prog="pdfwordsearch",
            description="smart pdf querying",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        parser.add_argument("pdf", help="pdf path")
        parser.add_argument("query", default=None, help="search query")
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

        pdf_info = pdf_info_get(args.pdf)

        postings_list = pdf_to_pl(pdf_info, CompressedPostingsList)

        if args.query:
            scores = execute_query(args.query, postings_list)
        else:
            while True:
                query = input("please specify a query to search")
                scores = execute_query(query, postings_list)

        print(f"Found {len(scores)} result(s). Printing top {args.count} results")
        for i in range(min(args.count, len(scores))):
            print(scores[i])


