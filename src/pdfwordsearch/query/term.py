from abc import ABC, abstractmethod
from typing import List

from pdfwordsearch.query.tokenizer import Token


class AbstractTerm(ABC):

    def get_value(self):
        raise NotImplementedError()

    def add_to_list(self, term_list: List['AbstractTerm']):
        term_list.append(self)

    def __repr__(self):
        return str(self.get_value())

    def __eq__(self, other):
        return self.get_value() == other.get_value()

class AbstractAddableTerm(AbstractTerm):
    @abstractmethod
    def add_to_values(self, term):
        raise NotImplementedError()

class EmptyTerm(AbstractAddableTerm):
    def add_to_values(self, term):
        pass

    def __init__(self):
        super().__init__()

    def get_value(self):
        return None

    def add_to_list(self, term_list: List['AbstractTerm']):
        pass

class Term(AbstractTerm):
    """
    Rank documents with this term higher
    """
    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_value(self):
        return self.value


class NegativeTerm(AbstractAddableTerm):
    """
    Rank documents with this term lower.
    """

    def __init__(self):
        super().__init__()
        self.value = []

    def get_value(self):
        return self.value

    def add_to_values(self, term: AbstractTerm):
        self.value.append(term)


def tokens_to_terms(tokens: List[Token]) -> List[AbstractTerm]:
    result: List[AbstractTerm] = []
    current_term: AbstractAddableTerm = EmptyTerm()
    for token in tokens:
        match token.kind:
            case "MINUS":
                current_term.add_to_list(result)
                current_term = NegativeTerm()
            case "WORD":
                term = Term(token.value)
                if type(current_term) is NegativeTerm:
                    current_term.add_to_values(term)
                else:
                    term.add_to_list(result)
            case _:
                raise RuntimeError(f"Unexpected token {token}")
    current_term.add_to_list(result)
    return result

