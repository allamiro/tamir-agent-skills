#!/usr/bin/env python3
"""Simulate ODE models, find steady states and classify their stability (standard library only).

  ode.py simulate MODEL.txt --t 20 [--dt 0.01] [--method rk4|euler] [--every 1]
  ode.py steady MODEL.txt                 Newton search for a steady state, starting from the initial values
  ode.py stability MODEL.txt              Jacobian and eigenvalues at the steady state, with a classification
  ode.py sens MODEL.txt --t 10            normalised local sensitivity of each state at time t to each parameter
  ode.py --selftest

MODEL.txt, one statement per line:

    var S = 10            state variable and its initial value
    par k1 = 0.5          parameter
    d S = -k1*S/(1+S)     right-hand side dS/dt (one per state variable)

Expressions may use + - * / **, parentheses, numbers, the names declared above, t, and exp, log, sqrt, sin, cos,
tanh, abs, min, max. They are checked against that list before use, so a model file cannot run other code.

RK4 with a fixed step is fine for smooth, non-stiff teaching models. If the stiffness ratio printed by stability
is large (thousands or more), or the solution changes as you shrink --dt, use an adaptive stiff solver
(for example scipy.integrate.solve_ivp with method LSODA or BDF, or a dedicated tool such as COPASI).
"""
import argparse
import ast
import cmath
import math
import sys

FUNCS = {"exp": math.exp, "log": math.log, "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos, "tanh": math.tanh,
         "abs": abs, "min": min, "max": max}
ALLOWED = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd,
           ast.Constant, ast.Name, ast.Load, ast.Call)


def compile_expr(text, names):
    tree = ast.parse(text.strip(), mode="eval")
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED):
            raise ValueError("not allowed in an expression: %s (in %r)" % (type(node).__name__, text))
        if isinstance(node, ast.Constant) and not isinstance(node.value, (int, float)):
            raise ValueError("only numbers are allowed as constants: %r" % text)
        if isinstance(node, ast.Call) and not (isinstance(node.func, ast.Name) and node.func.id in FUNCS):
            raise ValueError("unknown function in %r" % text)
        if isinstance(node, ast.Name) and node.id not in names and node.id not in FUNCS and node.id != "t":
            raise ValueError("unknown name %r in %r" % (node.id, text))
    return compile(tree, "<model>", "eval")


def parse_model(text):
    """Returns (state names, initial values, parameters, right-hand side function f(t, x) -> list)."""
    states, init, pars, rhs = [], [], {}, {}
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        kind, _, rest = line.partition(" ")
        name, eqsign, expr = rest.partition("=")
        name = name.strip()
        if not eqsign or not name.isidentifier():
            raise ValueError("cannot read %r" % raw)
        if kind == "var":
            states.append(name)
            init.append(float(eval(compile_expr(expr, set(pars)), {"__builtins__": {}}, dict(FUNCS, **pars))))
        elif kind == "par":
            pars[name] = float(eval(compile_expr(expr, set(pars)), {"__builtins__": {}}, dict(FUNCS, **pars)))
        elif kind == "d":
            rhs[name] = expr
        else:
            raise ValueError("lines start with var, par or d: %r" % raw)
    missing = [s for s in states if s not in rhs]
    extra = [s for s in rhs if s not in states]
    if missing or extra or not states:
        raise ValueError("every state needs exactly one 'd' line (missing %s, unknown %s)" % (missing, extra))
    names = set(states) | set(pars)
    code = [compile_expr(rhs[s], names) for s in states]

    def f(t, x):
        env = dict(FUNCS, **pars)
        env.update(zip(states, x))
        env["t"] = t
        return [eval(c, {"__builtins__": {}}, env) for c in code]
    return states, init, pars, f


def integrate(f, x0, t_end, dt, method="rk4"):
    """List of (t, x) from 0 to t_end with a fixed step."""
    steps = int(round(t_end / dt))
    if steps < 1:
        raise ValueError("t must be at least one step")
    t, x = 0.0, list(x0)
    out = [(t, list(x))]
    for i in range(steps):
        if method == "euler":
            k = f(t, x)
            x = [xi + dt * ki for xi, ki in zip(x, k)]
        elif method == "rk4":
            k1 = f(t, x)
            k2 = f(t + dt / 2, [xi + dt / 2 * k for xi, k in zip(x, k1)])
            k3 = f(t + dt / 2, [xi + dt / 2 * k for xi, k in zip(x, k2)])
            k4 = f(t + dt, [xi + dt * k for xi, k in zip(x, k3)])
            x = [xi + dt / 6 * (a + 2 * b + 2 * c + d) for xi, a, b, c, d in zip(x, k1, k2, k3, k4)]
        else:
            raise ValueError("method must be rk4 or euler")
        t = (i + 1) * dt
        out.append((t, list(x)))
    return out


