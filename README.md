# Natural Language to Code Converter

A rule-based Natural Language to Code Converter that walks through lexical, syntax, semantic, and intent analysis stages.

## Backend setup

1. Create and activate a Python environment.
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the API:

```
uvicorn backend.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

## Frontend usage

Open `frontend/index.html` in your browser. Enter a sentence and press **Process** to see the results.

## Example inputs

- add x and 5
- print total
- if x greater than 10
- loop 3 times
