import pygame
import networkx as nx
from claw_hunter.main import ClawHunter

def test_add_node():

    #init the app
    app = ClawHunter()
    assert app.id == 1
    
    #set the points
    point_1 = (0,0)
    point_2 = (1,1)

    #add nodes
    app.add_node(point_1)
    app.add_node(point_2)

    assert app.id==3

    #set another point
    point_3 = (2,2)

    app.edge_queue=[1]

    app.add_node(point_3)
    assert app.edge_queue == []

    positions = nx.get_node_attributes(app.G, "pos")
    assert app.pos == positions

def test_add_edge():

    #init the app
    app = ClawHunter()

    #add some nodes
    app.add_node((0,0))
    app.add_node((1,1))

    #add an edge
    app.add_edge(1,2)

    assert app.edge_id == 2
    assert app.edge_dict[1] == (1,2)

    edges = list(app.G.edges())
    assert edges == [(1,2)]

def test_undo():

    #init app
    app = ClawHunter()

    #add two nodes
    app.add_node((0,0))
    app.add_node((1,1))

    #add edge
    app.add_edge(1,2)

    app.undo()
    assert app.edge_id == 1
    assert app.edge_dict == {}
    assert app.G.number_of_edges() == 0

    #undo twice to undo vertices
    app.undo()
    app.undo()
    assert app.id == 1
    assert app.G.number_of_nodes() == 0

    #undo once more to check it doesn't crash
    app.undo()
