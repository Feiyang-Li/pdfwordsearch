import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="pdfwordsearch",
        description="smart pdf querying",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("pdf", help="pdf path")
    parser.add_argument("query", help="search query")
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
    args = parser.parse_args()


if __name__ == "__main__":
    main()
