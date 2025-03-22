from typing import Dict, List

class PostingsList:
    def __init__(self):
        self.postings_list : Dict[str, List] = dict()

    def add_word(self, word: str, location: int):
        if word in self.postings_list:
            self.postings_list[word].append(location)
        else:
            self.postings_list[word] = [location]

    def get_locations(self, word : str) -> List[int]:
        return self.postings_list[word]