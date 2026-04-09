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
```
---

---

## 💻 Tech Stack

- **Language:** Python
- **Concepts:** Finite Automata, Thompson's Construction, Shunting Yard Algorithm

---

## 📥 Installation & Usage

**1. Clone the repository**

```bash
git clone https://github.com/FarahAwadalla/Regex-to-NFA-.git
```

**2. Navigate to the directory**

```bash
cd Regex-to-NFA-
```

**3. Run the application**

```bash
python main.py
```

---

## 📝 Supported Operators

| Operator | Meaning |
|:---:|:---|
| `\|` | Union (a or b) |
| `*` | Kleene Star (zero or more) |
| `+` | One or more |
| `?` | Optional (zero or one) |
| `()` | Grouping |
| `ε` | Epsilon (empty string) |

---

## 📄 License

This project is for educational purposes as part of the CSCI419 Theory of Computation course — Nile University.
