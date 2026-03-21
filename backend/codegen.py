from typing import Dict, List


ARITHMETIC_OPERATORS = {
    "add": "+",
    "subtract": "-",
    "multiply": "*",
    "divide": "/",
}


def generate(ir: Dict[str, object]) -> str:
    """Convert IR instructions into readable Python code."""
    instructions = ir.get("instructions", [])
    if not instructions:
        return "# No instructions to generate."

    lines: List[str] = []
    for instruction in instructions:
        inst_type = instruction.get("type")

        if inst_type == "arithmetic":
            operation = instruction.get("operation")
            operands = instruction.get("operands", [])
            result = instruction.get("result", "result")
            operator = ARITHMETIC_OPERATORS.get(operation, "+")
            if len(operands) >= 2:
                expression = f"{operands[0]} {operator} {operands[1]}"
            elif len(operands) == 1:
                expression = f"{operands[0]} {operator} 0"
            else:
                expression = "0"
            lines.append(f"{result} = {expression}")

        elif inst_type == "input":
            target = instruction.get("target") or "value"
            lines.append(f"{target} = input()")

        elif inst_type == "output":
            value = instruction.get("value") or "''"
            lines.append(f"print({value})")

        elif inst_type == "conditional":
            condition = instruction.get("condition", {})
            left = condition.get("left") or "x"
            operator = condition.get("operator") or ">"
            right = condition.get("right") or "0"
            lines.append(f"if {left} {operator} {right}:")
            lines.append("    # TODO: add statements")
            lines.append("    pass")
            if instruction.get("else"):
                lines.append("else:")
                lines.append("    # TODO: add statements")
                lines.append("    pass")

        elif inst_type == "loop":
            count = instruction.get("count") or "0"
            lines.append(f"for _ in range({count}):")
            lines.append("    # TODO: add statements")
            lines.append("    pass")

        else:
            lines.append("# Unsupported instruction")

    return "\n".join(lines)
