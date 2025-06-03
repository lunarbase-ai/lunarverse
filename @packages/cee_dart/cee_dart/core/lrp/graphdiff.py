# get the adjacency matrices
from ..functions import graphs as fg
from .graph import LRPGraph
import numpy as np
import pandas as pd
from gprofiler import GProfiler
import os

class LRPGraphDiff:
    def __init__(self, LRPGraph1, LRPGraph2, diff_thres=0.6):
        '''
        Initializes the comparison of two LRPGraph objects and computes their differences.

        Args:
            LRPGraph1 (LRPGraph): The first LRPGraph object to compare.
            LRPGraph2 (LRPGraph): The second LRPGraph object to compare.
            diff_thres (float, optional): The threshold for determining significant differences
                in edge attributes. Defaults to 0.6.

        Attributes:
            LRPGraph1 (LRPGraph): The first LRPGraph object.
            LRPGraph2 (LRPGraph): The second LRPGraph object.
            diff_thres (float): The threshold for significant differences.
            adj_diff (numpy.ndarray): The adjacency difference matrix calculated from the two graphs.
            edge_df (pandas.DataFrame): A DataFrame containing edges with differences above the threshold.
            diff_graph (LRPGraph): An LRPGraph object representing the difference graph,
                including significant edges and their attributes.
        '''
        self.LRPGraph1 = LRPGraph1
        self.LRPGraph2 = LRPGraph2
        self.diff_thres = diff_thres
        self.adj_diff = fg.calculate_adjacency_difference(
            self.LRPGraph1, self.LRPGraph2
        )
        self.edge_df = fg.create_edge_dataframe_from_adj_diff(
            self.adj_diff, self.diff_thres
        )
        self.diff_graph = LRPGraph(
            edges_sample_i=self.edge_df,
            source_column="source_node",
            target_column="target_node",
            edge_attrs=["LRP", "LRP_norm"],
            top_n_edges=None,
            sample_ID="Diff. graph",
        )
        self.diff_graph.get_communitites()

    def get_edges_and_nodes_vs_threshold(self):
        '''
        Computes the number of edges and nodes in a graph for varying threshold values
        and stores the results in a DataFrame.

        This method iterates over a range of threshold values from 0.0 to 1.0 with a step
        size of 0.02. For each threshold, it creates an edge DataFrame from the adjacency
        difference matrix, calculates the number of edges, and determines the unique nodes
        involved. The results are stored as a DataFrame with columns for the threshold,
        number of edges, and number of nodes.

        Attributes:
            self.edge_node_df_sizes (pd.DataFrame): A DataFrame containing the threshold
                values, number of edges, and number of nodes for each threshold.

        Returns:
            None
        '''
        edge_node_df_sizes = []
        for diff_thres in np.linspace(0.0, 1.0, 25):
            diff_thres = round(diff_thres, 2)
            edge_df = fg.create_edge_dataframe_from_adj_diff(self.adj_diff, diff_thres)            
            if edge_df.empty:
                num_edges = 0
                num_nodes = 0
            else:
                num_edges = len(edge_df)
                nodes = set(edge_df["source_node"]).union(set(edge_df["target_node"]))
                num_nodes = len(nodes)
                
            edge_node_df_sizes.append((diff_thres, num_edges, num_nodes))
        # convert to dataframe
        self.edge_node_df_sizes = pd.DataFrame(
            edge_node_df_sizes, columns=["threshold", "num_edges", "num_nodes"]
        )



