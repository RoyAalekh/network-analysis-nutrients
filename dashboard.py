import streamlit as st
from analysis.data_analysis import load_data, display_basic_info
from analysis.network_analysis import (
    create_bipartite_network, network_metrics, detect_communities, calculate_betweenness_centrality
)
from visualization.visualizations import (
    basic_network_layout, centrality_visualization, filtered_network_visualization, 
    degree_distribution_histogram, plot_3d_network, animate_pathways
)

def filter_network(df, nutrient_types=None, food_types=None):
    """
    Filter the DataFrame based on selected nutrient and food types.
    """
    if nutrient_types:
        df = df[df['Compound'].isin(nutrient_types)]
    if food_types:
        df = df[df['Food'].isin(food_types)]
    return df

def main():
    st.title("Interactive Nutrient-Food Network Dashboard")

    # Load data
    data_file_path = './data/nutrients.csv'
    df = load_data(data_file_path)

    # Data analysis section
    if st.sidebar.checkbox("Show Data Overview"):
        info = display_basic_info(df)
        st.write("### Data Preview")
        st.dataframe(info["head"])
        st.write("### Summary Statistics")
        st.write(info["description"])
        st.write("### Missing Values")
        st.write(info["missing_values"])
        st.write("### Unique Counts")
        st.write(info["unique_counts"])

    # Filter options
    st.sidebar.header("Filter Options")
    nutrient_types = st.sidebar.multiselect("Select Nutrient Types", options=df['Compound'].unique())
    food_types = st.sidebar.multiselect("Select Food Types", options=df['Food'].unique())
    filtered_df = filter_network(df, nutrient_types, food_types)

    # Network analysis section
    if st.sidebar.checkbox("Generate Network"):
        B = create_bipartite_network(filtered_df)
        centrality_scores = network_metrics(B)
        betweenness_scores = calculate_betweenness_centrality(B)
        communities = detect_communities(B)

        # Display community information
        st.write("### Detected Communities")
        for i, community in enumerate(communities):
            st.write(f"Community {i+1}: {', '.join(community)}")

        # Visualization options
        visualization_type = st.sidebar.radio(
            "Select Visualization Type",
            ["Basic Network Layout", "Centrality Visualization", "Filtered Network", 
             "Degree Distribution Histogram", "3D Network Visualization", "Animate Pathways"]
        )

        if visualization_type == "Basic Network Layout":
            st.write("### Basic Network Layout")
            fig = basic_network_layout(B)
            st.plotly_chart(fig, use_container_width=True)

        elif visualization_type == "Centrality Visualization":
            st.write("### Network Visualization by Centrality")
            fig = centrality_visualization(B, centrality_scores)
            st.plotly_chart(fig, use_container_width=True)

        elif visualization_type == "Filtered Network":
            st.write("### Filtered Network (Top 10% Centrality)")
            fig = filtered_network_visualization(B, centrality_scores, threshold=0.1)
            st.plotly_chart(fig, use_container_width=True)

        elif visualization_type == "Degree Distribution Histogram":
            st.write("### Degree Distribution Histogram")
            degree_distribution_histogram(B)

        elif visualization_type == "3D Network Visualization":
            st.write("### 3D Network Visualization")
            fig = plot_3d_network(B, centrality_scores)
            st.plotly_chart(fig, use_container_width=True)

        elif visualization_type == "Animate Pathways":
            st.write("### Nutritional Pathways Animation")
            start_node = st.sidebar.selectbox("Choose a starting nutrient", options=df['Compound'].unique())
            steps = st.sidebar.slider("Number of steps", min_value=1, max_value=10, value=5)
            animate_pathways(B, start_node, steps)

if __name__ == "__main__":
    main()
