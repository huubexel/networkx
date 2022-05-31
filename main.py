import pandas as pd
import networkx as nx
from matplotlib import pyplot
from nltk.tokenize import word_tokenize
# TODO: post more and clearer comments and add more text to the readme


def prepare_data():
    # Specify where the file is
    filepath = './csgo2000.csv'

    # Read in the csv file with pandas
    df = pd.read_csv(
        filepath,
        delimiter=',',
        skiprows=1,  # skips the first line of the file
        encoding='unicode_escape',  # prevents errors on unknown symbols
        usecols=['Vertex 1', 'Vertex 2', 'Tweet'],  # only import the columns we use
    )

    df.columns = ['source_user', 'mentioned_user', 'tweet_text']

    # Make a dictionary with the tweet texts and add the user that said them to the tweet
    tweet_library = {}

    # create network Digraph (G), see README why a Digraph
    g = nx.DiGraph()

    for source_user, mentioned_user, tweet_text in zip(df.source_user, df.mentioned_user, df.tweet_text):

        if source_user != mentioned_user:
            g.add_edge(source_user, mentioned_user)  # An edge is the connection (line) between two nodes (tweets, etc.)

        # Add to the tweet_text library
        tweet_library[source_user] = tweet_text

    return g, tweet_library


def calc_centrality_measures(g):
    # Calculate in degree centrality
    in_deg_cent = nx.in_degree_centrality(g)

    # Calculate out degree centrality
    out_deg_cent = nx.out_degree_centrality(g)

    # Calculate betweenness
    betweenness = nx.betweenness_centrality(g)

    # Calculate closeness
    closeness = nx.closeness_centrality(g)

    # Calculate harmonic centrality
    global_reaching_centrality = nx.global_reaching_centrality(g)

    return in_deg_cent, out_deg_cent, betweenness, closeness, global_reaching_centrality, g


def make_plot(g):
    # Add the spring layout
    pos = nx.spring_layout(g)

    # Create the plot where everything will go on to
    fig, ax = pyplot.subplots(1, figsize=(20, 16))  # The first number in figsize is the width, the second is the length
    ax.set_title('CSGO network')  # Set a title
    return pos, ax


def set_color_and_importance_measure(centrality_measure, pos_nodes, g):
    centrality_measure_list = []
    degree_list = []
    final_list = []

    # Get node with the highest betweenness
    highest_betweenness = max(centrality_measure.values())

    # filling the two lists for later use
    for node in pos_nodes:

        # filling the degree list for later
        if g.degree[node] > 1:
            degree_list.append(g.degree[node])
        else:
            degree_list.append(0)

        # filling the betweenness list for later
        if centrality_measure[node] != 0:
            centrality_measure_list.append(centrality_measure[node] / highest_betweenness)
        else:
            centrality_measure_list.append(0)

    # Get the highest degree
    highest_degree = max(degree_list)

    for node in range(len(pos_nodes)):
        b_score = centrality_measure_list[node]
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


def set_font_size(pos, font_size_list):
    counter = 0
    for node, (x, y) in pos.items():
        pyplot.text(x, y, node, fontsize=font_size_list[counter], ha='center', va='center')
        counter += 1


def create_networkx(g, pos, ax, color_list):
    nx.draw_networkx_edges(g, pos, alpha=0.1)  # Alpha is how see-through the edges will be
    nx.draw_networkx_labels(g, pos, font_size=0)
    nx.draw_networkx_nodes(
        g,
        pos,
        node_color=color_list     # een lijst geven voor elke node een kleur
    )

    ax.margins(0, 0)
    ax.axis("off")          # No X or Y axis will be shown
    pyplot.savefig("network.png")
    pyplot.show()           # Will show the figure


