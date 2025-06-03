import networkx as nx
import numpy as np
import pandas as pd
import os

def get_edges_subset(edges_sample_i, top_n_edges=None):
    """
    Get the top `n_` edges based on the LRP values, or all edges if `n_` is not specified.

    Parameters:
    edges_sample_i (pd.DataFrame): DataFrame containing edges and their LRP values.
    n_ (int, optional): Number of top edges to retain. If None, all edges are retained.

    Returns:
    pd.DataFrame: Subset of edges containing the top `n_` rows, or all rows if `n_` is None.
    """
    if top_n_edges is None:
        return edges_sample_i.copy()

    return edges_sample_i.iloc[:top_n_edges, :].copy()


def normalize_lrp(edges_temp):
    """
    Normalize the LRP values in the edges DataFrame.

    Parameters:
    edges_temp (pd.DataFrame): DataFrame containing edges with LRP values.

    Modifies:
    Adds a new column 'LRP_norm' with normalized LRP values.
    """
    if "LRP" not in edges_temp.columns:
        print('edges_temp head: \n', edges_temp.head())
        raise ValueError("The input DataFrame must contain a column named 'LRP'.")
        
    edges_temp["LRP_norm"] = edges_temp["LRP"] / edges_temp["LRP"].max()

    return edges_temp

