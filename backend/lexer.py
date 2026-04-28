
import re
from typing import Dict, List

KEYWORDS = {
    "add",
    "subtract",
    "multiply",
    "divide",
    "modulo",
    "power",
    "print",
    "input",
    "if",
    "else",
    "begin",
    "end",
    "while",
    "loop",
    "set",
    "increment",
    "decrement",
    "minimum",
    "maximum",
}

WORDS = {
    "and",
    "from",
    "by",
    "greater",
    "than",
    "less",
    "equal",
    "is",
    "not",
    "or",
    "to",
    "of",
    "then",
    "times",
}


def preprocess(text: str) -> str:
    lowered = text.lower()
    cleaned = re.sub(r"[^\w\s-]", "", lowered)
    return cleaned


def classify_token(token: str) -> str:
    if token in KEYWORDS:
        return "KEYWORD"
    if token in WORDS:
        return "WORD"
    if re.fullmatch(r"-?\d+", token):
        return "NUMBER"
    if re.fullmatch(r"[a-z_][a-z0-9_]*", token):
        return "IDENTIFIER"
    return "UNKNOWN"


def tokenize(text: str) -> List[Dict[str, str]]:
    cleaned = preprocess(text)
    parts = [p for p in cleaned.split() if p]
    tokens = []
    for part in parts:
        tokens.append({"value": part, "type": classify_token(part)})
    return tokens
