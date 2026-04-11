# =========================
# NFA Visualization (Graphviz)
# =========================

from graphviz import Digraph
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

def visualize_nfa(nfa, filename="nfa_graph"):
    """
    Renders the NFA as a directed graph using Graphviz.
    - Left-to-right layout (rankdir=LR)
    - Start state has an invisible incoming arrow
    - Accept state is a double circle
    - Parallel edges (same src→dst) are merged into one label
    Saves as PNG and displays inline with Matplotlib.
    """

    dot = Digraph(name="NFA", format="png")
    dot.attr(rankdir="LR", bgcolor="white", fontname="Arial")
    dot.attr("node", fontname="Arial", fontsize="12")
    dot.attr("edge", fontname="Arial", fontsize="11")

    states = sorted(nfa.get_all_states(), key=lambda s: s.id)

    # ── Invisible entry arrow for start state 
    dot.node("__start__", shape="none", label="", width="0", height="0")
    dot.edge("__start__", repr(nfa.start), arrowhead="normal")

    # ── Draw all states 
    for state in states:
        if state == nfa.accept:
            # Accept state → double circle, filled light green
            dot.node(
                repr(state),
                shape="doublecircle",
                style="filled",
                fillcolor="#d4edda",
                color="#28a745",
                penwidth="2"
            )
        elif state == nfa.start:
            # Start state → filled light blue
            dot.node(
                repr(state),
                shape="circle",
                style="filled",
                fillcolor="#cce5ff",
                color="#004085",
                penwidth="2"
            )
        else:
            # Regular state
            dot.node(
                repr(state),
                shape="circle",
                style="filled",
                fillcolor="#f8f9fa",
                color="#6c757d"
            )

    # ── Collect and merge parallel edges 
    # edges[(src, dst)] = list of symbols
    edges = {}
    for state in states:
        for symbol, targets in state.transitions.items():
            for target in targets:
                key = (repr(state), repr(target))
                if key not in edges:
                    edges[key] = []
                edges[key].append(symbol)

    # ── Draw edges 
    for (src, dst), symbols in edges.items():
        label = ", ".join(sorted(symbols))
        is_epsilon = label == "ε"
        dot.edge(
            src, dst,
            label=label,
            style="dashed" if is_epsilon else "solid",
            color="#999999" if is_epsilon else "#333333",
            fontcolor="#666666" if is_epsilon else "#000000"
        )

    # ── Render
    output_path = dot.render(filename, cleanup=True)   # saves filename.png
    print(f"NFA graph saved to: {output_path}")

    # ── Display with Matplotlib 
    img = mpimg.imread(output_path)
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.imshow(img)
    ax.axis("off")
    ax.set_title(
        f"NFA — Start: {nfa.start}   Accept: {nfa.accept}",
        fontsize=13, fontweight="bold", pad=12
    )
    plt.tight_layout()
    plt.show()