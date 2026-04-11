# =========================================================
# COMPLETE REGEX TO NFA CONVERTER WITH VISUALIZATION
# =========================================================

class State:
    """Represents a state in the NFA."""
    
    def __init__(self, id, is_accept=False):
        self.id = id
        self.is_accept = is_accept
        self.transitions = {}  # symbol -> list of states
    
    def add_transition(self, symbol, target_state):
        """Add a transition from this state on given symbol to target state."""
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(target_state)
    
    def __repr__(self):
        return f"q{self.id}"


class NFA:
    """Represents a Non-deterministic Finite Automaton."""
    
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept
    
    def get_all_states(self):
        """Return all states reachable from start state."""
        states = set()
        
        def collect(state):
            if state in states:
                return
            states.add(state)
            for targets in state.transitions.values():
                for target in targets:
                    collect(target)
        
        collect(self.start)
        return states


# =========================================================
# REGEX TO NFA CONVERTER (Thompson Construction)
# =========================================================

class RegexToNFA:
    """Convert regular expression to NFA using Thompson's construction."""
    
    def __init__(self):
        self.state_counter = 0
    
    def new_state(self, is_accept=False):
        """Create a new state with unique ID."""
        state = State(self.state_counter, is_accept)
        self.state_counter += 1
        return state
    
    def from_symbol(self, symbol):
        """Create NFA for a single symbol."""
        start = self.new_state()
        accept = self.new_state(is_accept=True)
        start.add_transition(symbol, accept)
        return NFA(start, accept)
    
    def from_concat(self, nfa1, nfa2):
        """Concatenate two NFAs: nfa1 followed by nfa2."""
        # Remove accept status from nfa1's accept state
        nfa1.accept.is_accept = False
        
        # Add epsilon transition from nfa1's accept to nfa2's start
        nfa1.accept.add_transition('ε', nfa2.start)
        
        # Return new NFA with nfa1's start and nfa2's accept
        return NFA(nfa1.start, nfa2.accept)
    
    def from_union(self, nfa1, nfa2):
        """Union of two NFAs: nfa1 or nfa2."""
        start = self.new_state()
        accept = self.new_state(is_accept=True)
        
        # Add epsilon transitions from new start to both NFAs
        start.add_transition('ε', nfa1.start)
        start.add_transition('ε', nfa2.start)
        
        # Remove accept status from original accept states
        nfa1.accept.is_accept = False
        nfa2.accept.is_accept = False
        
        # Add epsilon transitions from both NFAs to new accept
        nfa1.accept.add_transition('ε', accept)
        nfa2.accept.add_transition('ε', accept)
        
        return NFA(start, accept)
    
    def from_star(self, nfa):
        """Kleene star of NFA: nfa*"""
        start = self.new_state()
        accept = self.new_state(is_accept=True)
        
        # Add epsilon from new start to accept (for zero repetitions)
        start.add_transition('ε', accept)
        
        # Add epsilon from new start to original start
        start.add_transition('ε', nfa.start)
        
        # Remove accept status from original accept
        nfa.accept.is_accept = False
        
        # Add epsilon from original accept back to original start (for repetition)
        nfa.accept.add_transition('ε', nfa.start)
        
        # Add epsilon from original accept to new accept
        nfa.accept.add_transition('ε', accept)
        
        return NFA(start, accept)
    
    def from_plus(self, nfa):
        """One or more: nfa+"""
        # nfa+ = nfa followed by nfa*
        star_nfa = self.from_star(nfa)
        
        # Create a copy of nfa for concatenation
        nfa_copy = self.from_symbol('temp')  # Placeholder
        # Rebuild properly
        start = self.new_state()
        accept = self.new_state(is_accept=True)
        
        # Add epsilon from start to nfa.start
        start.add_transition('ε', nfa.start)
        
        # Remove accept from original
        nfa.accept.is_accept = False
        
        # Add epsilon from nfa.accept to star's start
        star_start = self.new_state()
        star_accept = self.new_state(is_accept=True)
        star_start.add_transition('ε', accept)
        star_accept.is_accept = False
        
        nfa.accept.add_transition('ε', star_start)
        
        return NFA(start, accept)
    
    def from_optional(self, nfa):
        """Optional: nfa?"""
        start = self.new_state()
        accept = self.new_state(is_accept=True)
        
        # Direct epsilon from start to accept (skip nfa)
        start.add_transition('ε', accept)
        
        # Epsilon from start to nfa
        start.add_transition('ε', nfa.start)
        
        # Remove accept from nfa
        nfa.accept.is_accept = False
        
        # Epsilon from nfa.accept to accept
        nfa.accept.add_transition('ε', accept)
        
        return NFA(start, accept)
    
    def parse_regex(self, regex):
        """Parse and convert regex to NFA."""
        # Add concatenation operator explicitly
        regex = self.add_concatenation_operator(regex)
        # Convert infix to postfix (Shunting yard algorithm)
        postfix = self.infix_to_postfix(regex)
        # Build NFA from postfix
        return self.build_nfa_from_postfix(postfix)
    
    def add_concatenation_operator(self, regex):
        """Add '.' for concatenation between adjacent tokens."""
        result = []
        operators = {'|', '*', '+', '?', '(', ')'}
        
        for i in range(len(regex)):
            current = regex[i]
            result.append(current)
            
            if i < len(regex) - 1:
                next_char = regex[i + 1]
                # Add '.' if current is not operator and next is not operator
                # Except for cases like 'a*' where * follows a
                if (current not in operators and current != '(' and 
                    next_char not in operators and next_char != ')' and
                    next_char not in {'*', '+', '?'}):
                    result.append('.')
                # Handle cases like 'a('
                elif (current not in operators and current != '(' and next_char == '('):
                    result.append('.')
                # Handle cases like ')a'
                elif (current == ')' and next_char not in operators and next_char != ')'):
                    result.append('.')
                # Handle cases like '*a'
                elif (current in {'*', '+', '?'} and next_char not in operators and next_char != ')'):
                    result.append('.')
        
        return ''.join(result)
    
    def infix_to_postfix(self, regex):
        """Convert infix regex to postfix using Shunting yard algorithm."""
        precedence = {
            '|': 1,
            '.': 2,
            '*': 3,
            '+': 3,
            '?': 3
        }
        
        output = []
        stack = []
        
        for char in regex:
            if char == '(':
                stack.append(char)
            elif char == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()  # Remove '('
            elif char in precedence:
                while (stack and stack[-1] != '(' and 
                       precedence.get(stack[-1], 0) >= precedence.get(char, 0)):
                    output.append(stack.pop())
                stack.append(char)
            else:  # Character (operand)
                output.append(char)
        
        while stack:
            output.append(stack.pop())
        
        return ''.join(output)
    
    def build_nfa_from_postfix(self, postfix):
        """Build NFA from postfix expression using stack."""
        stack = []
        
        for char in postfix:
            if char == '|':  # Union
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self.from_union(nfa1, nfa2))
            elif char == '.':  # Concatenation
                nfa2 = stack.pop()
                nfa1 = stack.pop()
                stack.append(self.from_concat(nfa1, nfa2))
            elif char == '*':  # Kleene star
                nfa = stack.pop()
                stack.append(self.from_star(nfa))
            elif char == '+':  # One or more
                nfa = stack.pop()
                stack.append(self.from_plus(nfa))
            elif char == '?':  # Optional
                nfa = stack.pop()
                stack.append(self.from_optional(nfa))
            else:  # Symbol
                stack.append(self.from_symbol(char))
        
        return stack.pop()


