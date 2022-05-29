import pandas as pd
import networkx as nx
import scipy
import matplotlib as mpl
import matplotlib.pyplot as plt

# Specify where the file is
filepath = './csgo2000.csv'

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

options = {
    "font_size": 9,
    "node_size": 300,
    "node_color": "red",
    "edgecolors": "black",
    "linewidths": 1,
    "width": 1,
}

# You need to figure the figsize before you draw the network
plt.figure(num=1, figsize=(20, 16))      # The first number in figsize is the width, the second is the length

# Draw the network with the Digraph, spring_layout and options included
nx.draw_networkx(G, pos, **options)

# Set margins for the axes so that nodes aren't clipped ???
ax = plt.gca()
ax.margins(0, 0)
plt.axis("off")     # No X or Y axis will be shown
plt.show()          # Will show the figure

# TODO: zorgen dat de bolletjes, zich groter/ kleiner maken afhankelijk van hoe belangrijk ze zijn
# TODO: lijntjes een andere kleur geven afhankelijk van iets
# TODO: Misschien de pijltjes een beetje meer zichbaar maken
# TODO: De naam van belangrijke mensen groter maken
