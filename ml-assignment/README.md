# Trigram Language Model

This directory contains the core assignment files for the Trigram Language Model.

## How to Run

This README explains how to run the test-suite and the small example generator included in the assignment.

Prerequisites
- Python 3.8+ (the project uses only the standard library and `pytest` for tests)
- Install test deps:

```powershell
cd "e:\my documents\decible.ai\ml-intern-assessment"
python -m pip install -r requirements.txt
```

Run tests
- From the repository root run the test file for the n‑gram model:

```powershell
cd "e:\my documents\decible.ai\ml-intern-assessment"
pytest ml-assignment/tests/test_ngram.py -q
```

Quick example (train + generate)
- The repository includes a small runner at `ml-assignment/src/generate.py` which trains a `TrigramModel` on `ml-assignment/data/example_corpus.txt` and prints a generated sentence.
- Run the example from the `ml-assignment` folder so `src` imports resolve correctly:

```powershell
cd "e:\my documents\decible.ai\ml-intern-assessment\ml-assignment"
python src/generate.py
```

Programmatic usage
- Example usage from Python:

```python
from src.ngram_model import TrigramModel
import random

random.seed(42)  # optional: make generation reproducible
model = TrigramModel()
with open("data/example_corpus.txt") as f:
    model.fit(f.read())
print(model.generate(max_length=30))
```

Notes and tips
- If you prefer to run tests or scripts from the repository root, add `ml-assignment` to `PYTHONPATH` for the session:

```powershell
$env:PYTHONPATH = "e:\my documents\decible.ai\ml-intern-assessment\ml-assignment"
python ml-assignment/src/generate.py
```

- The `TrigramModel` implementation is in `ml-assignment/src/ngram_model.py` and is intentionally simple and easy to extend. See `evaluation.md` for the design rationale and optimization suggestions.

## Design Choices

Please document your design choices in the `evaluation.md` file. This should be a 1-page summary of the decisions you made and why you made them.
