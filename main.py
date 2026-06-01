import random
import uuid
from math import sqrt

import numpy
import xxhash
from scipy import stats
from sortedcontainers import SortedList

UNIQUE_USER_ID_COUNT = 10_000_000
DUPLICATE_USER_ID_COUNT = 25_000
TOTAL_LOGIN_ATTEMPTS = UNIQUE_USER_ID_COUNT + DUPLICATE_USER_ID_COUNT
MAX_HASH_SPACE = 2 ** 128
MAX_SKETCH_SIZE = 10_000
RELATIVE_STANDARD_ERROR = 1 / sqrt(MAX_SKETCH_SIZE) * 100


def format_number(number: float, fraction_digits: int = 7) -> str:
    return f"{number:_.{fraction_digits}f}"


def generate_login_attempts() -> list[str]:
    unique_ids = [str(uuid.uuid4()) for _ in range(UNIQUE_USER_ID_COUNT)]
    duplicates = random.sample(unique_ids, DUPLICATE_USER_ID_COUNT)
    return unique_ids + duplicates


def hash_user_id_to_unit_interval(user_id: str) -> float:
    hash_value = xxhash.xxh128(user_id).intdigest()

    return hash_value / MAX_HASH_SPACE


def estimate_unique_count(retained_hashes: SortedList, theta_threshold: float) -> float:
    retained_hash_count = len(retained_hashes)
    return retained_hash_count / theta_threshold


def count_unique_logins_with_theta_sketch() -> None:
    print(f"--- Generating {format_number(TOTAL_LOGIN_ATTEMPTS, 0)} login attempts ---")
    login_attempts = generate_login_attempts()

    print(f"\n--- Estimating number of unique login attempts (Theta Sketch) ---")
    retained_hashes = SortedList()
    theta_threshold = 1.0

    for user_id in login_attempts:
        normalized_hash = hash_user_id_to_unit_interval(user_id)

        if normalized_hash >= theta_threshold:
            continue

        if normalized_hash in retained_hashes:
            continue

        retained_hashes.add(normalized_hash)
        if len(retained_hashes) > MAX_SKETCH_SIZE:
            theta_threshold = retained_hashes[MAX_SKETCH_SIZE]
            del retained_hashes[MAX_SKETCH_SIZE:]

    estimate_unique_user_ids = estimate_unique_count(retained_hashes, theta_threshold)
    error_rate = (abs(UNIQUE_USER_ID_COUNT - estimate_unique_user_ids) / UNIQUE_USER_ID_COUNT) * 100

    print(f"Estimated number of unique user IDs: {format_number(estimate_unique_user_ids)}")
    print(f"\nActual login attempts: {format_number(TOTAL_LOGIN_ATTEMPTS, 0)}")
    print(f"Actual unique user IDs: {format_number(UNIQUE_USER_ID_COUNT, 0)}")
    print(f"Theta threshold: {format_number(theta_threshold)}")
    print(f"Error: {format_number(error_rate, 2)}%")
    if error_rate <= RELATIVE_STANDARD_ERROR:
        print(
            f"Result: PASS — error_rate is within the expected relative standard error of {RELATIVE_STANDARD_ERROR:.2f}%")
    else:
        print(
            f"Result: WARNING - error_rate is higher the expected relative standard error of {RELATIVE_STANDARD_ERROR:.2f}%")

    verify_uniform_hash_distribution(login_attempts)


def verify_uniform_hash_distribution(login_attempts: list[str]):
    print(f"\n--- Hash uniformity test (Chi-Squared) ---")

    num_bins = 50
    hashes = [hash_user_id_to_unit_interval(uid) for uid in set(login_attempts)]
    observed, bin_edges = numpy.histogram(hashes, bins=num_bins, range=(0.0, 1.0))
    expected_count = len(set(login_attempts)) / num_bins
    expected = [expected_count] * num_bins
    chi2, p_value = stats.chisquare(observed, f_exp=expected)

    print(f"Samples: {format_number(UNIQUE_USER_ID_COUNT, 0)}, Bins: {format_number(num_bins, 0)}")
    print(f"Chi-squared statistic: {format_number(chi2)}")
    print(f"p-value: {p_value:.4f}")
    if p_value > 0.05:
        print("Result: PASS — hashes appear uniformly distributed (p > 0.05)")
    else:
        print("Result: FAIL — hashes do NOT appear uniformly distributed (p <= 0.05)")


if __name__ == "__main__":
    count_unique_logins_with_theta_sketch()