def calc_social_words_per_tweet(tweet_lib):
    social_ranking_words_dict = {}

    i_words = ["i", "I", "me", "Me", "my", "My"]
    i_words_set = set()
    we_you_words = ["we", "We", "us", "Us", "our", "Our", "you", "You", "your", "Your"]
    we_you_words_set = set()
    for i in range(len(i_words)):
        i_words_set.add(i_words[i])
    for i in range(len(we_you_words)):
        we_you_words_set.add(we_you_words[i])

    for user_and_tweet in tweet_lib.items():
        i_words_counter = 0
        we_you_words_counter = 0

        tokenized_tweet = word_tokenize(user_and_tweet[1])
        for word in tokenized_tweet:
            if word in i_words_set:
                i_words_counter += 1
            elif word in we_you_words_set:
                we_you_words_counter += 1

        social_ranking_words_dict[user_and_tweet[0]] = {
            "i_words_count": i_words_counter,
            "i_words_prop": calc_proportion(i_words_counter, user_and_tweet[1]),
            "we_you_words_count": we_you_words_counter,
            "we_you_words_prop": calc_proportion(we_you_words_counter, user_and_tweet[1]),
            "tweet": user_and_tweet[1]
        }

    return social_ranking_words_dict


def calc_proportion(counter, tweet):
    return counter / len(tweet)


def linguistic_status(srw_dict):
    linguistic_status_dict = {}
    for key_and_value in srw_dict.items():
        linguistic_status_dict[key_and_value[0]] = 0.5 + key_and_value[1]['we_you_words_prop'] - key_and_value[1]['i_words_prop']
    return linguistic_status_dict


def get_highest_and_lowest(l_s_dict, in_deg, out_deg, between, close):
    lowest = 1
    highest = 0
    name_lowest = ""
    name_highest = ""
    for user_and_score in l_s_dict.items():
        if user_and_score[1] > highest:
            if user_and_score[0] != "drmrainclouds":
                highest = user_and_score[1]
                name_highest = user_and_score[0]
        if user_and_score[1] < lowest:
            lowest = user_and_score[1]
            name_lowest = user_and_score[0]

    return name_highest, highest, between[name_highest], close[name_highest], in_deg[name_highest], out_deg[name_highest], name_lowest, lowest, between[name_lowest], close[name_lowest], in_deg[name_lowest], out_deg[name_lowest]


def print_lowest_and_highest(name_highest, highest_ling_score, between_highest, close_highest, in_deg_highest, out_deg_highest, name_lowest, lowest_ling_score, between_lowest, close_lowest, in_deg_lowest, out_deg_lowest):
    print(name_highest)
    print("{0} highest ling_score".format(highest_ling_score))
    print("{0} highest betweenness".format(between_highest))
    print("{0} highest closeness".format(close_highest))
    print("{0} highest in_degree".format(in_deg_highest))
    print("{0} highest out_degree".format(out_deg_highest))
    print(name_lowest)
    print("{0} lowest ling_score".format(lowest_ling_score))
    print("{0} lowest betweenness".format(between_lowest))
    print("{0} lowest closeness".format(close_lowest))
    print("{0} lowest in_degree".format(in_deg_lowest))
    print("{0} lowest out_degree".format(out_deg_lowest))


def part1(g):
    in_deg_cent, out_deg_cent, betweenness, closeness, global_reaching_centrality, graph = calc_centrality_measures(g)
    pos, ax = make_plot(graph)
    color_list = set_color_and_importance_measure(betweenness, pos, graph)
    node_size_list = nodes_size(color_list)
    font_size_list = font_sizes(node_size_list)
    set_font_size(pos, font_size_list)
    create_networkx(graph, pos, ax, color_list)
    return in_deg_cent, out_deg_cent, betweenness, closeness, global_reaching_centrality


def part2(tw_lib, in_deg, out_deg, between, close, grc):
    s_r_w_dict = calc_social_words_per_tweet(tw_lib)
    ling_stat_dict = linguistic_status(s_r_w_dict)
    name_highest, highest_ling_score, between_highest, close_highest, in_deg_highest, out_deg_highest, name_lowest, lowest_ling_score, between_lowest, close_lowest, in_deg_lowest, out_deg_lowest = get_highest_and_lowest(ling_stat_dict, in_deg, out_deg, between, close)
    print_lowest_and_highest(name_highest, highest_ling_score, between_highest, close_highest, in_deg_highest, out_deg_highest, name_lowest, lowest_ling_score, between_lowest, close_lowest, in_deg_lowest, out_deg_lowest)


def main():
    g, tweet_library = prepare_data()
    in_deg, out_deg, between, close, grc = part1(g)
    part2(tweet_library, in_deg, out_deg, between, close, grc)


if __name__ == "__main__":
    main()
