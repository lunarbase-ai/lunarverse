import networkx as nx

class CausalGraphBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()

    def update_graph(self, var_1: str, var_2: str, relation: str) -> None:
        """
        Update the graph based on the discovered causal relationship.
        var_1 : str
            The first variable's name
        var_2 : str
            The second variable's name
        reation : str
            The causal relationship between the two variables (0,1), (1,0), (0,0), or (-1,-1)
        
        """
        if relation == '(0,1)':
            self.graph.add_edge(var_1, var_2, weight=1)
            self.graph.add_edge(var_2, var_1, weight=-1)
        elif relation == '(1,0)':
            self.graph.add_edge(var_2, var_1, weight=1)
            self.graph.add_edge(var_1, var_2, weight=-1)
        elif relation == '(0,0)':
            # Add nodes restrictions (weighted as -1)
            self.graph.add_edge(var_1, var_2, weight=-1)
            self.graph.add_edge(var_2, var_1, weight=-1)
        else:
            # For '(-1,-1)', we only add the nodes without edges
            self.graph.add_node(var_1)
            self.graph.add_node(var_2)

    def get_graph(self) -> any:
        """
        Return the current graph as a JSON serializable object (node-link format).
        """
        return nx.node_link_data(self.graph)