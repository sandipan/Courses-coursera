"""
AKS (Agrawal-Kayal-Saxena) Primality Test Implementation in Python.

Reference:
    Manindra Agrawal, Neeraj Kayal, and Nitin Saxena,
    "PRIMES is in P", Annals of Mathematics, 160(2), 2004, pp. 781-793.
"""

import math


# ==============================================================================
# Helper Functions: Polynomial Arithmetic modulo (X^r - 1, n)
# ==============================================================================

def poly_mult_mod(p1: list[int], p2: list[int], r: int, n: int) -> list[int]:
    """
    Multiplies two polynomials p1 and p2 modulo (X^r - 1) and modulo n.
    Polynomials are represented as lists of coefficients where index i is the coeff of X^i.
    
    Since X^r = 1 mod (X^r - 1), any term X^k reduces to X^(k mod r).
    """
    res = [0] * r
    for i, c1 in enumerate(p1):
        if c1 == 0:
            continue
        for j, c2 in enumerate(p2):
            if c2 == 0:
                continue
            idx = (i + j) % r
            res[idx] = (res[idx] + c1 * c2) % n
    return res


def poly_pow_mod(base: list[int], exponent: int, r: int, n: int) -> list[int]:
    """
    Computes (base^exponent) mod (X^r - 1, n) via binary exponentiation.
    Runs in O(r^2 * log(exponent)) modular multiplications.
    """
    res = [0] * r
    res[0] = 1  # polynomial '1'

    curr = [c % n for c in base]
    # Pad or trim to size r
    if len(curr) < r:
        curr.extend([0] * (r - len(curr)))
    else:
        curr = curr[:r]

    exp = exponent
    while exp > 0:
        if exp & 1:
            res = poly_mult_mod(res, curr, r, n)
        curr = poly_mult_mod(curr, curr, r, n)
        exp >>= 1

    return res


# ==============================================================================
# Step 1 Helper: Perfect Power Detection
# ==============================================================================

def is_perfect_power(n: int) -> bool:
    """
    Checks if n = a^b for some integers a > 1 and b > 1.
    If n is a perfect power, it is strictly composite.
    
    Complexity: O(log^3 n) using integer b-th root checks.
    """
    if n <= 3:
        return False

    max_b = math.floor(math.log2(n))
    for b in range(2, max_b + 1):
        # Find integer floor of n^(1/b) using binary search
        low = 2
        high = int(math.isqrt(n)) + 1
        while low <= high:
            mid = (low + high) // 2
            val = mid ** b
            if val == n:
                return True
            elif val < n:
                low = mid + 1
            else:
                high = mid - 1
    return False


# ==============================================================================
# Step 2 Helper: Multiplicative Order and Euler Totient
# ==============================================================================

def euler_phi(m: int) -> int:
    """Computes Euler's totient function phi(m)."""
    result = m
    p = 2
    temp = m
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def find_smallest_r(n: int) -> int:
    """
    Finds the smallest integer r such that ord_r(n) > (log2(n))^2.
    
    Theory:
      ord_r(n) is the smallest positive integer k such that n^k = 1 (mod r).
      AKS proved that such an r exists and is bounded by max(3, ceil((log2 n)^5)).
    """
    max_k = math.floor(math.log2(n) ** 2)
    
    r = 2
    while True:
        if math.gcd(r, n) == 1:
            # Check powers n^k mod r for k = 1 .. max_k
            # If for all k <= (log2 n)^2, n^k != 1 (mod r), then ord_r(n) > (log2 n)^2
            rem = 1
            satisfies = True
            for k in range(1, max_k + 1):
                rem = (rem * n) % r
                if rem == 1:
                    satisfies = False
                    break
            if satisfies:
                return r
        r += 1


# ==============================================================================
# Main AKS Primality Test Algorithm
# ==============================================================================

def is_prime_aks(n: int) -> bool:
    """
    Deterministic polynomial-time primality test (AKS algorithm).
    Returns True if n is prime, False if composite.
    """
    # Base cases
    if n < 2:
        return False
    if n in (2, 3):
        return True

    # --------------------------------------------------------------------------
    # Step 1: Check if n = a^b for b > 1
    # If n is a perfect power, it is composite.
    # --------------------------------------------------------------------------
    if is_perfect_power(n):
        return False

    # --------------------------------------------------------------------------
    # Step 2: Find smallest r such that ord_r(n) > (log2(n))^2
    # --------------------------------------------------------------------------
    r = find_smallest_r(n)

    # --------------------------------------------------------------------------
    # Step 3: Check gcd(a, n) for 1 < a <= r
    # If 1 < gcd(a, n) < n, then a is a non-trivial factor, so n is composite.
    # --------------------------------------------------------------------------
    for a in range(2, min(r + 1, n)):
        g = math.gcd(a, n)
        if 1 < g < n:
            return False

    # --------------------------------------------------------------------------
    # Step 4: If n <= r, then n is prime.
    # (Since it passed step 1 and has no factor <= r)
    # --------------------------------------------------------------------------
    if n <= r:
        return True

    # --------------------------------------------------------------------------
    # Step 5: For a = 1 to floor(2 * sqrt(phi(r)) * log2(n)), test:
    #         (X + a)^n == X^n + a  (mod X^r - 1, n)
    #
    # Notice that X^n mod (X^r - 1) = X^(n mod r).
    # So the right-hand side is simply the polynomial: X^(n % r) + a.
    # --------------------------------------------------------------------------
    phi_r = euler_phi(r)
    max_a = math.floor(2 * math.sqrt(phi_r) * math.log2(n))

    for a in range(1, max_a + 1):
        # Left-hand side: (X + a)^n mod (X^r - 1, n)
        # Represent base (X + a) as [a, 1]
        base_poly = [a % n, 1]
        lhs = poly_pow_mod(base_poly, n, r, n)

        # Right-hand side: (X^(n % r) + a) mod n
        rhs = [0] * r
        rhs[0] = (rhs[0] + a) % n
        rhs[n % r] = (rhs[n % r] + 1) % n

        # Compare lhs and rhs
        if lhs != rhs:
            return False

    # --------------------------------------------------------------------------
    # Step 6: If all checks passed, n is unconditionally PRIME.
    # --------------------------------------------------------------------------
    return True


# ==============================================================================
# Verification / Demo
# ==============================================================================
if __name__ == "__main__":
    test_numbers = [2, 3, 4, 17, 19, 25, 29, 31, 561, 1009]
    print(f"{'Number':<8} | {'AKS Result':<12} | {'Expected'}")
    print("-" * 35)

    def simple_is_prime(x):
        if x < 2: return False
        for d in range(2, int(math.isqrt(x)) + 1):
            if x % d == 0: return False
        return True

    for num in test_numbers:
        result = is_prime_aks(num)
        expected = simple_is_prime(num)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"{num:<8} | {str(result):<12} | {expected} ({status})")