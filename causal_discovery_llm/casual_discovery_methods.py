import pandas as pd
import numpy as np
import networkx as nx
from causallearn.search.ConstraintBased.PC import pc
from causallearn.search.ConstraintBased.FCI import fci
from causallearn.search.ScoreBased.GES import ges
from causallearn.search.FCMBased import lingam
from causallearn.search.FCMBased.PNL.PNL import PNL
from causallearn.search.Granger.Granger import Granger
from causallearn.utils.PCUtils.BackgroundKnowledge import BackgroundKnowledge
from causallearn.graph.GraphNode import GraphNode
from causallearn.search.HiddenCausal.GIN.GIN import GIN
from causallearn.search.PermutationBased.GRaSP import grasp


## Utilities -----------------------------------------------------
def _parse_background_knowledge(background_knowledge):
    """ 
    Parse the background knowledge into a BackgroundKnowledge object.
    
    Args:
        background_knowledge (dict): A dictionary containing the background knowledge.
            The dictionary should have the following structure:
            
            {
                ...
                'links': [
                    {
                        'source': str,
                        'target': str,
                        'weight': int (optional - only checks for (-1) weights)
                                -1: (0, 0) - Means there is NO causation whatsoever
                    },
                    ...
                ],
                ...
            }
    """
    bk = BackgroundKnowledge()
    if(background_knowledge is not None):
        # Add required and forbidden edges
        for link in background_knowledge['links']:
            source = link['source']
            target = link['target']
            # Check weights
            if( ('weight' in link.keys()) and link['weight'] == -1):
                # Means there is NO causation from A -> B
                bk.add_forbidden_by_node(
                    GraphNode(source), GraphNode(target))
            else:
                # Means there is a causal relationship A -> B
                bk.add_required_by_node(
                    GraphNode(source), GraphNode(target))
    else:
        # No background knowledge
        return None
    return bk

## Constraint Based -----------------------------------------------------

# -- PC 
def pc_algorithm(
    data: pd.DataFrame,
    alpha=0.05,
    background_knowledge=None) -> str:
    """ Run PC algorithm
    data: pandas dataframe
    alpha: significance level = 0.05
    background_knowledge: background knowledge = None
    
    returns:
        dict: dictionary with the graph in node-link format
    """
    
    bk = _parse_background_knowledge(background_knowledge)
        
    cg = pc(
        data.values,
        alpha=alpha,
        background_knowledge=bk,
        node_names=data.columns)
    
    # back to node-link format
    dg = nx.node_link_data(nx.DiGraph())

    dg['nodes'] = list(map(lambda x: {'id': x}, data.columns))
    for i in range(len(cg.G.graph)):
        for j in range(len(cg.G.graph)):
            if(cg.G.graph[i,j] == -1 and cg.G.graph[j, i] == 1):
                dg.get('links').append({
                    'weight': 1,
                    'source': data.columns[i],
                    'target': data.columns[j]
                })
            elif(cg.G.graph[i,j] == 1 and cg.G.graph[j, i] == 1):
                dg.get('links').append({
                    'weight': 0,
                    'source': data.columns[i],
                    'target': data.columns[j]
                })
            else:
                dg.get('links').append({
                    'weight': -1,
                    'source': data.columns[i],
                    'target': data.columns[j]
                })
    # cg.to_nx_graph()
    # dg = nx.node_link_data(cg.nx_graph.to_directed())
    # dg['nodes'] = list(
    #     map(lambda x:
    #         {'id': cg.labels[x['id']]},  dg['nodes'] ))
    # dg['links'] = list(
    #     map(lambda x:
    #         {
    #             **x,
    #             'source': cg.labels[x['source']],
    #             'target': cg.labels[x['target']]
    #         },
    #         dg['links'] ))
    return str(dg)

