from typing import Dict, List


ARITHMETIC_OPERATORS = {
    "add": "+",
    "subtract": "-",
    "multiply": "*",
    "divide": "/",
    "modulo": "%",
    "power": "**",
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
            lines.append(f"print({result})")

        elif inst_type == "assignment":
            target = instruction.get("target") or "value"
            value = instruction.get("value") or "0"
            lines.append(f"{target} = {value}")
            lines.append(f"print({target})")

        elif inst_type == "increment":
            target = instruction.get("target") or "value"
            lines.append(f"{target} += 1")
            lines.append(f"print({target})")

        elif inst_type == "decrement":
            target = instruction.get("target") or "value"
            lines.append(f"{target} -= 1")
            lines.append(f"print({target})")

        elif inst_type == "minmax":
            function = instruction.get("function") or "min"
            operands = instruction.get("operands", [])
            result = instruction.get("result", "result")
            if len(operands) >= 2:
                expression = f"{function}({operands[0]}, {operands[1]})"
            elif len(operands) == 1:
                expression = f"{function}({operands[0]}, 0)"
            else:
                expression = f"{function}(0, 0)"
            lines.append(f"{result} = {expression}")
            lines.append(f"print({result})")

        elif inst_type == "input":
            target = instruction.get("target") or "value"
            lines.append(f"{target} = input()")
            lines.append(f"print({target})")

        elif inst_type == "output":
            value = instruction.get("value") or "''"
            lines.append(f"print({value})")

        elif inst_type == "conditional":
            condition = instruction.get("condition", {})
            left = condition.get("left") or "x"
            operator = condition.get("operator") or ">"
            right = condition.get("right") or "0"
            lines.append(f"if {left} {operator} {right}:")
            if instruction.get("then_action") == "print":
                then_value = instruction.get("then_value") or "''"
                lines.append(f"    print({then_value})")
            else:
                lines.append("    # TODO: add statements")
                lines.append("    print(\"Condition matched\")")
            if instruction.get("else_action") == "print":
                else_value = instruction.get("else_value") or "''"
                lines.append("else:")
                lines.append(f"    print({else_value})")
            elif instruction.get("else"):
                lines.append("else:")
                lines.append("    # TODO: add statements")
                lines.append("    print(\"Condition not matched\")")

        elif inst_type == "conditional_compound":
            conditions = instruction.get("conditions", [])
            logical = instruction.get("logical") or "and"
            parts = []
            for condition in conditions:
                left = condition.get("left") or "x"
                operator = condition.get("operator") or "=="
                right = condition.get("right") or "0"
                parts.append(f"{left} {operator} {right}")
            condition_expr = f" {logical} ".join(parts) if parts else "False"
            lines.append(f"if {condition_expr}:")
            if instruction.get("then_action") == "print":
                then_value = instruction.get("then_value") or "''"
                lines.append(f"    print({then_value})")
            else:
                lines.append("    # TODO: add statements")
                lines.append("    print(\"Condition matched\")")

        elif inst_type == "while":
            condition = instruction.get("condition", {})
            left = condition.get("left") or "x"
            operator = condition.get("operator") or ">"
            right = condition.get("right") or "0"
            lines.append(f"while {left} {operator} {right}:")
            lines.append("    # TODO: add statements")
            lines.append("    print(\"Loop iteration\")")

        elif inst_type == "loop":
            count = instruction.get("count") or "0"
            lines.append(f"for _ in range({count}):")
            lines.append("    # TODO: add statements")
            lines.append("    print(\"Loop iteration\")")

        else:
            lines.append("# Unsupported instruction")

    return "\n".join(lines)
