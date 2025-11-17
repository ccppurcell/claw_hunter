# Claw Hunter

This is a small personal tool for building a graph interactively and
highlighting induced claws. It can highlight induced subgraphs
isomorphic to any graph, in principle. Future versions will allow
user-defined forbidden induced subgraphs.

I built it with pygame to practise after
completing the python course at
[programming-25.mooc.fi](https://programming-25.mooc.fi) (see the game I submitted at the end of that
course [here](https://github.com/ccppurcell/coin_game)). I will
continue to develop and test this tool as a learning exercise; one
goal for the future is to switch pygame for tkinter or something
similar.

## Installation and usage

Download, cd into the folder and do `python main.py`.

Click to add a vertex. Click a vertex once to start creating an edge.
Click the same vertex again to change your mind; click a different
vertex to complete the edge. Press "u" to undo. If the graph you build
has induced claws, the most recently created will be highlighted. If
not, the most recent induced $H$ will be highlighted. At the moment, $H$
is the line graph of $A_7$ where $A_n$ is obtained from the cycle graph
$C_n$ by adding a pendant edge.

## Dependencies

Currently requires pygame and networkx.

## Future features

- User defined forbidden graphs
- Save and load
- Graph layout options (and drag and drop vertices)
- Switch pygame for tkinter

## Graph theory

Claw-free graphs are widely studied in graph theory. They generalise
line graphs and the polynomial time algorithm for Maximum Matching can
be extended to a polynomial time algorithm for Maximum Independent Set
in claw-free graphs. On the other hand, problems like 3-Colourability,
Maximum Clique and Hamiltonian Cycle are NP-hard; Graph Isomorphism
for claw-free graphs is known to be at least as hard as in the general
case.

In the universe of graph classes closed under deleting vertices (or
hereditary classes), claw-free graphs seem to be on the border between
very simple classes and classes whose structure defies intuitive
explanation.

For more information see the ISGCI page on
[claw-free graphs](https://www.graphclasses.org/lasses/gc_62.html).