class LRPGraph:
    """
    A class to represent and process a graph based on an edge list. 
    It includes functionality to compute adjacency and Laplacian matrices, 
    derive Laplacian embeddings, and create fixed-size embeddings for nodes.

    This class is designed for applications involving graph-based machine learning
    or analysis tasks that require structured representations of nodes and edges.
    """
    def __init__(self, edges_sample_i, source_column, target_column, edge_attrs, embedding_dim=2, top_n_edges=None, sample_ID = None):
        """
        Initialize the LRPGraph object and compute embeddings.
        
        Parameters:
            edges_sample_i (DataFrame): The edge list dataframe containing graph edges. Each row represents an edge between two nodes.
            source_column (str): Name of the source node column in the edge list dataframe.
            target_column (str): Name of the target node column in the edge list dataframe.
            edge_attrs (list): List of edge attributes to include in the graph. These attributes are added as edge weights or metadata.
            embedding_dim (int): Dimension of the Laplacian embedding (default is 2). Determines the size of the embedding vector for each node.
            top_n_edges (int, optional): Number of top edges to retain based on LRP values. If None, all edges are retained.
            sample_ID (any, optional): Identifier for the graph instance, useful for tracking or indexing.
        """

        self.sample_ID = sample_ID
        self.top_n_edges = top_n_edges
        edges_temp = get_edges_subset(edges_sample_i, top_n_edges)
        print('Edges temp shape: ', edges_temp.shape)
        edges_temp = normalize_lrp(edges_temp)


        self.G = nx.from_pandas_edgelist(
            edges_temp,
            source=source_column,
            target=target_column,
            edge_attr=edge_attrs,
        )
        # Add normalized weights as edge attributes
        nx.set_edge_attributes(
            self.G, {(u, v): d["LRP_norm"] for u, v, d in self.G.edges(data=True)}, "weight"
        )
        # Laplacian embedding dimensions 
        self.embedding_dim = embedding_dim
        self.all_nodes = None

        # get node names that do not include the node type
        self.node_names_no_type = sorted(list(set(node.rsplit('_', 1)[0] for node in self.G.nodes)))
        self.map_gene_aliases()        

        """
        This graph represents the structure of relationships between nodes as defined 
        by the `edges` dataframe. The `edge_attrs` parameter includes specific attributes 
        such as weights (e.g., "LRP" or "LRP_norm") that quantify the strength or significance 
        of the relationships. These attributes are particularly useful in applications requiring 
        weighted adjacency or customized graph analysis.
        """

        # Compute fixed size embedding
        '''fixed_embedding = self.create_fixed_size_embedding(
            self.laplacian_embedding,
            all_nodes,
            list(self.G.nodes()),            
            self.embedding_dim
        )

        self.fixed_laplacian_embedding = fixed_embedding
        self.fixed_laplacian_embedding_flattened = fixed_embedding.ravel()

        self.max_nodes = len(all_nodes)'''
     

    def map_gene_aliases(self, alias_file_path = 'aliases.csv'):
            """
            Maps gene aliases from a CSV file to the genes in the current object.
            This method reads a CSV file containing gene aliases and creates a mapping
            between the genes in `self.node_names_no_type` and their corresponding aliases.
            It also generates a sorted list of unique aliases.
            Args:
                alias_file_path (str, optional): The path to the CSV file containing gene aliases.
                    Defaults to 'aliases.csv'. The file is expected to have a column named 'aliases',
                    where each entry is a string representation of a list of aliases.
            Attributes:
                self.aliases (pd.DataFrame): The DataFrame containing the gene aliases read from the file.
                self.node_names_aliase_dict (dict): A dictionary where keys are gene names from
                    `self.node_names_no_type` and values are lists of their corresponding aliases.
                self.node_names_aliases (list): A sorted list of unique aliases across all genes.
            Raises:
                FileNotFoundError: If the specified alias file does not exist.
                ValueError: If the 'aliases' column in the CSV file contains invalid data.
            Example:
                Given a CSV file with the following content:
                ```
                aliases
                "['geneA', 'geneA_alias1', 'geneA_alias2']"
                "['geneB', 'geneB_alias1']"
                ```
                and `self.node_names_no_type = ['geneA', 'geneB', 'geneC']`,
                the method will produce:
                self.node_names_aliase_dict = {
                    'geneA': ['geneA', 'geneA_alias1', 'geneA_alias2'],
                    'geneB': ['geneB', 'geneB_alias1'],
                    'geneC': ['geneC']
                }
                self.node_names_aliases = ['geneA', 'geneA_alias1', 'geneA_alias2', 'geneB', 'geneB_alias1', 'geneC']
            """
            
            alias_file_path = os.path.join(os.path.dirname(__file__), 'aliases.csv')
            gene_aliases = pd.read_csv(alias_file_path)
            self.aliases = gene_aliases
            #print(gene_aliases)
            gene_alias_dict = {}
            # Iterate through each gene in the gene list
            for gene in self.node_names_no_type:
                
                matching_rows = gene_aliases[gene_aliases['aliases'].apply(lambda aliases: gene in eval(aliases) if pd.notna(aliases) else False)]
                
                aliases = matching_rows['aliases'].apply(eval).explode().dropna().unique().tolist()
                
                if gene not in aliases:
                    aliases.append(gene)
                
                gene_alias_dict[gene] = aliases
            unique_aliases = sorted(list(set(alias for aliases in gene_alias_dict.values() for alias in aliases)))
            self.node_names_aliase_dict = gene_alias_dict
            self.node_names_aliases = unique_aliases

    def get_adjacency_and_laplacian(self):
        """
        Compute the adjacency and Laplacian matrices for the graph.
        
        Returns:
            tuple:
                A (ndarray): Weighted adjacency matrix of the graph. Entries represent edge weights normalized by "LRP_norm".
                L (ndarray): Laplacian matrix of the graph, calculated as D - A, where D is the degree matrix.

        Details:
            - The adjacency matrix does not include self-loops unless explicitly defined in the input edge list.
            - This method assumes an undirected graph. For directed graphs, the adjacency matrix is computed
              considering only the directionality provided in the input data.
        """
        A = nx.to_numpy_array(self.G, weight="LRP_norm")
        degrees = np.sum(A, axis=1)
        D = np.diag(degrees)
        L = D - A
        self.A = A
        self.L = L

    def compute_laplacian_embedding(self):
        """
        Compute the Laplacian embedding of the graph.
        
        Parameters:
            L (ndarray): Laplacian matrix of the graph. Assumes the matrix is symmetric and real-valued.
        
        Returns:
            ndarray: Laplacian embedding of the graph. Contains the eigenvectors corresponding to the smallest non-zero eigenvalues.

        Details:
            The eigenvalues and eigenvectors are computed using `numpy.linalg.eigh`, which is optimized 
            for symmetric (Hermitian) matrices. The method assumes the Laplacian matrix is symmetric 
            and all its eigenvalues are real, ensuring numerical stability and meaningful embeddings.
        """
        self.get_adjacency_and_laplacian()

        eigenvalues, eigenvectors = np.linalg.eigh(self.L)
        idx = np.argsort(eigenvalues)
        eigenvectors = eigenvectors[:, idx]
        self.laplacian_embedding = eigenvectors[:, 1 : self.embedding_dim + 1]
        
    def create_fixed_size_embedding(self, all_nodes):
        """
        Create a fixed-size embedding matrix for the graph.
        
        Parameters:
            all_nodes (list): List of all possible nodes in the graph. Used to map embeddings to a consistent order.
                    
        Returns:
            ndarray: Fixed-size embedding matrix of shape (len(all_nodes), embedding_dim), with rows corresponding to nodes in all_nodes.

        Details:
            Nodes in the graph are matched with rows in the fixed-size embedding matrix 
            based on their order in `all_nodes`. Each node's embedding is placed in 
            the row corresponding to its position in `all_nodes`. If a node in the graph 
            does not exist in `all_nodes`, its embedding remains as zeros. The resulting 
            matrix ensures a consistent mapping of nodes to embeddings across graphs of varying sizes.
        """
        # Create a zero matrix of maximum size
        fixed_embedding = np.zeros((len(all_nodes), self.embedding_dim))
        
        # Create mapping of node positions
        node_to_idx = {node: idx for idx, node in enumerate(all_nodes)}
        
        # Fill in the embedding values for existing nodes
        for idx, node in enumerate(self.G.nodes()):
            if node in node_to_idx:
                fixed_embedding[node_to_idx[node]] = self.laplacian_embedding[idx]
                
        self.fixed_size_embedding = fixed_embedding

    def ravel_fixed_size_embedding(self):
        """
        Ravel the fixed-size embedding matrix to a 1D array.

        Returns:
            ndarray: 1D array of the raveled fixed-size embedding matrix.
        """
        if hasattr(self, 'fixed_size_embedding'):
            self.raveled_fixed_size_embedding = self.fixed_size_embedding.ravel()
        else:
            raise AttributeError("The fixed-size embedding has not been created yet.")


    def create_fixed_size_adjacency_matrix(self, all_nodes):
        """
        Create a fixed-size adjacency matrix for a graph with a consistent 
        node order defined by all_nodes.

        Parameters:
            graph (networkx.Graph): The input graph.
            all_nodes (list): List of all possible nodes. Defines the consistent 
                            order of nodes for the adjacency matrix.

        Returns:
            ndarray: Fixed-size adjacency matrix of shape (len(all_nodes), len(all_nodes)).
                    Each entry (i, j) corresponds to the edge weight between nodes 
                    `all_nodes[i]` and `all_nodes[j]`. If no edge exists, the value is 0.
        """
        # Initialize an empty adjacency matrix
        size = len(all_nodes)
        adjacency_matrix = np.zeros((size, size), dtype=float)

        # Create a mapping of node to its index in all_nodes
        node_to_idx = {node: idx for idx, node in enumerate(all_nodes)}

        # Fill in the adjacency matrix based on edges in the graph
        for u, v, data in self.G.edges(data=True):
            if u in node_to_idx and v in node_to_idx:
                i, j = node_to_idx[u], node_to_idx[v]
                weight = data.get('weight', 1.0)  # Default weight is 1 if not provided
                adjacency_matrix[i, j] = weight
                adjacency_matrix[j, i] = weight  # Ensure the matrix is symmetric for undirected graphs

        self.fixed_size_adjacency_matrix = adjacency_matrix

    def get_communitites(self):
        """
        Identifies communities in the graph using the Louvain method and stores the result in a DataFrame.
        This method uses the Louvain algorithm to detect communities within the graph `self.G`. It then creates a 
        DataFrame where each row corresponds to a node and its associated community. The DataFrame is stored in 
        the `self.communitites` attribute.
        Returns:
            None
        """
        partition = nx.community.louvain_communities(self.G )
        partition_sorted = sorted(partition, key=len, reverse=True)
        partition_dict = {i+1: community for i, community in enumerate(partition_sorted)}

        community_df = pd.DataFrame([(node, community) for community, nodes in partition_dict.items() for node in nodes], columns=['node', 'community'])
        self.communitites = community_df