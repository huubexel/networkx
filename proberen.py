import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Open file (straight from NodeXL)
# import -> from search twitter network -> export edges page as csv

filepath = './csgo2000.csv'

df = pd.read_csv(filepath, delimiter=',',
                skiprows=1, # skips the first line of the file
                encoding='unicode_escape', # prevents errors on unknown symbols
                usecols=['Vertex 1', 'Vertex 2', 'Tweet'], # only import the columns we use
                )
df.columns = ['source_user', 'mentioned_user', 'tweet_text']

# create network graph (G)

G = nx.DiGraph()

for source_user, mentioned_user in zip(df.source_user, df.mentioned_user):

    if source_user != mentioned_user:
        G.add_edge(source_user, mentioned_user)


print(G)