import sympy as sp

def solve_linear_ode(P, Q, x):
    """
    Solve dy/dx + P(x)*y = Q(x)
    using the integrating factor method.
    """

    # Integrating factor
    IF = sp.exp(sp.integrate(P, x))

    # General solution
    integral = sp.integrate(IF * Q, x)

    C = sp.Symbol('C')

    y_solution = (integral + C) / IF

    return sp.simplify(IF), sp.simplify(y_solution)


x = sp.symbols('x')

P = 3
Q = 6*x
IF, solution = solve_linear_ode(P, Q, x)
#print("Integrating factor:")
#sp.pprint(IF)
#print("\nGeneral solution:")
#sp.pprint(solution)

x = sp.symbols('x')
y = sp.Function('y')

# Define the differential equation
#ode = sp.Eq(sp.diff(y(x), x) + 3*y(x), 6*x)
ode = sp.Eq(sp.diff(y(x), x), 4*x)

# Solve
solution = sp.dsolve(ode)
#sp.pprint(solution)

# Solve with initial condition y(0) = 2
sol = sp.dsolve(
    ode,
    y(x),
    ics={y(0): 2}
)

#print(sol)



import sympy as sp

def gen_sol(ode, yp, ic):

    # Extract independent variable and dependent function
    x = next(iter(ode.lhs.free_symbols))
    y = next(iter(ode.lhs.atoms(sp.Function))).func

    # 1. Homogeneous solution
    homogeneous_ode = sp.Eq(ode.lhs, 0)
    yc = sp.dsolve(homogeneous_ode, y(x))
    print("Homogeneous solution:")
    sp.pprint(yc)

    # 2. Particular solution using undetermined coefficients
    # Substitute yp into the original ODE's LHS
    residual = (
        ode.lhs.subs(y(x), yp)
        .doit() - ode.rhs
    )
    # Collect coefficients of the unknown parameters in yp
    parameters = yp.free_symbols - {x}
    equations = sp.Poly(residual, x).coeffs()
    constants = sp.solve(equations, list(parameters))
    yp = sp.simplify(yp.subs(constants))
    print("\nParticular solution:")
    sp.pprint(yp)

    # 3. General solution
    general = sp.simplify(yc.rhs + yp)
    print("\nGeneral solution:")
    sp.pprint(general)

    # 4. Extract integration constants from dsolve
    integration_constants = sorted(yc.free_symbols - {x}, key=str)
    print("\nIntegration constants:", integration_constants)

    # 5. Apply initial conditions
    equations_ic = []
    for condition, value in ic.items():
        if isinstance(condition, sp.Subs):
            # Derivative evaluated at a point
            order = condition.expr.derivative_count
            point = condition.point[0]
        elif isinstance(condition, sp.Derivative):
            order = condition.derivative_count
            point = condition.variables[0]
        elif condition.func == y:
            order = 0
            point = condition.args[0]
        else:
            raise ValueError(
                f"Unsupported initial condition: {condition}"
            )
        expression = sp.diff(general, x, order)
        equations_ic.append(
            expression.subs(x, point) - value
        )
    print("\nIC equations:")
    sp.pprint(equations_ic)
    constants_ic = sp.solve(
        equations_ic,
        integration_constants,
        dict=True
    )
    if not constants_ic:
        raise ValueError("Could not determine integration constants")
    constants_ic = constants_ic[0]
    print("\nConstants from IC:")
    print(constants_ic)

    # 6. Final solution
    final_solution = sp.simplify(general.subs(constants_ic))
    print("\nConstants:")
    print(constants_ic)
    print("\nSolution satisfying IC:")
    sp.pprint(final_solution)

    # 7. Verification
    check = sp.simplify(
        ode.lhs.subs(y(x), final_solution).doit()
        - ode.rhs
    )
    print("\nVerification:")
    print("ODE residual =", check)
    for condition, value in ic.items():
        print(condition, "=", 
              sp.simplify(condition.subs(y(x), final_solution)))

    return final_solution

def gen_sol2(ode, ic):
    sol = sp.dsolve(
        ode,
        y(x),
        ics=ic
    )
    sp.pprint(sol)



x = sp.symbols('x')
y = sp.Function('y')
A, B = sp.symbols('A B')

# ODE
ode = sp.Eq(
    sp.diff(y(x), x, 2)
    - 3*sp.diff(y(x), x)
    + 2*y(x),
    4*x + 1
)

# Particular solution assumption
yp = A*x + B

# Initial conditions
ic = {
    y(0): 10,
    sp.diff(y(x), x).subs(x, 0): 3
}

#sol = gen_sol(ode, yp, ic)

#gen_sol2(ode, ic)

sol = sp.dsolve(sp.Eq(sp.diff(y(x), x, 2) + y(x), x + 1), y(x))
sp.pprint(sol)

sol = sp.dsolve(sp.Eq(sp.diff(y(x), x) - y(x), 0), y(x))
sp.pprint(sol)

sol = sp.dsolve(sp.Eq(sp.diff(y(x), x, 2) - y(x), sp.exp(x)), y(x))
sp.pprint(sol)