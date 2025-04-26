from typing import Dict
import os
from pdfwordsearch.output.abstract_output import AbstractOutput


class ConsoleOutput(AbstractOutput):

    def __init__(self, nb_of_results: int) -> None:
        self.nb_of_results = nb_of_results

    def output(self, rankings: Dict[int, float]) -> None:
        print(f"Found {len(rankings)} results")

        term_size = os.get_terminal_size()
        top_message = f"Top {self.nb_of_results} results"
        horizontal_line_size = term_size.columns // 2 - len(top_message)
        horizontal_line = "-" * horizontal_line_size
        print(f"{horizontal_line}{top_message}{horizontal_line}")