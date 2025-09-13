

import sympy as sp
import random
import json
import os
import re

# Variables (typical algebra vars)
vars_list = ["a", "b", "c", "m", "n", "p", "q", "x", "y", "z"]

flashcards = []


def format_term(coef, var=None, exp=1, hide_one=True):
    """Format an individual term with proper coefficient rules."""
    if var is None:  # constant
        return str(coef)

    if coef == 1 and hide_one:
        coef_str = ""
    elif coef == -1 and hide_one:
        coef_str = "-"
    else:
        coef_str = str(coef)

    if exp == 1:
        return f"{coef_str}{var}"
    return f"{coef_str}{var}^{exp}"


def format_poly_term(expr):
    """Format a single Sympy term into readable math string."""
    coef, factors = expr.as_coeff_Mul()

    if factors == 1:  # pure constant
        return str(coef)

    vars = []
    if isinstance(factors, sp.Symbol):
        vars = [(str(factors), 1)]
    elif isinstance(factors, sp.Pow):
        base, exp = factors.as_base_exp()
        vars = [(str(base), int(exp))]
    else:
        for f in factors.as_ordered_factors():
            if isinstance(f, sp.Symbol):
                vars.append((str(f), 1))
            elif isinstance(f, sp.Pow):
                base, exp = f.as_base_exp()
                vars.append((str(base), int(exp)))

    # Keep variable order as-is (alphabetical ordering handled elsewhere)
    var_str = "".join([f"{v}" if e == 1 else f"{v}^{e}" for v, e in vars])

    if coef == 1:
        coef_str = ""
    elif coef == -1:
        coef_str = "-"
    else:
        coef_str = str(coef)

    return coef_str + var_str


def normalize_spacing(s):
    """Ensure consistent spacing around + and - signs."""
    s = s.replace("+ -", "- ")
    s = re.sub(r"\s*\+\s*", " + ", s)
    s = re.sub(r"\s*-\s*", " - ", s)
    s = re.sub(r"\s+", " ", s)
    s = s.strip()
    if s.startswith("+ "):
        s = s[2:]
    return s


def format_binomial_square(first, second, sign):
    """Expand (first ± second)^2 in binomial order."""
    first_sq = sp.expand(first ** 2)
    cross = sp.expand(2 * sign * first * second)
    second_sq = sp.expand(second ** 2)

    parts = [format_poly_term(first_sq), format_poly_term(cross), format_poly_term(second_sq)]
    joined = " + ".join(parts)
    return normalize_spacing(joined)


def pick_vars():
    """Pick two distinct variables, return them in alphabetical order."""
    v1, v2 = random.sample(vars_list, 2)
    return tuple(sorted([sp.Symbol(v1), sp.Symbol(v2)], key=lambda s: str(s)))


def generate_case(case_type):
    x, y = pick_vars()  # alphabetically ordered

    if case_type == 1:
        b = random.randint(1, 6)
        sign = random.choice([1, -1])
        q = normalize_spacing(f"({x} {'+' if sign == 1 else '-'} {b})^2")
        ans = format_binomial_square(x, sp.Integer(b), sign)

    elif case_type == 2:
        b = random.randint(1, 6)
        sign = random.choice([1, -1])
        q = normalize_spacing(f"({x} {'+' if sign == 1 else '-'} {'' if b == 1 else b}{y})^2")
        ans = format_binomial_square(x, b * y, sign)

    elif case_type == 3:
        a = random.randint(1, 3)
        b = random.randint(1, 6)
        sign = random.choice([1, -1])
        a_term = f"{'' if a == 1 else a}{x}"
        q = normalize_spacing(f"({a_term} {'+' if sign == 1 else '-'} {b})^2")
        ans = format_binomial_square(a * x, sp.Integer(b), sign)

    else:  # case_type == 4
        a = random.randint(1, 3)
        b = random.randint(1, 6)
        sign = random.choice([1, -1])

        # enforce alphabetical order in question
        first_var, second_var = (x, y) if str(x) < str(y) else (y, x)
        a_term = f"{'' if a == 1 else a}{first_var}"
        b_term = f"{'' if b == 1 else b}{second_var}"

        q = normalize_spacing(f"({a_term} {'+' if sign == 1 else '-'} {b_term})^2")
        ans = format_binomial_square(a * first_var, b * second_var, sign)

    return {"question": q, "answer": ans}


# Generate 200 flashcards (50 per case)
for case_type in range(1, 5):
    for _ in range(50):
        flashcards.append(generate_case(case_type))

# Save to ./public/flashcards.json
output_dir = os.path.join(os.getcwd(), "public")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "flashcards.json")

with open(output_path, "w") as f:
    json.dump(flashcards, f, indent=2)

print(f"✅ flashcards.json generated with {len(flashcards)} flashcards at {output_path}")


