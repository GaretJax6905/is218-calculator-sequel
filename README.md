# Calculator Sequel: Commands, Factory, and Statistics

An interactive command-line calculator that extends my earlier OOP calculator ([is218_calculator](https://github.com/GaretJax6905/is218_calculator)) through the six-part IS218 sequel: static operations, callable composition, a calculation factory, flexible `*values`/`**options` inputs, application commands, and pandas-backed statistics with CSV input.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/GaretJax6905/is218-calculator-sequel.git
cd is218-calculator-sequel
```

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies (pytest, pytest-cov, pandas):
```bash
python -m pip install -r requirements.txt
```

## Running the Calculator

```bash
python -m calculator
```

Requests are a single line: an operation name, positional values, and optional `key=value` settings.

| Request | Example | Result |
|---|---|---|
| `add/subtract/multiply/divide A B` | `divide 7 2` | `Result: 3.5000` |
| `square VALUE` / `sqrt VALUE` | `sqrt 9` | `Result: 3.0000` |
| `power VALUE [exponent=N]` | `power 3 exponent=4` | `Result: 81.0000` (default exponent 2) |
| `sum VALUES` | `sum 2 3 4` | `Result: 9.0000` |
| `mean VALUES` | `mean 2 4 6` | `Result: 4.0000` |
| `stddev VALUES [ddof=0/1]` | `stddev 10 20 30 40 50` | `Result: 15.8114` (sample by default) |
| `csv mean/stddev PATH` | `csv mean values.csv` | `Result: 30.0000` |
| `count` | `count` | Number of successful calculations |
| `history` | `history` | Saved requests and results, in order |
| `clear` | `clear` | `History cleared.` |
| `help` | `help` | Supported syntax |
| `exit` | `exit` |