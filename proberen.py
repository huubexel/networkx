import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

filepath = './csgo.csv'

df = pd.read_csv(filepath,
                 delimiter=',',                             # because we use a .csv
                 skiprows=1,                                # skips the first line of the file
                 encoding='unicode_escape',                 # prevents errors on unknown symbols
                 usecols=['Vertex 1', 'Vertex 2', 'Tweet']  # only import the columns we use
                )
df.columns = ['source_user', 'mentioned_user', 'tweet_text']

# create network graph (G)
G = nx.DiGraph()

for source_user, mentioned_user in zip(df.source_user, df.mentioned_user):
    if source_user != mentioned_user:
        G.add_edge(source_user, mentioned_user)


pos = nx.spring_layout(G)
nx.draw(G, pos)
plt.figure(1, figsize=(1000, 1000), dpi=10)
plt.show()
