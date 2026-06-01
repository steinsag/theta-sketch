# Theta Sketch — Unique Count Estimation

This sample demonstrates the **Theta Sketch** algorithm for efficiently estimating the number of unique elements in a
large data stream, without storing all elements in memory.

## What it does

The script simulates `UNIQUE_USER_ID_COUNT` login attempts (with `DUPLICATE_USER_ID_COUNT` duplicates) and uses a
Theta Sketch to estimate the number of unique user IDs. It then compares the estimate against the actual count and
reports the error rate.

Additionally, it verifies that the underlying hash function (xxHash 128 Bit) produces a uniform distribution across the
hash space using a Chi-Squared test.

### Key concepts

- **Theta (θ)**: A dynamic threshold in the `[0, 1)` interval. Only hashes below θ are retained.
- **Sketch size**: Capped at `MAX_SKETCH_SIZE` retained hashes. When the cap is reached, θ shrinks to keep only the
  smallest hashes.
- **Estimation**: `unique_count ≈ retained_hash_count / θ`
- **Expected error**: Relative standard error of `1 / sqrt(MAX_SKETCH_SIZE) ≈ RELATIVE_STANDARD_ERROR`

## Setup

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

### Example output

```
--- Generating 10_025_000 login attempts ---

--- Estimating number of unique login attempts (Theta Sketch) ---
Estimated number of unique user IDs: 10_027_428.4006383

Actual login attempts: 10_025_000
Actual unique user IDs: 10_000_000
Theta threshold: 0.0009973
Error: 0.27%
Result: PASS — error_rate is within the expected relative standard error of 1.00%

--- Hash uniformity test (Chi-Squared) ---
Samples: 10_000_000, Bins: 50
Chi-squared statistic: 35.2483600
p-value: 0.9301
Result: PASS — hashes appear uniformly distributed (p > 0.05)
```
