

import sympy as sp
import random
import json
import os

# Variables (typical algebra vars)
vars_list = ["a", "b", "c", "m", "n", "p", "q", "x", "y", "z"]

flashcards = []


def format_poly(expr):
    """Format polynomial for display: replace ** with ^, remove *."""
    s = sp.sstr(expr, order='lex')
    s = s.replace("**", "^").replace("*", "")
    return s


def format_term(coef, var=None, exp=1, hide_one=True):
    """Format individual term with coefficient rules."""
    if var is None:  # constant
        return str(coef)
    if coef == 1 and hide_one:
        c_str = ""
    elif coef == -1 and hide_one:
        c_str = "-"
    else:
        c_str = str(coef)
    if exp == 1:
        return f"{c_str}{var}"
    return f"{c_str}{var}^{exp}"


def pick_vars():
    """Pick two distinct variables, ordered alphabetically."""
    v1, v2 = random.sample(vars_list, 2)
    return tuple(sorted([v1, v2]))


def generate_case(case_type):
    if case_type == 1:
        # (x ± b)^2
        x = sp.Symbol(random.choice(vars_list))
        b = random.randint(1, 6)
        sign = random.choice([1, -1])
        expr = (x + sign * b) ** 2
        q = f"({x} {'+' if sign == 1 else '-'} {b})^2"

    elif case_type == 2:
        # (x ± by)^2
        v1, v2 = pick_vars()
        x = sp.Symbol(v1)
        y = sp.Symbol(v2)
        b = random.randint(1, 6)
        sign = random.choice([1, -1])
        expr = (x + sign * b * y) ** 2
        q = f"({x} {'+' if sign == 1 else '-'} {format_term(b, str(y), hide_one=True)})^2"

    elif case_type == 3:
        # (ax ± b)^2
        x = sp.Symbol(random.choice(vars_list))
        a = random.randint(1, 3)
        b = random.randint(1, 6)
        sign = random.choice([1, -1])
        expr = (a * x + sign * b) ** 2
        q = f"({format_term(a, str(x), hide_one=True)} {'+' if sign == 1 else '-'} {b})^2"

    else:  # case_type == 4
        # (ax ± by)^2
        v1, v2 = pick_vars()
        x = sp.Symbol(v1)
        y = sp.Symbol(v2)
        a = random.randint(1, 3)
        b = random.randint(1, 6)
        sign = random.choice([1, -1])
        expr = (a * x + sign * b * y) ** 2
        q = f"({format_term(a, str(x), hide_one=True)} {'+' if sign == 1 else '-'} {format_term(b, str(y), hide_one=True)})^2"

    return {"question": q, "answer": format_poly(sp.expand(expr))}


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


 