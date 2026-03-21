from typing import Dict, List, Optional

Token = Dict[str, str]


def analyze(tokens: List[Token], rule: Optional[str]) -> Dict[str, object]:
    if not rule:
        return {"valid": False, "message": "Cannot analyze semantics without a rule match."}

    if rule in {"addition", "subtraction", "multiplication", "division"}:
        if len(tokens) != 4:
            return {"valid": False, "message": "Operation requires two operands."}
        if tokens[1]["type"] not in {"NUMBER", "IDENTIFIER"}:
            return {"valid": False, "message": "First operand is invalid."}
        if tokens[3]["type"] not in {"NUMBER", "IDENTIFIER"}:
            return {"valid": False, "message": "Second operand is invalid."}
        return {"valid": True, "message": "Operands are valid."}

    if rule == "print":
        if len(tokens) != 2:
            return {"valid": False, "message": "Print requires one operand."}
        if tokens[1]["type"] not in {"NUMBER", "IDENTIFIER"}:
            return {"valid": False, "message": "Print operand is invalid."}
        return {"valid": True, "message": "Print operand is valid."}

    if rule == "input":
        if len(tokens) != 2:
            return {"valid": False, "message": "Input requires a variable name."}
        if tokens[1]["type"] != "IDENTIFIER":
            return {"valid": False, "message": "Input target must be an identifier."}
        return {"valid": True, "message": "Input target is valid."}

    if rule == "if_greater":
        if len(tokens) != 5:
            return {"valid": False, "message": "Conditional requires identifier and number."}
        if tokens[1]["type"] != "IDENTIFIER":
            return {"valid": False, "message": "Left side of condition must be an identifier."}
        if tokens[4]["type"] != "NUMBER":
            return {"valid": False, "message": "Right side of condition must be a number."}
        return {"valid": True, "message": "Conditional operands are valid."}

    if rule == "loop_times":
        if len(tokens) != 3:
            return {"valid": False, "message": "Loop requires a number of times."}
        if tokens[1]["type"] != "NUMBER":
            return {"valid": False, "message": "Loop count must be a number."}
        if int(tokens[1]["value"]) <= 0:
            return {"valid": False, "message": "Loop count must be positive."}
        return {"valid": True, "message": "Loop count is valid."}

    return {"valid": False, "message": "Unknown rule for semantic analysis."}
