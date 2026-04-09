# Infix --> Postfix
def regex_to_postfix(regex):
    precedence = {'*': 3, '.': 2, '|': 1}

    output = ""
    stack = []

    for char in regex:

        # Operand (letters, digits, ε)
        if char.isalnum() or char == 'ε':
            output += char

        # Opening bracket
        elif char == '(':
            stack.append(char)

        # Closing bracket
        elif char == ')':
            while stack and stack[-1] != '(':
                output += stack.pop()
            stack.pop()

        # Operator (* . |)
        else:
            while (stack and stack[-1] != '(' and
                   precedence.get(stack[-1], 0) >= precedence.get(char, 0)):
                output += stack.pop()

            stack.append(char)

    # Pop remaining operators
    while stack:
        output += stack.pop()

    return output