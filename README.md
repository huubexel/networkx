# networkx combined with NodeXL
networkx combined with NodeXL Excel program

## Things to watch out for:
- Make sure that the delimiter of the Excel version you use is a comma,
not a semicolon. Otherwise, pandas will not be able to read the code.

# Edges and nodes
Nodes are the dots, this could be anything from internet-links to whole movies,
in our case they are tweets.

Edges are the lines between the nodes, they are the connections between the nodes.
This could be a comment, retweet or maybe a mention to another person.

# Graphs
There are 4 types of graphs:
- Graph
- DiGraph
- MultiGraph
- MultiDiGraph

### 'Di' or no 'Di'
If the Graph includes 'Di', it means that the edges are 'Di'rected,
it means that the connection (line) between two nodes has a direction, for example
you tweet about Queen Elizabeth, but she won't respond or tweet back or do anything
with the tweet. This is more like an arrow that points from one node to another node.

If the Graph does not include 'Di', it means that there is no direction specified.
The line does not have an arrow pointing towards something, it is just a line, 
just a connection without a direction.

### 'Multi' or no 'Multi'
If the Graph includes 'Multi', it means that you can have more than one connection
(line) between two nodes. A good example would be that there are 2 nodes,
Amsterdam and Brussels, and every connection (line) would be a way to travel from
one city to another. You could do that with train, by car, by foot etc. Now you have
at least three lines running between them, this is multi.

If the Graph does not include 'Multi', it means that it is not possible to have
multiple connections (lines) between the 2 nodes. So there will be just one connection
(line) between the 2 nodes.

### What Graph are we using?
We will be using a DiGraph, why? Because we do not allow for more than one connection
(line) between two nodes, but the connections between the nodes are directional from
one node to another, so there is an arrow pointing from one node to another.

# Layout
For layouts, you have a wide variety of layouts to choose from, we choose the spring
layout, this because it shows what we want to show. The most tweeted about, retweeted,
commented on, etc. persons are on the outskirts and quite hard to reach (made green).
The spring layout highlights the nodes that are most interesting for us to look at 
in this type of network. The people that are in the middle and that are purple are
the people who know these more famous individuals, they are links to other these 
more famous and well know persons, with this kind of layout, we try to highlight 
those persons (links to more famous individuals).

## Spectrum
The spectrum goes from -1 to 1 on the x-axis and same for the y-axis. It also happens
to be that the middle is within -0.5 and 0.5 for both the x- and y-axis.
