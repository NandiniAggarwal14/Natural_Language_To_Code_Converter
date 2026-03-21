from typing import Dict, List, Optional, Tuple

from .rules import RULES

Token = Dict[str, str]


def _is_operand(token: Token) -> bool:
    return token["type"] in {"NUMBER", "IDENTIFIER"}


def _match_pattern(tokens: List[Token], pattern: List[Tuple[str, Optional[str]]]) -> bool:
    if len(tokens) != len(pattern):
        return False
    for token, (ptype, pvalue) in zip(tokens, pattern):
        if ptype == "OPERAND":
            if not _is_operand(token):
                return False
            continue
        if ptype == "WORD":
            if token["value"] != pvalue:
                return False
            continue
        if token["type"] != ptype:
            return False
        if pvalue is not None and token["value"] != pvalue:
            return False
    return True


def parse(tokens: List[Token]) -> Dict[str, object]:
    if not tokens:
        return {"valid": False, "message": "No tokens found.", "rule": None}

    for rule in RULES:
        if _match_pattern(tokens, rule["pattern"]):
            return {"valid": True, "message": "Matched grammar rule.", "rule": rule["name"]}

    return {"valid": False, "message": "No matching grammar rule.", "rule": None}
