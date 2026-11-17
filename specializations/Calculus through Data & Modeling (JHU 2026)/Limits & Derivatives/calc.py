
import numpy as np

def evaluate_limit(f, a, tol=1e-5, max_iter=12):
    """
    Numerically evaluate the left-hand and right-hand
    limits of f(x) as x approaches a.
    """

    h = 0.1
    left_values = []
    right_values = []

    for i in range(max_iter):
        h /= 2

        # Evaluate from the left and right
        left_values.append(f(a - h))
        right_values.append(f(a + h))

    LHL = left_values[-1]
    RHL = right_values[-1]

    # Check convergence of each one-sided limit
    left_converges = np.allclose(
        left_values[-3:], LHL, atol=tol, rtol=tol
    )

    right_converges = np.allclose(
        right_values[-3:], RHL, atol=tol, rtol=tol
    )

    print(f"Left-hand limit  = {LHL}")
    print(f"Right-hand limit = {RHL}")

    if left_converges and right_converges and np.isclose(
        LHL, RHL, atol=tol, rtol=tol
    ):
        print(f"\nLimit exists: {LHL}")
        return LHL

    print("\nTwo-sided limit does not exist (or convergence was not established).")
    return None


print(evaluate_limit(lambda x: (2*x+12)/abs(x+6), -6))
#print(evaluate_limit(lambda x: abs(x)*np.cos(1/np.sqrt(x)), 0))
#print(evaluate_limit(lambda x: np.sin(x-3) / np.sqrt(x+6), 3))
#print(evaluate_limit(lambda x: (np.sqrt(x**2+9)-5) / (x+4), -4))