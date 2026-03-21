from typing import Dict, List, Optional

Token = Dict[str, str]

INTENT_MAP = {
    "addition": "addition",
    "subtraction": "subtraction",
    "multiplication": "multiplication",
    "division": "division",
    "print": "print",
    "input": "input",
    "if_greater": "conditional",
    "loop_times": "loop",
}


def extract(tokens: List[Token], rule: Optional[str]) -> Dict[str, object]:
    intent = INTENT_MAP.get(rule)
    entities = [token["value"] for token in tokens if token["type"] in {"NUMBER", "IDENTIFIER"}]
    return {"intent": intent, "entities": entities}
