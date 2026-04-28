from typing import Dict, List, Optional

Token = Dict[str, str]

INTENT_MAP = {
    "addition": "addition",
    "subtraction": "subtraction",
    "multiplication": "multiplication",
    "division": "division",
    "modulo": "modulo",
    "power": "power",
    "print": "print",
    "input": "input",
    "set_variable": "assignment",
    "increment": "increment",
    "decrement": "decrement",
    "minimum": "minimum",
    "maximum": "maximum",
    "if_greater": "conditional",
    "if_less": "conditional",
    "if_equal": "conditional",
    "if_not_equal": "conditional",
    "if_greater_equal": "conditional",
    "if_less_equal": "conditional",
    "if_greater_then_begin_print_else_begin_print": "conditional_else",
    "if_equal_and_equal_then_print": "conditional_compound",
    "if_equal_or_equal_then_print": "conditional_compound",
    "if_else_greater_print": "conditional_else",
    "while_greater": "loop",
    "loop_times": "loop",
}


def extract(tokens: List[Token], rule: Optional[str]) -> Dict[str, object]:
    intent = INTENT_MAP.get(rule)
    entities = [token["value"] for token in tokens if token["type"] in {"NUMBER", "IDENTIFIER"}]
    return {"intent": intent, "entities": entities}
