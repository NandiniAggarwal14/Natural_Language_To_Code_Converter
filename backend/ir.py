from typing import Dict, List, Optional


def generate(rule: Optional[str], entities: List[str]) -> Dict[str, object]:
    """Build a simple, machine-independent IR from the rule and extracted entities."""
    if not rule:
        return {"instructions": []}

    instruction: Dict[str, object]

    if rule == "addition":
        instruction = {
            "type": "arithmetic",
            "operation": "add",
            "operands": entities[:2],
            "result": "result",
        }
    elif rule == "subtraction":
        # Pattern is "subtract a from b" => b - a
        operands = entities[:2]
        if len(operands) == 2:
            operands = [operands[1], operands[0]]
        instruction = {
            "type": "arithmetic",
            "operation": "subtract",
            "operands": operands,
            "result": "result",
        }
    elif rule == "multiplication":
        instruction = {
            "type": "arithmetic",
            "operation": "multiply",
            "operands": entities[:2],
            "result": "result",
        }
    elif rule == "division":
        instruction = {
            "type": "arithmetic",
            "operation": "divide",
            "operands": entities[:2],
            "result": "result",
        }
    elif rule == "print":
        instruction = {"type": "output", "value": entities[0] if entities else None}
    elif rule == "input":
        instruction = {"type": "input", "target": entities[0] if entities else None}
    elif rule == "if_greater":
        instruction = {
            "type": "conditional",
            "condition": {
                "left": entities[0] if len(entities) > 0 else None,
                "operator": ">",
                "right": entities[1] if len(entities) > 1 else None,
            },
            "body": [],
            "else": [],
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
