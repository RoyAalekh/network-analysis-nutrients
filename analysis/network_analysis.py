import networkx as nx
import pandas as pd


# Create a bipartite network from the data
def create_bipartite_network(df: pd.DataFrame) -> nx.Graph:
    """
    Create a bipartite network from the data
    
    Parameters:
    ----------
    df : pd.DataFrame
        DataFrame containing the data
    
    Returns:
    -------
    B : nx.Graph
        Bipartite network
    """
    B = nx.Graph()
    for _, row in df.iterrows():
        nutrient, food = row[0], row[1]
        B.add_node(nutrient, bipartite=0)
        B.add_node(food, bipartite=1)
        B.add_edge(nutrient, food)
    return B


# Calculate network metrics
def network_metrics(B: nx.Graph) -> dict:
    """
    Calculate network metrics for a bipartite network
    
    Parameters:
    ----------
    B : nx.Graph
        Bipartite network
    
    Returns:
    -------
    centrality : dict
        Dictionary containing centrality scores for each node in the network
    """
    centrality = nx.degree_centrality(B)
    return centrality


from networkx.algorithms import community


def detect_communities(B: nx.Graph) -> list:
    """
    Detect communities in the network using the Louvain method.

    Parameters:
    ----------
    B : nx.Graph
        Bipartite network

    Returns:
    -------
    communities : list of sets
        List of sets, each containing nodes that form a community
    """
    # Using greedy modularity for community detection
    communities = community.greedy_modularity_communities(B)
    return communities


def calculate_betweenness_centrality(B: nx.Graph) -> dict:
    """
    Calculate betweenness centrality for nodes in the network

    Parameters:
    ----------
    B : nx.Graph
        Bipartite network

    Returns:
    -------
    centrality : dict
        Dictionary of nodes with their betweenness centrality scores
    """
    return nx.betweenness_centrality(B)
