import time

import streamlit as st

import networkx as nx
import plotly.graph_objects as go
from matplotlib import pyplot as plt


def basic_network_layout(B: nx.Graph):
    pos = nx.spring_layout(B, k=0.15)
    edge_x, edge_y = [], []
    for edge in B.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')

    node_x, node_y, node_text = [], [], []
    for node in B.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text',
        text=node_text, textposition="bottom center",
        marker=dict(size=10, color='blue'),
        hoverinfo='text')

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(title="Basic Nutrient-Food Network Layout",
                                     showlegend=False, hovermode='closest'))
    return fig


def centrality_visualization(B: nx.Graph, centrality_scores: dict):
    pos = nx.spring_layout(B, k=0.15)
    edge_x, edge_y = [], []
    for edge in B.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), hoverinfo='none', mode='lines')

    node_x, node_y, node_color, node_size, node_text = [], [], [], [], []
    for node in B.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        centrality = centrality_scores.get(node, 0)
        node_size.append(centrality * 100 + 10)  # Size nodes based on centrality
        node_color.append(centrality * 100)
        node_text.append(f"{node} - Centrality: {centrality:.2f}")

    node_trace = go.Scatter(
        x=node_x, y=node_y, mode='markers+text',
        marker=dict(size=node_size, color=node_color, colorscale='Viridis', colorbar=dict(title="Centrality")),
        text=node_text, hoverinfo='text')

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(title="Nutrient-Food Network by Centrality",
                                     showlegend=False, hovermode='closest'))
    return fig


def filtered_network_visualization(B: nx.Graph, centrality_scores: dict, threshold: float = 0.1):
    top_nodes = [node for node, centrality in centrality_scores.items() if centrality >= threshold]
    subgraph = B.subgraph(top_nodes)
    return basic_network_layout(subgraph)  # Reuse the basic layout function to display this subgraph


def degree_distribution_histogram(B: nx.Graph):
    degrees = [degree for _, degree in B.degree()]
    plt.figure()
    plt.hist(degrees, bins=10, color='blue', edgecolor='black')
    plt.title("Degree Distribution of Nutrient-Food Network")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    st.pyplot(plt.gcf())


def plot_3d_network(B: nx.Graph, centrality_scores):
    pos = nx.spring_layout(B, dim=3)  # 3D layout
    node_x, node_y, node_z = [], [], []
    edge_x, edge_y, edge_z = [], [], []
    node_color, node_text, node_size = [], [], []

    # Nodes
    for node in B.nodes():
        x, y, z = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_z.append(z)
        centrality = centrality_scores.get(node, 0)
        node_color.append(centrality * 100)
        node_text.append(f"{node} - Centrality: {centrality:.2f}")
        node_size.append(centrality * 50 + 10)  # Size based on centrality

    node_trace = go.Scatter3d(
        x=node_x, y=node_y, z=node_z,
        mode='markers+text',
        marker=dict(size=node_size, color=node_color, colorscale='Viridis', opacity=0.8),
        text=node_text,
        hoverinfo='text'
    )

    # Edges
    for edge in B.edges():
        x0, y0, z0 = pos[edge[0]]
        x1, y1, z1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_z.extend([z0, z1, None])

    edge_trace = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(width=1, color='#888'),
        hoverinfo='none'
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title="3D Nutrient-Food Network",
                        scene=dict(
                            xaxis=dict(showbackground=False),
                            yaxis=dict(showbackground=False),
                            zaxis=dict(showbackground=False)
                        ),
                        showlegend=False
                    ))
    return fig

def animate_pathways(B: nx.Graph, start_node: str, steps=5):
    """
    Animate pathways from a given nutrient node to food nodes.
    """
    # Initialize Plotly figure
    fig = go.Figure()
    pos = nx.spring_layout(B)

    # Get neighbors iteratively up to the specified number of steps
    visited_nodes = set()
    current_layer = {start_node}

    for step in range(steps):
        next_layer = set()
        edge_x, edge_y, node_x, node_y = [], [], [], []

        for node in current_layer:
            visited_nodes.add(node)
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

            # Add edges to neighbors
            for neighbor in B.neighbors(node):
                if neighbor not in visited_nodes:
                    x1, y1 = pos[neighbor]
                    edge_x.extend([x, x1, None])
                    edge_y.extend([y, y1, None])
                    node_x.append(x1)
                    node_y.append(y1)
                    next_layer.add(neighbor)

        # Update figure for each step
        fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers', marker=dict(color='orange', size=10)))

        # Render the frame in Streamlit
        st.plotly_chart(fig)
        time.sleep(1)  # Delay for animation effect

        current_layer = next_layer  # Move to the next layer of nodes