# -- FCI 
def fci_algorithm(
    data: pd.DataFrame,
    alpha=0.05,
    background_knowledge=None) -> dict:
    """ Run FCI algorithm
    data: pandas dataframe
    alpha: significance level = 0.05
    background_knowledge: background knowledge = None

    returns:
        graph: dictionary with the graph in node-link format
    """
    # transform the background knowledge colums into Xi format fro FCI
    transformed_dg = nx.node_link_data(nx.DiGraph())
    if(background_knowledge is not None):
        transformed_dg['nodes'] = list(map(lambda x: {'id': f"X{data.columns.get_loc(x['id'])+1}"}, background_knowledge['nodes']))
        transformed_dg['links'] = list(map(lambda x:
            {
                **x,
                'source': f"X{data.columns.get_loc(x['source'])+1}",
                'target': f"X{data.columns.get_loc(x['target'])+1}",
            }, background_knowledge['links']))
    bk = _parse_background_knowledge(transformed_dg)

    gg, edges = fci(
        data.values,
        alpha=alpha,
        background_knowledge=bk
        )
    
    # back to node-link format
    dg = nx.node_link_data(nx.DiGraph())

    dg['nodes'] = list(map(lambda x: {'id': x}, data.columns))
    for i in range(len(gg.graph)):
        for j in range(len(gg.graph)):
            if(gg.graph[i,j] == -1 and gg.graph[j, i] != 2):
                dg.get('links').append({
                    'source': data.columns[i],
                    'target': data.columns[j]
                })
                
    def _parseEdges(stp):
        indx = stp.split('X')
        if(len(indx) == 2):
            indx = data.columns[int(indx[1])-1]
            return indx
        return indx[0]
    
    dataF = [
        list(
            map(
                _parseEdges,
                str(e).split(' ')
                )
            )
        for e in edges]
    interpretation = '''
        A --> B: A causes B
        A o-> B: B is not an ancestor of A
        A o-o B: No set d-separates A and B
        A <-> B: There is a latent common cause of A and B
    '''
    dg['info'] = {
        'interpretation': interpretation,
        'edges': dataF
    }
    return str(dg)

## PermutationBased
def grasp_algorithm(data: pd.DataFrame, score_func: str):
    G = grasp(data.values, score_func=score_func)
    dg = nx.node_link_data(nx.DiGraph())
    dg['nodes'] = list(map(lambda x: {'id': x}, data.columns))
    for i in range(len(G.graph)):
        for j in range(len(G.graph)):
            if(G.graph[i,j] == -1 and G.graph[j, i] == -1):
                dg.get('links').append({
                    'source': data.columns[i],
                    'target': data.columns[j]
                })

    return str(dg)
                    
    
## ScoreBased
def ges_algorithm(data: pd.DataFrame, score_func: str):
    # default parameters
    Record = ges(data.values, node_names=data.columns, score_func=score_func)
    dg = nx.node_link_data(nx.DiGraph())
    G = Record['G']
    dg['nodes'] = list(map(lambda x: {'id': x}, data.columns))
    for i in range(len(G.graph)):
        for j in range(len(G.graph)):
            if(G.graph[i,j] == -1 and G.graph[j, i] != -1):
                dg.get('links').append({
                    'source': data.columns[i],
                    'target': data.columns[j]
                })
    dg['graph_score'] = Record['score']
    return str(dg)
    
## Func. Constrained Based ----------------------------------------------

# -- Direct LINGAM
def lingam_algorithm(
    data: pd.DataFrame,
    alpha=0.05,
    measure='pwling',
    background_knowledge=None):
    """ Run Direct LINGAM algorithm
    data: pandas dataframe
    alpha: significance level = 0.05
    measure: 'pwling' or 'kernel'
    background_knowledge: background knowledge = None
    
    returns:
        dict: dictionary with the graph in node-link format
    """
    if measure not in ['pwling', 'kernel']:
        raise ValueError(f'Measure must be "pwling" or "kernel", Input was {measure}')
    
    bk: BackgroundKnowledge = _parse_background_knowledge(
                                background_knowledge)    
    # parse the BackgroundKnowledge (bk) for the prior_knowledge
    # parameter for dlingam
    if bk is not None:
        prior_knowledge = np.zeros((data.shape[1], data.shape[1]))
        for i, iv in enumerate(data.columns):
            for j, jv in enumerate(data.columns):
                if(bk.is_forbidden(GraphNode(iv), GraphNode(jv))):
                    prior_knowledge[i, j] = 0
                elif(bk.is_required(GraphNode(iv), GraphNode(jv))):
                    prior_knowledge[i, j] = 1
                else:
                    prior_knowledge[i, j] = -1
    else:
        prior_knowledge = None
        
    model = lingam.DirectLiNGAM(
        prior_knowledge=prior_knowledge,
        measure=measure
        )
    model.fit(data.values)
    adjMat = model.adjacency_matrix_
    G = nx.DiGraph(adjMat)
    dg = nx.node_link_data(G)
    dg['nodes'] = list(
        map(lambda x:
            {'id': data.columns[x['id']]},  dg['nodes'] ))
    dg['links'] = list(
        map(lambda x:
            {
                **x,
                'source': data.columns[x['source']],
                'target': data.columns[x['target']]
            },
            dg['links'] ))
    
    # Remove dg['links'] where the weight is <= alpha
    dg['links'] = list(
        filter(lambda x:
            x['weight'] > alpha,
            dg['links'] ))
    
    return str(dg)

