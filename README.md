# Theta Sketch — Unique Count Estimation

This sample demonstrates the **Theta Sketch** algorithm for efficiently estimating the number of unique elements in a
large data stream, without storing all elements in memory.

## What it does

The script simulates `UNIQUE_USER_ID_COUNT` login attempts (with `DUPLICATE_USER_ID_COUNT` duplicates) and uses a
Theta Sketch to estimate the number of unique user IDs. It then compares the estimate against the actual count and
reports the error rate.

Additionally, it verifies that the underlying hash function (MurmurHash3) produces a uniform distribution across the
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
Estimated number of unique user IDs: 10098031.452088824

Actual login attempts: 10025000
Actual unique user IDs: 10000000
Error: 0.98%
Result: PASS — error_rate is within the expected relative standard error of 1.12%

--- Hash Uniformity Test (Chi-Squared) ---
Samples: 10000000, Bins: 50
Chi-squared statistic: 47.2269
p-value: 0.5453
Result: PASS — hashes appear uniformly distributed (p > 0.05)
```
