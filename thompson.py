# =========================
# Postfix → NFA (Thompson's Construction)
# =========================

# ---------- State ----------
class State:
    counter = 0

    def __init__(self):
        self.id = State.counter
        State.counter += 1
        self.transitions = {}   # symbol -> list of States
        self.is_accept = False

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

    def __repr__(self):
        return f"q{self.id}"


# ---------- NFA Fragment ----------
class NFA:
    def __init__(self, start, accept):
        self.start  = start   # single start State
        self.accept = accept  # single accept State

    def get_all_states(self):
        """BFS to collect every state reachable from start."""
        visited = set()
        queue   = [self.start]
        while queue:
            state = queue.pop(0)
            if state in visited:
                continue
            visited.add(state)
            for targets in state.transitions.values():
                for t in targets:
                    queue.append(t)
        return visited


# ---------- Thompson's Construction ----------
def build_symbol_nfa(symbol):
    """Base case: single character."""
    s = State()
    e = State()
    s.add_transition(symbol, e)
    return NFA(s, e)


def build_concat_nfa(nfa1, nfa2):
    """nfa1 followed by nfa2."""
    nfa1.accept.add_transition('ε', nfa2.start)
    nfa1.accept.is_accept = False
    return NFA(nfa1.start, nfa2.accept)


def build_union_nfa(nfa1, nfa2):
    """nfa1 | nfa2."""
    s = State()
    e = State()
    s.add_transition('ε', nfa1.start)
    s.add_transition('ε', nfa2.start)
    nfa1.accept.add_transition('ε', e)
    nfa2.accept.add_transition('ε', e)
    nfa1.accept.is_accept = False
    nfa2.accept.is_accept = False
    return NFA(s, e)


def build_star_nfa(nfa1):
    """nfa1* — zero or more."""
    s = State()
    e = State()
    s.add_transition('ε', nfa1.start)   # enter the loop
    s.add_transition('ε', e)            # skip entirely
    nfa1.accept.add_transition('ε', nfa1.start)  # loop back
    nfa1.accept.add_transition('ε', e)            # exit loop
    nfa1.accept.is_accept = False
    return NFA(s, e)


def postfix_to_nfa(postfix):
    """Main function: reads postfix string, returns final NFA."""
    State.counter = 0   # reset state IDs for clean output
    stack = []

    for char in postfix:
        if char.isalnum() or char == 'ε':
            stack.append(build_symbol_nfa(char))

        elif char == '.':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(build_concat_nfa(nfa1, nfa2))

        elif char == '|':
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            stack.append(build_union_nfa(nfa1, nfa2))

        elif char == '*':
            nfa1 = stack.pop()
            stack.append(build_star_nfa(nfa1))

    final_nfa = stack.pop()
    final_nfa.accept.is_accept = True
    return final_nfa


# ---------- Print NFA Transition Table ----------
def print_nfa(nfa):
    states = sorted(nfa.get_all_states(), key=lambda s: s.id)

    print("\n===== NFA Transition Table =====")
    print(f"Start State  : {nfa.start}")
    print(f"Accept State : {nfa.accept}")
    print()

    # Collect all symbols
    symbols = set()
    for state in states:
        symbols.update(state.transitions.keys())
    symbols = sorted(symbols)

    # Header
    col_w = 12
    header = f"{'State':<{col_w}}" + "".join(f"{s:<{col_w}}" for s in symbols)
    print(header)
    print("-" * len(header))

    # Rows
    for state in states:
        marker = "→" if state == nfa.start else (" *" if state.is_accept else "  ")
        row = f"{marker}{state!r:<{col_w - 2}}"
        for sym in symbols:
            targets = state.transitions.get(sym, [])
            cell = "{" + ",".join(repr(t) for t in targets) + "}" if targets else "∅"
            row += f"{cell:<{col_w}}"
        print(row)
    print()
