# -*- coding: utf-8 -*-
# =========================
# Regex Preprocessing & Validation
# =========================

VALID_SYMBOLS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789ε")
OPERATORS = set("|*+?()")

# ---------- Check Balanced Parentheses ----------
def is_balanced(regex):
    stack = []
    for char in regex:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:
                return False
            stack.pop()
    return len(stack) == 0

# ---------- Validate Characters ----------
def is_valid_symbols(regex):
    for char in regex:
        if char not in VALID_SYMBOLS and char not in OPERATORS:
            return False, char
    return True, None

# ---------- Check Operator Usage ----------
def check_operator_usage(regex):
    operators = "|.*+?"
    prev = ''
    for i, char in enumerate(regex):
        if char in operators:
            # '*' '+' '?' cannot appear at start
            if i == 0 and char in '*+?':
                return False, f"Operator '{char}' cannot be at the start"

            # '*' '+' '?' '|' cannot appear right after '('
            if prev == '(' and char in '*+?|':
                return False, f"Operator '{char}' cannot appear right after '('"

            # '*' '+' '?' cannot follow another binary operator
            if char in '*+?' and prev in '|.':
                return False, f"Operator '{char}' cannot follow '{prev}'"

            # cannot start with '|' or '.'
            if i == 0 and char in "|.":
                return False, f"Operator '{char}' cannot be at the start"

            # cannot end with '|' or '.'
            if i == len(regex) - 1 and char in "|.":
                return False, f"Operator '{char}' cannot be at the end"

            # '|' cannot appear right before ')'
            if char == '|' and i + 1 < len(regex) and regex[i + 1] == ')':
                return False, f"Operator '|' cannot appear right before ')'"

            # consecutive unary operators like '**' '++' '??' '+*' etc.
            if prev in '*+?' and char in '*+?':
                return False, f"Consecutive operators '{prev}{char}' are not allowed"

            # two consecutive binary operators like '||' '|.' are invalid
            if prev in operators and char in "|.":
                return False, f"Two consecutive operators detected: '{prev}{char}'"
        prev = char
    return True, ""

# ---------- Validate Regex ----------
def validate_regex(regex):
    if not regex:
        return False, "Error: Regex is empty."

    valid, invalid_char = is_valid_symbols(regex)
    if not valid:
        return False, (
            f"Error: Invalid symbol '{invalid_char}' detected.\n"
            f"Allowed symbols: a-z, A-Z, 0-9, ε\n"
            f"Allowed operators: | * + ? ( )"
        )

    if not is_balanced(regex):
        return False, "Error: Unbalanced parentheses. Make sure every '(' has a matching ')'."

    valid, msg = check_operator_usage(regex)
    if not valid:
        return False, f"Error: {msg}"

    return True, "Valid regex."

# ---------- Get Last Token ----------
def get_last_token(expr):
    """Returns (token_string, start_index) of the last atom in expr."""
    if not expr:
        return '', 0
    if expr[-1] == ')':
        # walk back to matching '('
        depth = 0
        for i in range(len(expr) - 1, -1, -1):
            if expr[i] == ')':
                depth += 1
            elif expr[i] == '(':
                depth -= 1
                if depth == 0:
                    return expr[i:], i
    else:
        # single character token (including ε)
        return expr[-1], len(expr) - 1

# ---------- Expand + and ? into primitives ----------
# a+  -->  a.a*      (one or more)
# a?  -->  (a|ε)     (zero or one)
def expand_operators(regex):
    result = ""
    i = 0
    while i < len(regex):
        char = regex[i]
        if char == '+':
            last, start = get_last_token(result)
            result = result[:start] + last + '.' + last + '*'
        elif char == '?':
            last, start = get_last_token(result)
            result = result[:start] + '(' + last + '|ε)'
        else:
            result += char
        i += 1
    return result

# ---------- Add Explicit Concatenation ----------
def add_concatenation(regex):
    result = ""
    for i in range(len(regex)):
        result += regex[i]
        if i + 1 < len(regex):
            curr = regex[i]
            nxt  = regex[i + 1]
            # Insert '.' when:
            # left  : symbol, ε, ')', '*', '+', '?'
            # right : symbol, ε, '('
            if ((curr in VALID_SYMBOLS or curr in ')*+?') and
                (nxt  in VALID_SYMBOLS or nxt  == '(')):
                result += '.'
    return result

# ---------- Process Regex ----------
def preprocess_regex():
    regex = input("Enter Regular Expression: ").strip()

    # Step 1: Validate
    is_valid, message = validate_regex(regex)
    if not is_valid:
        print(message)
        return None
    print(message)

    expanded = expand_operators(regex)
    print("After expanding + and ?:   ", expanded)

    processed = add_concatenation(expanded)
    print("After adding concatenation:", processed)

    return processed