# -- PNL
def pnl_algorithm(
    data: pd.DataFrame,
    x1: str,
    x2: str,
    alpha=0.05):
    """ Run PNL test
    data: pandas dataframe
    x1: string with the name of the first variable
    x2: string with the name of the second variable
    alpha: significance level = 0.05
    
    """
    pnl = PNL()

    # Reshape data
    x = data[x1].values.reshape(-1, 1)
    y = data[x2].values.reshape(-1, 1)

    p_value_forward, p_value_backward = pnl.cause_or_effect(x, y)

    alpha = 0.05
    result = f'The results of Post Non-Linearity Likelihood (PNL) with an alpha = {alpha} are:\n'

    if p_value_forward[0] >= alpha and p_value_backward[0] >= alpha:
        result += f"""
        The PNL method cannot determine a causal relationship between {x1} and {x2}.
        Neither direction shows significant independence (p-values: {p_value_forward[0]:.4f}, {p_value_backward[0]:.4f}).
        This suggests that either there is no causal relationship, or the relationship is too weak to detect.
        """
    elif p_value_forward[0] < alpha and p_value_backward[0] < alpha:
        result += f"""
        The PNL method cannot distinguish the causal direction between {x1} and {x2}.
        Both directions show significant independence (p-values: {p_value_forward[0]:.4f}, {p_value_backward[0]:.4f}).
        This could indicate a complex relationship or fall into a non-identifiable case for the PNL model.
        Further investigation or alternative methods may be needed.
        """
    elif p_value_forward[0] < alpha:
        result += f"""
        The PNL method suggests a causal relationship where {x1} causes {x2}.
        Forward p-value: {p_value_forward[0]:.4f}
        Backward p-value: {p_value_backward[0]:.4f}
        """
    else:
        result += f"""
        The PNL method suggests a causal relationship where {x2} causes {x1}.
        Forward p-value: {p_value_forward[0]:.4f}
        Backward p-value: {p_value_backward[0]:.4f}
        """
        
    return result
    
## Granger Causality ----------------------------------------------------
def granger_algorithm(
    data: pd.DataFrame,
    maxlag=2,
    alpha=0.05,
    background_knowledge=None):
    
    """ Run Granger Causality algorithm
    data: pandas dataframe
    maxlag: maximum number of lags to test
    alpha: significance level = 0.05
    background_knowledge: background knowledge = None

    returns:
        dict: dictionary with the graph in node-link format
    """
    bk = _parse_background_knowledge(background_knowledge)
    
    gr = Granger(maxlag=maxlag, significance_level=alpha)
    adjmat = gr.granger_lasso(data.values)

    # Create a directed graph from the Granger causality results
    # Depending on the maxlag, 
    G = nx.DiGraph()
    edge_info = {}
    for i, col_i in enumerate(data.columns):
        for j, col_j in enumerate(data.columns):
            if i != j:
                # Check if the relationship is allowed by background knowledge
                if bk is None or not bk.is_forbidden(GraphNode(col_i), GraphNode(col_j)):
                    significant_lags = []
                    for lag in range(maxlag):
                        if adjmat[i, j*maxlag + lag]:
                            significant_lags.append(lag + 1)

                    if significant_lags:
                        G.add_edge(col_i, col_j)
                        edge_info[(col_i, col_j)] = significant_lags

    # Convert the graph to node-link format
    dg = nx.node_link_data(G)
    dg['nodes'] = [{'id': node} for node in data.columns]
    dg['links'] = [{
        'source': u,
        'target': v,
        'lags': edge_info.get((u, v), [])}
                        for u, v in G.edges()]

  # Add the full Granger causality matrix for reference
    dg['info'] = f"""
                The Granger Matrix is composed of a Nx(N*maxlag) matrix,
                where N is the number of variables in the dataset.
                Each row represents a variable, and each column represents a
                lagged pair of variables. If the value of the matrix is
                higher than alpha:{alpha}, the variable X_i is Granger
                causal of the variable X_j at the lag k.
                """
    dg['granger_matrix'] = adjmat.tolist()
    return str(dg)

## Hidden Causal Model ----------------------------------------------------
def gin_algorithm(
    data: pd.DataFrame,
    alpha=0.05):
    """ Run Gin algorithm
    data: pandas dataframe
    alpha: significance level = 0.05
    
    Return: str(dict)
    """
    G, K = GIN(data, alpha=alpha)
    dg = nx.node_link_data(nx.DiGraph())

    dg['nodes'] = list(map(lambda x: {'id': x}, data.columns))
    for i in range(len(G.graph)):
        for j in range(len(G.graph)):
            if(G.graph[i,j] == -1 and G.graph[j, i] != 2):
                dg.get('links').append({
                    'source': data.columns[i],
                    'target': data.columns[j]
                })
        
    dg['causal_order'] = K
        
    return str(dg)
    