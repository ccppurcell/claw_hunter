import networkx as nx

def net_graph(i:int, j:int, k:int):
    if i<0 or j<0 or k<0:
        raise TypeError("Parameters must be non-negative")
    P_1 = nx.path_graph(i+1)
    P_2 = nx.path_graph(j+1)
    P_3 = nx.path_graph(k+1)
    G = nx.disjoint_union(P_1, nx.disjoint_union(P_2,P_3))
    G.add_edge(0,i+1)
    G.add_edge(i+1,i+j+2)
    G.add_edge(i+j+2,0)

    return G

def bull_graph(i,j):
    return net_graph(i,j,0)

def paw_graph(i):
    return net_graph(i,0,0)

def phi_graph(k):
    if k<1:
        raise TypeError("Parameter must be at least 1")

    return nx.barbell_graph(3,k-1)

def line_of_apple_graph(n):
    if n<3:
        raise TypeError("Parameter must be at least 3")
    G=nx.cycle_graph(n)
    G.add_node(n)
    G.add_edge(0,n)
    G.add_edge(n-1,n)
    return G

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    Phi3=phi_graph(3)
    nx.draw(Phi3)
    plt.show()
