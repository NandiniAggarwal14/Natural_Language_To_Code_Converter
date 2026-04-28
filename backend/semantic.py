from typing import Dict, List, Optional

Token = Dict[str, str]


def _is_operand(token: Token) -> bool:
    return token["type"] in {"NUMBER", "IDENTIFIER"}


def analyze(tokens: List[Token], rule: Optional[str]) -> Dict[str, object]:
    if not rule:
        return {"valid": False, "message": "Cannot analyze semantics without a rule match."}

    if rule in {"addition", "subtraction", "multiplication", "division", "modulo", "power"}:
        if len(tokens) != 4:
            return {"valid": False, "message": "Operation requires two operands."}
        if not _is_operand(tokens[1]):
            return {"valid": False, "message": "First operand is invalid."}
        if not _is_operand(tokens[3]):
            return {"valid": False, "message": "Second operand is invalid."}
        return {"valid": True, "message": "Operands are valid."}

    if rule in {"minimum", "maximum"}:
        if len(tokens) != 5:
            return {"valid": False, "message": "Min/Max requires two operands."}
        if not _is_operand(tokens[2]) or not _is_operand(tokens[4]):
            return {"valid": False, "message": "Min/Max operands are invalid."}
        return {"valid": True, "message": "Min/Max operands are valid."}

    if rule == "print":
        if len(tokens) != 2:
            return {"valid": False, "message": "Print requires one operand."}
        if not _is_operand(tokens[1]):
            return {"valid": False, "message": "Print operand is invalid."}
        return {"valid": True, "message": "Print operand is valid."}

    if rule == "input":
        if len(tokens) != 2:
            return {"valid": False, "message": "Input requires a variable name."}
        if tokens[1]["type"] != "IDENTIFIER":
            return {"valid": False, "message": "Input target must be an identifier."}
        return {"valid": True, "message": "Input target is valid."}

    if rule == "set_variable":
        if len(tokens) != 4:
            return {"valid": False, "message": "Assignment requires a target and value."}
        if tokens[1]["type"] != "IDENTIFIER":
            return {"valid": False, "message": "Assignment target must be an identifier."}
        if not _is_operand(tokens[3]):
            return {"valid": False, "message": "Assignment value is invalid."}
        return {"valid": True, "message": "Assignment is valid."}

    if rule in {"increment", "decrement"}:
        if len(tokens) != 2:
            return {"valid": False, "message": "Increment/decrement requires a target."}
        if tokens[1]["type"] != "IDENTIFIER":
            return {"valid": False, "message": "Target must be an identifier."}
        return {"valid": True, "message": "Increment/decrement target is valid."}

    if rule in {"if_greater", "if_less", "if_equal", "if_not_equal", "if_greater_equal", "if_less_equal"}:
        expected_length = 5 if rule in {"if_greater", "if_less", "if_equal"} else 6
        if rule in {"if_greater_equal", "if_less_equal"}:
            expected_length = 7
        if len(tokens) != expected_length:
            return {"valid": False, "message": "Conditional requires two operands."}
        if not _is_operand(tokens[1]):
            return {"valid": False, "message": "Left side of condition is invalid."}
        if not _is_operand(tokens[-1]):
            return {"valid": False, "message": "Right side of condition is invalid."}
        return {"valid": True, "message": "Conditional operands are valid."}

    if rule == "if_greater_then_begin_print_else_begin_print":
        if len(tokens) != 16:
            return {"valid": False, "message": "If-else block requires a condition and two print values."}
        if not _is_operand(tokens[1]) or not _is_operand(tokens[5]):
            return {"valid": False, "message": "Condition operands are invalid."}
        if not _is_operand(tokens[9]) or not _is_operand(tokens[14]):
            return {"valid": False, "message": "Print operands are invalid."}
        return {"valid": True, "message": "If-else block operands are valid."}

    if rule in {"if_equal_and_equal_then_print", "if_equal_or_equal_then_print"}:
        if len(tokens) != 11:
            return {"valid": False, "message": "Compound condition requires two comparisons and a print value."}
        if not _is_operand(tokens[1]) or not _is_operand(tokens[3]):
            return {"valid": False, "message": "First comparison operands are invalid."}
        if not _is_operand(tokens[5]) or not _is_operand(tokens[7]):
            return {"valid": False, "message": "Second comparison operands are invalid."}
        if not _is_operand(tokens[10]):
            return {"valid": False, "message": "Print value is invalid."}
        return {"valid": True, "message": "Compound condition operands are valid."}

    if rule == "if_else_greater_print":
        if len(tokens) != 8:
            return {"valid": False, "message": "If-else requires a condition and print value."}
        if not _is_operand(tokens[1]) or not _is_operand(tokens[4]):
            return {"valid": False, "message": "Condition operands are invalid."}
        if not _is_operand(tokens[7]):
            return {"valid": False, "message": "Else print value is invalid."}
        return {"valid": True, "message": "If-else operands are valid."}

    if rule == "while_greater":
        if len(tokens) != 5:
            return {"valid": False, "message": "While loop requires two operands."}
        if not _is_operand(tokens[1]) or not _is_operand(tokens[4]):
            return {"valid": False, "message": "While loop operands are invalid."}
        return {"valid": True, "message": "While loop operands are valid."}

    if rule == "loop_times":
        if len(tokens) != 3:
            return {"valid": False, "message": "Loop requires a number of times."}
        if tokens[1]["type"] != "NUMBER":
            return {"valid": False, "message": "Loop count must be a number."}
        if int(tokens[1]["value"]) <= 0:
            return {"valid": False, "message": "Loop count must be positive."}
        return {"valid": True, "message": "Loop count is valid."}

    return {"valid": False, "message": "Unknown rule for semantic analysis."}
