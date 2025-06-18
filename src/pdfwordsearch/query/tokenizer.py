import re


class Token:
    def __init__(self, kind: str, value):
        self.kind = kind
        self.value = value

    def __str__(self):
        return f"{self.kind}: {self.value}"

    def __repr__(self):
        return f"{self.kind}: {self.value}"

    def __eq__(self, other):
        return self.kind == other.kind and self.value == other.value


def tokenize(code):
    token_specification = [
        ("NUMBER", r"\d+(\.\d*)?"),  # Integer or decimal number
        ("QUOTATION_MARK", r'"'),  # Quotation Mark
        ("WORD", r"[A-Za-z\']+"),  # Words
        ("MINUS", r"[\-]"),  # -
        ("SKIP", r"[\s\.]+"),  # Skip over whitespace, punctuation
        ("MISMATCH", r"."),  # Any other character
    ]
    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "NUMBER":
            value = float(value) if "." in value else int(value)
        elif kind == "SKIP" or kind == "MISMATCH":
            continue
        yield Token(kind, value)
