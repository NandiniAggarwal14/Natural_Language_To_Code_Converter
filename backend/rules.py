RULES = [
    {
        "name": "addition",
        "pattern": [("KEYWORD", "add"), ("OPERAND", None), ("WORD", "and"), ("OPERAND", None)],
    },
    {
        "name": "subtraction",
        "pattern": [("KEYWORD", "subtract"), ("OPERAND", None), ("WORD", "from"), ("OPERAND", None)],
    },
    {
        "name": "multiplication",
        "pattern": [("KEYWORD", "multiply"), ("OPERAND", None), ("WORD", "and"), ("OPERAND", None)],
    },
    {
        "name": "division",
        "pattern": [("KEYWORD", "divide"), ("OPERAND", None), ("WORD", "by"), ("OPERAND", None)],
    },
    {
        "name": "print",
        "pattern": [("KEYWORD", "print"), ("OPERAND", None)],
    },
    {
        "name": "input",
        "pattern": [("KEYWORD", "input"), ("IDENTIFIER", None)],
    },
    {
        "name": "if_greater",
        "pattern": [
            ("KEYWORD", "if"),
            ("IDENTIFIER", None),
            ("WORD", "greater"),
            ("WORD", "than"),
            ("NUMBER", None),
        ],
    },
    {
        "name": "loop_times",
        "pattern": [("KEYWORD", "loop"), ("NUMBER", None), ("WORD", "times")],
    },
]