def jacobian(f, x, t=0.0, h=1e-6):
    n = len(x)
    f0 = f(t, x)
    jac = [[0.0] * n for _ in range(n)]
    for j in range(n):
        step = h * max(1.0, abs(x[j]))
        xp = list(x)
        xm = list(x)
        xp[j] += step
        xm[j] -= step
        fp, fm = f(t, xp), f(t, xm)
        for i in range(n):
            jac[i][j] = (fp[i] - fm[i]) / (2 * step)
    return jac


def solve_linear(a, b):
    n = len(a)
    m = [row[:] + [bi] for row, bi in zip(a, b)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(m[i][c]))
        if abs(m[p][c]) < 1e-14:
            raise ValueError("singular Jacobian")
        m[c], m[p] = m[p], m[c]
        for i in range(n):
            if i != c:
                fct = m[i][c] / m[c][c]
                m[i] = [x - fct * y for x, y in zip(m[i], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def steady_state(f, x0, tol=1e-10, maxit=100):
    x = list(x0)
    for _ in range(maxit):
        fx = f(0.0, x)
        if max(abs(v) for v in fx) < tol:
            return x
        dx = solve_linear(jacobian(f, x), [-v for v in fx])
        lam = 1.0
        while lam > 1e-4:
            xn = [xi + lam * d for xi, d in zip(x, dx)]
            if max(abs(v) for v in f(0.0, xn)) < max(abs(v) for v in fx):
                break
            lam /= 2
        x = xn
    raise ValueError("Newton did not converge from these initial values; try others or simulate to a steady state")


def eigenvalues(a):
    """Eigenvalues of a small real matrix: characteristic polynomial (Faddeev-LeVerrier) and Durand-Kerner roots."""
    n = len(a)
    coeffs = [1.0]
    mk = [[0.0] * n for _ in range(n)]
    for k in range(1, n + 1):
        mk = [[sum(a[i][l] * mk[l][j] for l in range(n)) + (coeffs[-1] if i == j else 0.0) for j in range(n)] for i in range(n)]
        am = [[sum(a[i][l] * mk[l][j] for l in range(n)) for j in range(n)] for i in range(n)]
        coeffs.append(-sum(am[i][i] for i in range(n)) / k)
    z = [complex(0.4, 0.9) ** k for k in range(n)]
    for _ in range(2000):
        new = []
        for i in range(n):
            num = sum(c * z[i] ** (n - k) for k, c in enumerate(coeffs))
            den = 1
            for j in range(n):
                if j != i:
                    den *= z[i] - z[j]
            new.append(z[i] - num / den if den != 0 else z[i] + 1e-9)
        done = max(abs(p - q) for p, q in zip(new, z)) < 1e-15
        z = new
        if done:
            break
    out = []
    for r in z:
        r = complex(round(r.real, 9), round(r.imag, 9))
        out.append(r)
    return sorted(out, key=lambda v: (v.real, v.imag))


def classify(eigs):
    re_ = [e.real for e in eigs]
    im_ = [e.imag for e in eigs]
    if any(abs(r) < 1e-9 for r in re_):
        if all(abs(r) < 1e-9 for r in re_) and any(abs(i) > 1e-9 for i in im_):
            return "centre (purely imaginary eigenvalues): linearisation cannot decide; check the nonlinear terms"
        return "non-hyperbolic (an eigenvalue has zero real part): linearisation cannot decide"
    osc = any(abs(i) > 1e-9 for i in im_)
    if all(r < 0 for r in re_):
        return "asymptotically stable " + ("focus (damped oscillation)" if osc else "node")
    if all(r > 0 for r in re_):
        return "unstable " + ("focus (growing oscillation)" if osc else "node")
    return "saddle (unstable): some directions attract, some repel"


def sensitivities(f, init, pars, t_end, dt=0.01, rel=1e-4):
    """Normalised local sensitivities d ln x_i(t_end) / d ln p_j by central differences. Returns {par: [per state]}.
    A state at zero gives None, because the normalisation divides by it."""
    base = integrate(f, init, t_end, dt)[-1][1]
    out = {}
    for name in list(pars):
        p0 = pars[name]
        if p0 == 0:
            out[name] = [None] * len(base)
            continue
        h = rel * abs(p0)
        pars[name] = p0 + h
        up = integrate(f, init, t_end, dt)[-1][1]
        pars[name] = p0 - h
        dn = integrate(f, init, t_end, dt)[-1][1]
        pars[name] = p0
        out[name] = [((u - d) / (2 * h)) * p0 / x if x != 0 else None for u, d, x in zip(up, dn, base)]
    return out


def selftest():
    fails, count = [], [0]

    def eq(name, got, want, tol=None):
        count[0] += 1
        ok = abs(got - want) <= tol if tol is not None else got == want
        if not ok:
            fails.append("%s: got %r, want %r" % (name, got, want))

    states, init, pars, f = parse_model("par k = 0.5\nvar x = 2\nd x = -k*x")
    traj = integrate(f, init, 4.0, 0.01)
    eq("RK4 matches exp decay", traj[-1][1][0], 2 * math.exp(-2.0), 1e-9)
    eul = integrate(f, init, 4.0, 0.01, "euler")
    eq("Euler is less accurate but close", abs(eul[-1][1][0] - 2 * math.exp(-2.0)) < 0.003 and abs(eul[-1][1][0] - 2 * math.exp(-2.0)) > 1e-6, True)
    states, init, pars, f = parse_model("par r = 1\npar K = 10\nvar N = 1\nd N = r*N*(1 - N/K)")
    t = 3.0
    exact = 10 / (1 + 9 * math.exp(-t))
    eq("logistic growth", integrate(f, init, t, 0.001)[-1][1][0], exact, 1e-8)
    states, init, pars, f = parse_model("par k1 = 2\npar k2 = 0.5\nvar x = 0\nd x = k1 - k2*x")
    eq("production-degradation steady state", steady_state(f, init)[0], 4.0, 1e-9)
    eq("its eigenvalue is -k2", eigenvalues(jacobian(f, [4.0]))[0].real, -0.5, 1e-6)
    states, init, pars, f = parse_model("var x = 1\nvar v = 0\nd x = v\nd v = -x")
    e = eigenvalues(jacobian(f, [0.0, 0.0]))
    eq("harmonic oscillator imag eigenvalues", (round(e[0].imag, 6), round(e[1].imag, 6)), (-1.0, 1.0))
    eq("classified as centre", classify(e).startswith("centre"), True)
    states, init, pars, f = parse_model("par c = 0.5\nvar x = 1\nvar v = 0\nd x = v\nd v = -x - c*v")
    eq("damped oscillator is a stable focus", classify(eigenvalues(jacobian(f, [0.0, 0.0]))), "asymptotically stable focus (damped oscillation)")
    states, init, pars, f = parse_model("var x = 0.1\nvar y = 0.1\nd x = x\nd y = -y")
    eq("saddle", classify(eigenvalues(jacobian(f, [0.0, 0.0]))).startswith("saddle"), True)
    states, init, pars, f = parse_model("var x = 0.1\nvar y = 0.1\nd x = x + y\nd y = 2*y")
    eq("unstable node", classify(eigenvalues(jacobian(f, [0.0, 0.0]))), "unstable node")
    # Michaelis-Menten with inflow: steady S solves v_in = Vmax S/(Km+S)
    states, init, pars, f = parse_model("par vin = 1\npar Vmax = 2\npar Km = 3\nvar S = 1\nd S = vin - Vmax*S/(Km + S)")
    eq("MM inflow steady state", steady_state(f, init)[0], 3.0, 1e-9)
    eq("time-dependent input allowed", parse_model("var x = 0\nd x = sin(t)")[3](math.pi / 2, [0])[0], 1.0, 1e-12)
    states, init, pars, f = parse_model("par k = 0.3\npar b = 1\nvar x = 2\nd x = -k*x")
    sv = sensitivities(f, init, pars, 5.0)
    eq("sensitivity of exponential decay to k is -k t", sv["k"][0], -1.5, 1e-6)
    eq("an unused parameter has zero sensitivity", sv["b"][0], 0.0, 1e-9)
    eq("parameters restored after the sensitivity run", pars["k"], 0.3)
    eq("3x3 eigenvalues of a triangular matrix", [round(v.real, 6) for v in eigenvalues([[-1, 2, 0], [0, -3, 1], [0, 0, -5]])], [-5.0, -3.0, -1.0])
    for bad, label in ((lambda: parse_model("var x = 1\nd x = __import__('os')"), "call not allowed"),
                       (lambda: parse_model("var x = 1\nd x = y"), "unknown name"),
                       (lambda: parse_model("var x = 1"), "missing d line"),
                       (lambda: parse_model("var x = 1\nd x = x.real"), "attribute access"),
                       (lambda: steady_state(lambda t, x: [x[0] ** 2 + 1], [0.5]), "no steady state")):
        count[0] += 1
        try:
            bad()
            fails.append("%s should raise" % label)
        except (ValueError, SyntaxError):
            pass
    # Added after a mutation test: each case below is hand-computed and covers a path the earlier checks missed.
    def _near(label, got, want, tol=1e-6):
        count[0] += 1
        if not abs(got - want) <= tol:
            fails.append("%s: got %r, want %r" % (label, got, want))

    def _same(label, got, want):
        count[0] += 1
        if got != want:
            fails.append("%s: got %r, want %r" % (label, got, want))

    def _raises(label, fn):
        count[0] += 1
        try:
            fn()
            fails.append("%s should raise" % label)
        except (ValueError, ZeroDivisionError):
            pass
    _st, _in, _pa, _f = parse_model("var x = 0\nd x = cos(t)")
    _near("time-dependent right side: x(1) = sin(1)", integrate(_f, [_in[s] for s in _st] if isinstance(_in, dict) else _in, 1.0, 0.01)[-1][1][0], math.sin(1), 1e-9)
    _st, _in, _pa, _f = parse_model("var x = 0\nvar y = 3\nd x = 2 - x - y\nd y = x - y")
    _ss = steady_state(_f, [0.0, 3.0])
    _near("two-dimensional Newton steady state x", _ss[0], 1.0, 1e-8)
    _near("two-dimensional Newton steady state y", _ss[1], 1.0, 1e-8)
    _same("a zero eigenvalue is not called stable", "stable" in classify([0.0, -1.0]) and "asymptotically" in classify([0.0, -1.0]), False)
    if fails:
        print("SELFTEST FAILED")
        for f_ in fails:
            print(" -", f_)
        return 1
    print("ode selftest: OK (%d checks)" % count[0])
    return 0


def main():
    ap = argparse.ArgumentParser(description="Simulate ODE models, find steady states and classify stability.")
    ap.add_argument("op", nargs="?", choices=["simulate", "steady", "stability", "sens"])
    ap.add_argument("model", nargs="?")
    ap.add_argument("--t", type=float, default=10.0)
    ap.add_argument("--dt", type=float, default=0.01)
    ap.add_argument("--method", default="rk4", choices=["rk4", "euler"])
    ap.add_argument("--every", type=float, default=1.0, help="simulate: print every this much time")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.op or not a.model:
        ap.error("give an operation and a model file, or --selftest")
    try:
        states, init, pars, f = parse_model(open(a.model, encoding="utf-8").read())
        if a.op == "sens":
            sv = sensitivities(f, init, pars, a.t, a.dt)
            print("normalised sensitivity d ln(state) / d ln(parameter) at t = %g" % a.t)
            print("%-14s %s" % ("parameter", " ".join("%12s" % s for s in states)))
            for name, row in sorted(sv.items(), key=lambda kv: -max(abs(v) for v in kv[1] if v is not None) if any(v is not None for v in kv[1]) else 0):
                print("%-14s %s" % (name, " ".join("%12s" % ("n/a" if v is None else "%.4g" % v) for v in row)))
            print("A value of 0.5 means a 1 percent rise in the parameter raises the state about 0.5 percent at this time.")
        elif a.op == "simulate":
            traj = integrate(f, init, a.t, a.dt, a.method)
            stride = max(1, int(round(a.every / a.dt)))
            print("t\t" + "\t".join(states))
            for i, (t, x) in enumerate(traj):
                if i % stride == 0 or i == len(traj) - 1:
                    print("%.6g\t%s" % (t, "\t".join("%.6g" % v for v in x)))
        else:
            ss = steady_state(f, init)
            print("steady state: " + ", ".join("%s = %.6g" % (s, v) for s, v in zip(states, ss)))
            if a.op == "stability":
                jac = jacobian(f, ss)
                print("Jacobian:")
                for row in jac:
                    print("  [" + ", ".join("%.6g" % v for v in row) + "]")
                eigs = eigenvalues(jac)
                print("eigenvalues: " + ", ".join(("%.6g" % e.real) if abs(e.imag) < 1e-9 else "%.6g%+.6gi" % (e.real, e.imag) for e in eigs))
                print("classification: " + classify(eigs))
                mags = [abs(e.real) for e in eigs if abs(e.real) > 1e-12]
                if len(mags) > 1:
                    print("stiffness ratio (largest / smallest |real part|): %.3g" % (max(mags) / min(mags)))
    except (ValueError, OSError, ZeroDivisionError, OverflowError) as e:
        print("error:", e)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
