from typing import List

from pdfwordsearch.query.tokenizer import Token


class Term:
    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def add_to_list(self, term_list: List['Term']):
        term_list.append(self)

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

class EmptyTerm(Term):
    def __init__(self):
        super().__init__(None)
    def add_to_list(self, term_list: List['Term']):
        pass

class SimpleTerm(Term):
    """
    Rank documents with this term higher
    """

    pass


class NegativeTerm(Term):
    """
    Rank documents with this term lower.
    """

    def __init__(self):
        super().__init__([])

    def add_to_values(self, term: Term):
        self.value.append(term)


class ExactTerm(Term):
    """
    Rank documents with this exact phrase higher.
    """

    pass
def tokens_to_terms(tokens: List[Token]) -> List[Term]:
    result: List[Term] = []
    current_term: Term = EmptyTerm()
    for token in tokens:
        match token.kind:
            case "MINUS":
                current_term.add_to_list(result)
                current_term = NegativeTerm()
            case "WORD":
                term = SimpleTerm(token.value)
                if type(current_term) is NegativeTerm:
                    current_term.add_to_values(term)
                else:
                    term.add_to_list(result)
            case _:
                raise RuntimeError(f"Unexpected token {token}")
    current_term.add_to_list(result)
    return result