# =========================================================
# UI / PRESENTATION PART (YOUR ORIGINAL CODE)
# =========================================================

def state_label(state, nfa):
    """Return pretty label for report."""
    label = repr(state)
    tags = []

    if state == nfa.start:
        tags.append("Start")
    if state.is_accept:
        tags.append("Accept")

    if tags:
        label += " (" + ", ".join(tags) + ")"
    return label


def print_transition_list(nfa):
    """Clear transition list format: q0 --a--> q1"""
    states = sorted(nfa.get_all_states(), key=lambda s: s.id)

    print("\n" + "=" * 45)
    print("NFA TRANSITION LIST")
    print("=" * 45)
    print(f"Start State  : {nfa.start}")
    print(f"Accept State : {nfa.accept}")
    print("-" * 45)

    has_transitions = False

    for state in states:
        for symbol, targets in state.transitions.items():
            for target in targets:
                print(f"{state} --{symbol}--> {target}")
                has_transitions = True

    if not has_transitions:
        print("No transitions found.")

    print("=" * 45 + "\n")


def print_transition_table(nfa):
    """Print transition table in grid format."""
    states = sorted(nfa.get_all_states(), key=lambda s: s.id)

    print("\n" + "=" * 70)
    print("NFA TRANSITION TABLE")
    print("=" * 70)
    print(f"Start State  : {nfa.start}")
    print(f"Accept State : {nfa.accept}")
    print("-" * 70)

    # Collect all symbols
    symbols = set()
    for state in states:
        symbols.update(state.transitions.keys())
    symbols = sorted(symbols, key=lambda x: ('~' if x == 'ε' else x))

    col_w = 18
    header = f"{'State':<{col_w}}" + "".join(f"{sym:<{col_w}}" for sym in symbols)
    print(header)
    print("-" * len(header))

    for state in states:
        marker = ""
        if state == nfa.start:
            marker += "→"
        else:
            marker += " "

        if state.is_accept:
            marker += "*"
        else:
            marker += " "

        row = f"{marker}{repr(state):<{col_w-2}}"

        for sym in symbols:
            targets = state.transitions.get(sym, [])
            if targets:
                cell = "{" + ", ".join(repr(t) for t in targets) + "}"
            else:
                cell = "∅"
            row += f"{cell:<{col_w}}"

        print(row)

    print("=" * 70 + "\n")


