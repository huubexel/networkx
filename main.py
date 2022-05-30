import pandas as pd
import networkx as nx
from matplotlib import pyplot, patches

# Specify where the file is
filepath = './csgo500.csv'

# Read in the csv file with pandas
df = pd.read_csv(
    filepath,
    delimiter=',',
    skiprows=1,                                 # skips the first line of the file
    encoding='unicode_escape',                  # prevents errors on unknown symbols
    usecols=['Vertex 1', 'Vertex 2', 'Tweet'],  # only import the columns we use
    )

df.columns = ['source_user', 'mentioned_user', 'tweet_text']

# create network Digraph (G), see README why a Digraph
G = nx.DiGraph()

for source_user, mentioned_user in zip(df.source_user, df.mentioned_user):

    if source_user != mentioned_user:
        G.add_edge(source_user, mentioned_user)  # An edge is the connection (line) between two nodes (tweets, etc.)


def set_color_and_importance_measure(betw, pos_nodes, graph):
    betweenness_list = []
    degree_list = []
    final_list = []

    # Get node with the highest betweenness
    highest_betweenness = max(betw.values())

    # filling the two lists for later use
    for node in pos_nodes:

        # filling the degree list for later
        if G.degree[node] > 1:
            degree_list.append(graph.degree[node])
        else:
            degree_list.append(0)

        # filling the betweenness list for later
        if betw[node] != 0:
            betweenness_list.append(betw[node] / highest_betweenness)
        else:
            betweenness_list.append(0)

    # Get the highest degree
    highest_degree = max(degree_list)

    for node in range(len(pos_nodes)):
        b_score = betweenness_list[node]
        d_score = 0
        if degree_list[node] != 0:
            d_score = degree_list[node] / highest_degree

        # If both have a score higher than 0 (purple)
        if b_score > 0 and d_score > 0:
            combined_score = (b_score + d_score) / 2
            if combined_score > 0.5:
                color = "#9600FF"
            elif combined_score > 0.2:
                color = "#BC5EFF"
            elif combined_score > 0.1:
                color = "#D294FF"
            else:
                color = "#E7C4FF"

        # degree, importance (green)
        elif d_score > 0:
            if d_score > 0.5:
                color = "#0CFF14"
            elif d_score > 0.3:
                color = "#66FF6B"
            elif d_score > 0.1:
                color = "#A3FFA6"
            else:
                color = "#E8FEEA"
        else:
            color = "#FAFAFA"
        final_list.append(color)

    return final_list
# IK BEN ERACHTER GEKOMEN ALS B HOGER DAN 0 IS, DAN IS D AUTOMATISCH HOGER DAN 0


def nodes_size(importance_list):
    final_list = []
    for importance in importance_list:
        if importance == "#9600FF" or importance == "#0CFF14":
            size = 300
        elif importance == "#BC5EFF" or importance == "#66FF6B":
            size = 220
        elif importance == "#D294FF" or importance == "#A3FFA6":
            size = 150
        else:
            size = 60
        final_list.append(size)

    return final_list


def font_sizes(importance_list):
    final_list = []
    for importance in importance_list:
        if importance == 300:
            size = 40
        elif importance == 220:
            size = 30
        elif importance == 150:
            size = 20
        else:
            size = 5
        final_list.append(size)

    return final_list


# Calculate in degree centrality
in_deg_cent = nx.in_degree_centrality(G)

# Calculate out degree centrality
out_deg_cent = nx.out_degree_centrality(G)

# Calculate betweenness
betweenness = nx.betweenness_centrality(G)

# Calculate closeness
closeness = nx.closeness_centrality(G)

# Add the spring layout
pos = nx.spring_layout(G)

# Create the plot where everything will go on to
fig, ax = pyplot.subplots(1, figsize=(20, 16))  # The first number in figsize is the width, the second is the length
ax.set_title('CSGO network')  # Set a title

# get node color and the color is also an importance measure here
color_list = set_color_and_importance_measure(betweenness, pos, G)
node_size_list = nodes_size(color_list)
font_size_list = font_sizes(node_size_list)

counter = 0
for node, (x, y) in pos.items():
    print(font_size_list[counter])
    pyplot.text(x, y, node, fontsize=font_size_list[counter], ha='center', va='center')
    counter += 1

nx.draw_networkx_edges(G, pos, alpha=0.1)  # Alpha is how see-through the edges will be
nx.draw_networkx_labels(G, pos, font_size=0)
nx.draw_networkx_nodes(
    G,
    pos,
    node_color=color_list     # een lijst geven voor elke node een kleur
)

ax.margins(0, 0)
ax.axis("off")          # No X or Y axis will be shown
pyplot.show()           # Will show the figure

# TODO: post more and clearer comments and add more text to the readme


