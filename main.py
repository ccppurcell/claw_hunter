import pygame
import networkx as nx
import math
from itertools import combinations
import claw_hunter.graph_generators as gg

claw = nx.complete_bipartite_graph(1,3)
class ClawHunter:
    def __init__(self):
        pygame.init()

        #initialise the graph
        self.G = nx.Graph()

        #intialise nodes
        self.pos = {} #FIXME:rename node_coords
        self.id = 1 #FIXME: rename node_id

        #initialise edges
        self.edge_id = 1
        self.edge_queue = []
        self.edge_dict = {}

        #display parameters
        self.node_radius = 12
        self.edge_w = 4
        self.highlight_radius = 20
        self.highlight_w = 10

        #undo string FIXME: rename?
        self.node_or_edge = ""

        #define window
        self.width,self.height = 600,400
        self.window = pygame.display.set_mode(
                (self.width,self.height)
                )
        pygame.display.set_caption("Claw hunter")

        #define colours
        self.background_colour = (0,0,0)
        self.red = (213,94,0)
        self.blue = (0,114,178)
        self.yellow = (240,228,66)

        #extra graph to check; this is the line graph of A_7 where A_n
        #is obtained from the cycle C_n by adding a pendant edge
        self.forb_H=gg.line_of_apple_graph(7)

        #lists of forbidden graphs to check
        #FIXME currently these are lists of lists, should be lists of
        #tuples instead
        self.claws=[]
        self.Hs=[]
        self.clock = pygame.time.Clock()

    def add_node(self,pos):
        '''adds a node at a given position'''

        #add the node to the networkx graph
        self.G.add_node(self.id,pos=pos)

        #update the dict of positions
        self.pos = nx.get_node_attributes(self.G,'pos')

        #set the next id
        self.id+=1

        #reset edge queue
        self.edge_queue=[]

        #records node addition to undo string
        self.node_or_edge+="n"

    def add_edge(self,node1,node2):
        '''adds an edge between given nodes'''

        self.edge_dict[self.edge_id] = (node1,node2)

        #add the edge to the networkx graph
        self.G.add_edge(node1,node2,id=self.edge_id)
        self.edge_id+=1

        #records edge addition to undo string
        self.node_or_edge+="e"

        #check for claws FIXME: this double counts?
        self.find_claw(node1)
        self.find_claw(node2)
        self.find_H(node1,node2)

        self.update_claws()
        self.update_Hs()

    #FIXME: only need to check number of edges?
    def update_claws(self):
        self.claws = [c for c in self.claws if self.is_claw(c)]

    #FIXME: only need to check number of edges?
    def update_Hs(self):
        self.Hs = [h for h in self.Hs
                   if nx.is_isomorphic(
                       self.G.subgraph(h),
                       self.forb_H)
                   ]

    def run(self):
        '''run the program'''

        #for now run() is somewhat redundant but useful in future?
        self.main_loop()

    def main_loop(self):
        '''the main loop of the gui'''

        while True:
            self.check_events()
            self.update_window()

            #60fps
            self.clock.tick(60)

    def check_events(self):
        '''handle clicks, keypresses, quitting'''

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    #check if clicked inside node
                    for node in self.G.nodes:

                        #distance between current node and click
                        dist = math.dist(event.pos,self.pos[node])

                        #select a node to start an edge
                        if dist<self.node_radius*1.2:
                            if node in self.edge_queue:
                                self.edge_queue = []
                            else:
                                self.edge_queue.append(node)
                            break

                        #don't create overlapping nodes
                        elif dist<self.node_radius*2.1:
                            break

                    else:
                        #if clicked on black, add node
                        self.add_node(event.pos)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_u:
                    self.undo()

            #add edges if two nodes queued
            if len(self.edge_queue)==2:
                source = self.edge_queue[0]
                sink = self.edge_queue[1]
                self.add_edge(source,sink)
                #reset edge queue
                self.edge_queue = []

    def update_window(self):
        #paint the background
        self.window.fill(self.background_colour)

        if self.claws:
            #highlight the newest claw
            a_claw=self.claws[-1]
            #centre is always 0th node
            centre=self.pos[a_claw[0]]

            #draw the highlight under claw
            for node in a_claw:
                pos=self.pos[node]
                pygame.draw.circle(self.window, self.yellow, pos,
                        self.highlight_radius)
                pygame.draw.line(
                        self.window, self.yellow, centre, pos,
                        self.highlight_w)

        #highlight the newest forbidden H
        elif self.Hs:

            #init the newest H
            last_H = self.Hs[-1]
            last_H_edges = self.G.subgraph(last_H).edges()

            #draw the node highlights
            for node in last_H:
                pos = self.pos[node]
                pygame.draw.circle(
                        self.window, self.yellow,
                        pos, self.highlight_radius)

            #draw the edge highlights
            for edge in last_H_edges:
                start = self.pos[edge[0]]
                end = self.pos[edge[1]]
                pygame.draw.line(
                        self.window, self.yellow,
                        start, end, self.highlight_w)

        #FIXME:highlight selected node and line from it to cursor

        #draw the edges over any highlight
        for edge in self.G.edges:
            start = self.pos[edge[0]]
            end = self.pos[edge[1]]
            pygame.draw.line(
                    self.window, self.blue, start, end, self.edge_w
                    )

        #draw the nodes
        for node in self.G.nodes:
            pos = self.pos[node]
            pygame.draw.circle(self.window, self.red, pos,
                    self.node_radius)

        #update the full display
        pygame.display.flip()

    def find_claw(self,node1):
        if self.G.degree(node1)<3:
            return None
        for S in combinations(self.G.neighbors(node1),3):
            nodes = [node1]+list(S)
            if nodes in self.claws:
                continue
            if self.is_claw(nodes):
                self.claws.append(nodes)

    def find_H(self,node1,node2):
        size = self.forb_H.number_of_nodes()
        rest = set(self.G.nodes()) - {node1, node2}
        for S_rest in combinations(rest, size-2):
            S = (node1, node2) + S_rest
            G_S = self.G.subgraph(S)
            if nx.is_isomorphic(G_S, self.forb_H):
                self.Hs.append(list(S))

    def is_claw(self, nodes):
        H = self.G.subgraph(nodes)
        return nx.is_isomorphic(H, claw)

    def undo(self):
        #if nothing to undo
        if not self.G.nodes():
            return

        #pop last addition
        last_addition = self.node_or_edge[-1]
        self.node_or_edge = self.node_or_edge[:-1]

        #if previous action was add node
        if last_addition=="n":
            self.id-=1
            self.G.remove_node(self.id)

        #if previous action was add edge
        elif last_addition=="e":
            self.edge_id-=1
            e = self.edge_dict[self.edge_id]

            #FIXME group these into a delete_edge() method
            self.G.remove_edge(*e)
            self.edge_dict.pop(self.edge_id,None)

        self.update_claws()
        self.update_Hs()

if __name__ == "__main__":
    application = ClawHunter()
    application.run()
