import networkx as nx


# def names_extractor():
#     f = open('txt1.txt', 'r')
#     counter = 0
#     char_counter = 0
#     matrix = []
#     full_line = ""
#     for line in f.read().split("\n"):
#         counter += 1
#         if counter != 1:
#             split_line = line.split("\t")[1:]
#             matrix.append(split_line)
#     for line in matrix:
#         joined_line = '\t'.join(line)
#         full_line += joined_line + "\n"
#         for char in line:
#             if char == "0":
#                 char_counter += 1
#         print(char_counter)
#         char_counter = 0
#
#     return full_line
#
#
# def import_function():
#     return nx.read_weighted_edgelist("data.txt", create_using=nx.Graph(), nodetype=int)
#
#
# def main():
#     # Make data matrix
#     data_matrix = names_extractor().rstrip()
#
#     # put matrix in file
#     f = open("data.txt", "w")
#     f.write(data_matrix)
#     f.close()
#
#     # import file with function
#     graph = import_function()
#     print(graph)
#
#
# if __name__ == "__main__":
#     main()

