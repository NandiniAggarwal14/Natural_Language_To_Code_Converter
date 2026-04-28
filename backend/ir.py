from typing import Dict, List, Optional


def generate(rule: Optional[str], entities: List[str]) -> Dict[str, object]:
    """Build a simple, machine-independent IR from the rule and extracted entities."""
    if not rule:
        return {"instructions": []}

    instruction: Dict[str, object]

    arithmetic_map = {
        "addition": "add",
        "subtraction": "subtract",
        "multiplication": "multiply",
        "division": "divide",
        "modulo": "modulo",
        "power": "power",
    }

    comparison_map = {
        "if_greater": ">",
        "if_less": "<",
        "if_equal": "==",
        "if_not_equal": "!=",
        "if_greater_equal": ">=",
        "if_less_equal": "<=",
        "if_else_greater_print": ">",
        "if_greater_then_begin_print_else_begin_print": ">",
        "while_greater": ">",
    }

    if rule in arithmetic_map:
        operands = entities[:2]
        if rule == "subtraction" and len(operands) == 2:
            operands = [operands[1], operands[0]]
        instruction = {
            "type": "arithmetic",
            "operation": arithmetic_map[rule],
            "operands": operands,
            "result": "result",
        }
    elif rule == "print":
        instruction = {"type": "output", "value": entities[0] if entities else None}
    elif rule == "input":
        instruction = {"type": "input", "target": entities[0] if entities else None}
    elif rule == "set_variable":
        instruction = {
            "type": "assignment",
            "target": entities[0] if len(entities) > 0 else None,
            "value": entities[1] if len(entities) > 1 else None,
        }
    elif rule == "increment":
        instruction = {"type": "increment", "target": entities[0] if entities else None}
    elif rule == "decrement":
        instruction = {"type": "decrement", "target": entities[0] if entities else None}
    elif rule in {"minimum", "maximum"}:
        instruction = {
            "type": "minmax",
            "function": "min" if rule == "minimum" else "max",
            "operands": entities[:2],
            "result": "result",
        }
    elif rule in {"if_greater", "if_less", "if_equal", "if_not_equal", "if_greater_equal", "if_less_equal"}:
        instruction = {
            "type": "conditional",
            "condition": {
                "left": entities[0] if len(entities) > 0 else None,
                "operator": comparison_map.get(rule, ">"),
                "right": entities[1] if len(entities) > 1 else None,
            },
            "body": [],
            "else": [],
        }
    elif rule == "if_else_greater_print":
        instruction = {
            "type": "conditional",
            "condition": {
                "left": entities[0] if len(entities) > 0 else None,
                "operator": comparison_map.get(rule, ">"),
                "right": entities[1] if len(entities) > 1 else None,
            },
            "body": [],
            "else_action": "print",
            "else_value": entities[2] if len(entities) > 2 else None,
        }
    elif rule == "if_greater_then_begin_print_else_begin_print":
        instruction = {
            "type": "conditional",
            "condition": {
                "left": entities[0] if len(entities) > 0 else None,
                "operator": comparison_map.get(rule, ">"),
                "right": entities[1] if len(entities) > 1 else None,
            },
            "then_action": "print",
            "then_value": entities[2] if len(entities) > 2 else None,
            "else_action": "print",
            "else_value": entities[3] if len(entities) > 3 else None,
        }
    elif rule in {"if_equal_and_equal_then_print", "if_equal_or_equal_then_print"}:
        logical = "and" if rule == "if_equal_and_equal_then_print" else "or"
        instruction = {
            "type": "conditional_compound",
            "conditions": [
                {
                    "left": entities[0] if len(entities) > 0 else None,
                    "operator": "==",
                    "right": entities[1] if len(entities) > 1 else None,
                },
                {
                    "left": entities[2] if len(entities) > 2 else None,
                    "operator": "==",
                    "right": entities[3] if len(entities) > 3 else None,
                },
            ],
            "logical": logical,
            "then_action": "print",
            "then_value": entities[4] if len(entities) > 4 else None,
        }
    elif rule == "while_greater":
        instruction = {
            "type": "while",
            "condition": {
                "left": entities[0] if len(entities) > 0 else None,
                "operator": comparison_map.get(rule, ">"),
                "right": entities[1] if len(entities) > 1 else None,
            },
            "body": [],
        }
    elif rule == "loop_times":
        instruction = {
            "type": "loop",
            "count": entities[0] if entities else None,
            "body": [],
        }
    else:
        instruction = {"type": "unknown"}

    return {"instructions": [instruction]}
