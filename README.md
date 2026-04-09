# Regex to NFA Converter ⚙️

A powerful tool built to convert Regular Expressions into Non-deterministic Finite Automata (NFA) using **Thompson’s Construction Algorithm**. This project was developed as part of the Theory of Computation (TOC) curriculum.

---

## 🚀 Overview
This application takes a standard Regular Expression as input, validates it, converts it to postfix notation via the **Shunting Yard Algorithm**, and finally builds an NFA structure complete with $\epsilon$-transitions.

## 🛠 Features
* **Regex Validation:** Ensures balanced parentheses and valid operator placement.
* **Explicit Concatenation:** Automatically transforms `ab` into `a.b` for processing.
* **Infix to Postfix:** Implements the Shunting Yard algorithm to handle operator precedence ($*, ., |$).
* **Thompson’s Construction:** Generates states and transitions (including epsilon moves).
* **NFA Visualization:** Outputs a clear transition table and state map.

---

## 👥 Team Distribution

| Member | Responsibility | Key Tasks |
| :--- | :--- | :--- |
| **Member 1** | **Input & Validation** | Preprocessing, parentheses balancing, explicit dot (`.`) insertion. |
| **Member 2** | **Expression Conversion** | Infix to Postfix conversion using the Shunting Yard algorithm. |
| **Member 3** | **NFA Builder** | Implementation of Thompson's Construction (Union, Star, Concatenation). |
| **Member 4** | **UI & Formatting** | NFA output representation, transition table formatting, and integration. |

---

## 📐 Logic Flow

1. **Input:** User enters a regex, e.g., `a(b|c)*`
2. **Preprocessing:** Converted to `a.(b|c)*`
3. **Postfix:** Converted to `abc|*.` using Shunting Yard.
4. **Thompson's:** Stack-based NFA construction.
5. **Output:** A transition table representing the automaton.



### Example Transition Table
```text
State | Input | Next State
--------------------------
q0    | a     | q1
q1    | ε     | q2
q2    | b     | q3


💻 Tech Stack
Language: [Insert Language, e.g., Java / Python / C++]

Concepts: Finite Automata, Thompson's Construction, Shunting Yard Algorithm.

📥 Installation & Usage
Clone the repository:

Bash
git clone [https://github.com/YourUsername/NU-ITCS-Hub-backend.git](https://github.com/YourUsername/NU-ITCS-Hub-backend.git)
Navigate to the directory:

Bash
cd regex-nfa-converter
Run the application:

Bash
# Replace with your actual run command
python main.py 
📝 Example Output
Input: (a|b)*c

Refined Regex: (a|b)*.c

Postfix Notation: ab|*c.

NFA Result: * Start State: q0

Accept State: q10

📄 License
This project is for educational purposes as part of the University TOC Course.