def print_ascii_graph(nfa):
    """Basic ASCII visualization of the NFA."""
    states = sorted(nfa.get_all_states(), key=lambda s: s.id)

    print("\n" + "=" * 45)
    print("NFA ASCII GRAPH")
    print("=" * 45)

    for state in states:
        print(f"[{state_label(state, nfa)}]")

        if not state.transitions:
            print("   (no outgoing transitions)")

        for symbol, targets in state.transitions.items():
            for target in targets:
                print(f"   |-- {symbol} --> [{target}]")

        print()

    print("=" * 45 + "\n")


def print_nfa_report(nfa, title="NFA OUTPUT"):
    """One function to print all readable output together."""
    print("\n" + "#" * 80)
    print(title.center(80))
    print("#" * 80)

    print(f"\nStart State : {nfa.start}")
    print(f"Accept State: {nfa.accept}")
    print(f"Total States: {len(nfa.get_all_states())}")

    print_transition_list(nfa)
    print_transition_table(nfa)
    print_ascii_graph(nfa)

    print("#" * 80 + "\n")


# =========================================================
# MAIN FUNCTION WITH USER INPUT
# =========================================================

def main():
    """Main function to take regex input and output NFA."""
    print("\n" + "=" * 80)
    print("REGULAR EXPRESSION TO NFA CONVERTER".center(80))
    print("=" * 80)
    
    print("\nSupported operators:")
    print("  • |  : Union (or)")
    print("  • *  : Kleene star (zero or more)")
    print("  • +  : One or more")
    print("  • ?  : Optional (zero or one)")
    print("  • () : Grouping")
    print("\nExamples:")
    print("  • a|b     → NFA for 'a or b'")
    print("  • ab      → NFA for 'a followed by b'")
    print("  • a*      → NFA for 'zero or more a's'")
    print("  • (a|b)*c → NFA for '(a or b)* followed by c'")
    print("  • a+b     → NFA for 'one or more a's followed by b'")
    
    while True:
        print("\n" + "-" * 80)
        regex = input("\nEnter a regular expression (or 'quit' to exit): ").strip()
        
        if regex.lower() == 'quit':
            print("\nGoodbye!")
            break
        
        if not regex:
            print("Please enter a valid regular expression.")
            continue
        
        try:
            # Convert regex to NFA
            converter = RegexToNFA()
            nfa = converter.parse_regex(regex)
            
            # Display the NFA
            print_nfa_report(nfa, f"NFA FOR REGEX: '{regex}'")
            
        except Exception as e:
            print(f"\nError: Could not parse regex '{regex}'")
            print(f"Details: {e}")
            print("Please check your regex syntax and try again.")


# =========================================================
# RUN THE PROGRAM
# =========================================================

if __name__ == "__main__":
    main()
