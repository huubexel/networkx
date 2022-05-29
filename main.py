import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Specify where the file is
filepath = './csgo100.csv'

# Read in the csv file with pandas
df = pd.read_csv(filepath, delimiter=',',
                 skiprows=1,                                 # skips the first line of the file
                 encoding='unicode_escape',                  # prevents errors on unknown symbols
                 usecols=['Vertex 1', 'Vertex 2', 'Tweet'],  # only import the columns we use
                 )
df.columns = ['source_user', 'mentioned_user', 'tweet_text']

# create network graph (G)
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


#  TODO: Examine which of the 4 types of graphs we need for our system
