import os


def get_data():
    """
    file_key is f.e. LLLL9_S2976765
    file_type is 'o', 't', 's' or 'w'
    :return: data = {file_key: {file_type: content from file}}
    In every value are 4 filetypes and 4 contents from files
    """
    file_names = os.listdir('./data')
    data = {}
    while file_names:
        file_name = file_names.pop()
        file_list = file_name.split('_')
        file_key = "_".join(file_list[2:4])  # This is the first 2 things after cie_ so f.e. LLLL9_S2976765
        file_type = file_list[4]
        with open("data/" + file_name) as f:
            text = f.read()
        if file_key in data.keys():
            if file_type in data[file_key].keys():  # If this triggers, you have a duplicate in your data
                print(file_name)
                print(data[file_key][file_type])
            else:
                data[file_key][file_type] = text
        else:
            data[file_key] = {file_type: text}

    return data


# This function determines the point when the interface is changed.
# and adds a new key to the file dict with the index when the interface
# switch and which interface comes first
def splitpoint(data):
    new_data = data
    for key in data. keys():
        interface_list = data[key]['w'].split('¦')
        if '_' not in interface_list[:100]:
            for i in range(len(interface_list)):
                if interface_list[i] == '_':
                    new_data[key]['split'] = [i, "inter1"]
                    break
        else:
            for i in range(1, len(interface_list)+1):
                if interface_list[-i] == '_':
                    new_data[key]['split'] = [len(interface_list) - i, "inter2"]
                    break
    return new_data


# Q1. Which interface is the most efficient?
# Define a measure of efficiency and compare both interfaces in a suitable graph
# A1. which interface switches user the least amount of time
# compared to the amount of characters
# Q2. Which interface has better turn-taking? Define a measure
# and compare both interfaces in a suitable graph
# A2 average amount of keypresses between turn switch
def q1andq2(data, q):
    total_switches_single = 0
    total_switches_double = 0
    total_length_single = 0
    total_length_double = 0
    keys_list = data.keys()
    for key in keys_list:
        data_list = data[key]['s'].split('¦')
        if data_list[0] == '':
            turn = 'o'
        else:
            turn = 's'
        for i in range(len(data_list)):
            if i < data[key]['split'][0]:
                if data[key]['split'][0] == True:
                    total_length_double += 1
                    if data_list[i] == "" and turn == 's':
                        total_switches_double += 1
                        turn = 'o'
                    elif data_list[i] != "" and turn == 'o':
                        total_switches_double += 1
                        turn = 's'
                else:
                    total_length_single += 1
                    if data_list[i] == "" and turn == 's':
                        total_switches_single += 1
                        turn = 'o'
                    elif data_list[i] != "" and turn == 'o':
                        total_switches_single += 1
                        turn = 's'
            else:
                if data[key]['split'][0] == True:
                    total_length_single += 1
                    if data_list[i] == "" and turn == 's':
                        total_switches_single += 1
                        turn = 'o'
                    elif data_list[i] != "" and turn == 'o':
                        total_switches_single += 1
                        turn = 's'
                else:
                    total_length_double += 1
                    if data_list[i] == "" and turn == 's':
                        total_switches_double += 1
                        turn = 'o'
                    elif data_list[i] != "" and turn == 'o':
                        total_switches_double += 1
                        turn = 's'
    if q == 1:
        avg_pres_single = total_switches_single/total_length_single
        avg_pres_double = total_switches_double/total_length_double
        print("Q1:\nInterface 1 switched on average {0} times per keypress.".format(round(avg_pres_single, 4)))
        print("Interface 2 switched on average {0} times per keypress.".format(round(avg_pres_double, 4)))
    elif q == 2:
        avg_length_single = total_length_single/total_switches_single
        avg_length_double = total_length_double/total_switches_double
        print("Q2:\nInterface 1 had an average of {0} words between switches.".format(round(avg_length_single, 4)))
        print("Interface 2 had an average of {0} words between switches.".format(round(avg_length_double, 4)))


# turns a conversation dict into two list containing all words typed by
# both participants.
def word_string(file_dict):
    self_total = file_dict['s'].split("¦")
    other_total = file_dict['o'].split("¦")
    self_inter1 = ""
    self_inter2 = ""
    other_inter1 = ""
    other_inter2 = ""
    if file_dict["split"][1] == "inter1":
        self_inter1 = "".join(self_total[:file_dict["split"][0]])
        self_inter2 = "".join(self_total[file_dict["split"][0]:])
        other_inter1 = "".join(other_total[:file_dict["split"][0]])
        other_inter2 = "".join(other_total[file_dict["split"][0]:])
    elif file_dict["split"][1] == "inter2":
        self_inter1 = "".join(self_total[file_dict["split"][0]:])
        self_inter2 = "".join(self_total[:file_dict["split"][0]])
        other_inter1 = "".join(other_total[file_dict["split"][0]:])
        other_inter2 = "".join(other_total[:file_dict["split"][0]])
    return self_inter1, self_inter2, other_inter1, other_inter2


def q3(data):
    data_counter = 0
    percentage_interface1 = 0
    percentage_interface2 = 0
    for file_key, sort_and_text in data.items():
        data_counter += 1
        self_inter1, self_inter2, other_inter1, other_inter2 = word_string(data[file_key])
        percentage_interface1 += word_checker(self_inter1.split(), other_inter1.split())
        percentage_interface2 += word_checker(self_inter2.split(), other_inter2.split())

    print("Q3:\nIn Interface 1 they copied each other’s language {0}% out of 100% on average."
          .format(round((percentage_interface1 / data_counter) * 100, 4)))
    print("In Interface 2 they copied each other’s language {0}% out of 100% on average."
          .format(round((percentage_interface2 / data_counter) * 100, 4)))


# Q4. Which is the happier interface?
# Define a measure and compare both interfaces in a suitable graph
# A4 use wordlist with happy words, and compare the average amount of
# happy words per word.
def q4(data):
    with open("./happy_words.txt") as f:
        happy_words = f.read().split("\n")
    inter1_happy_words_total = 0
    inter2_happy_words_total = 0
    inter1_words_total = 0
    inter2_words_total = 0
    for key in data.keys():
        self_inter1, self_inter2, other_inter1, other_inter2 = word_string(data[key])
        inter1_words = self_inter1.split() + other_inter1.split()
        inter2_words = self_inter2.split() + other_inter2.split()
        inter1_words_total += len(inter1_words)
        inter2_words_total += len(inter2_words)
        for word in inter1_words:
            if word in happy_words:
                inter1_happy_words_total += 1
        for word in inter2_words:
            if word in happy_words:
                inter2_happy_words_total += 1
    print("Q4:\nInterface 1 has an average of {0} happy words per word."
          .format(round(inter1_happy_words_total/inter1_words_total, 4)))
    print("Interface 2 has an average of {0} happy words per word.".
          format(round(inter2_happy_words_total/inter2_words_total, 4)))


def word_checker(s, o):
    used_words_s = set()
    used_words_o = set()
    same_words_counter = 0
    for word_s, word_o in zip(s, o):
        used_words_s.add(word_s)
        used_words_o.add(word_o)
        if word_s in used_words_o:
            same_words_counter += 1
        if word_o in used_words_s:
            same_words_counter += 1

    try:
        return same_words_counter / (len(used_words_s) + len(used_words_o))
    except ZeroDivisionError:
        return 0.0


def q5(data):
    data_counter = 0

    same_emotion_inter1 = 0
    same_emotion_inter2 = 0
    other_emotion_inter1 = 0
    other_emotion_inter2 = 0

    # opening happy en sad words lists
    with open("./happy_words.txt") as f:
        positive_emotions = f.read().split("\n")
        lowered_positive_emotions = [pos_em.lower() for pos_em in positive_emotions]
    with open("./negative_emotions.txt") as f:
        negative_emotions = f.read().split("\n")
        lowered_negative_emotions = [neg_em.lower() for neg_em in negative_emotions]

    for file_key, sort_and_text in data.items():
        data_counter += 1
        self_inter1, self_inter2, other_inter1, other_inter2 = word_string(data[file_key])

        se_inter1, oe_inter1 = emotion_checker(self_inter1.split(), other_inter1.split(),
                                               set(lowered_positive_emotions),
                                               set(lowered_negative_emotions))
        same_emotion_inter1 += se_inter1
        other_emotion_inter1 += oe_inter1

        se_inter2, oe_inter2 = emotion_checker(self_inter2.split(), other_inter2.split(),
                                               set(lowered_positive_emotions),
                                               set(lowered_negative_emotions))
        same_emotion_inter2 += se_inter2
        other_emotion_inter2 += oe_inter2

    print("Q5:\nAmount of same emotions in interface 1: {0}\nAmount of other emotions in interface 1: {1}"
          .format(same_emotion_inter1, other_emotion_inter1))
    print("Amount of same emotions in interface 2: {0}\nAmount of other emotions in interface 2: {1}"
          .format(same_emotion_inter2, other_emotion_inter2))


def emotion_checker(self_inter, other_inter, positive_emotions, negative_emotions):
    same_emotion_counter = 0
    other_emotion_counter = 0
    last_emotion = ""

    for self_w, other_w in zip(self_inter, other_inter):
        if self_w in negative_emotions:
            last_emotion = "negative"
        elif self_w in positive_emotions:
            last_emotion = "positive"

        if last_emotion == "negative":
            if other_w.lower() in negative_emotions:
                same_emotion_counter += 1
            elif other_w.lower() in positive_emotions:
                other_emotion_counter += 1
        elif last_emotion == "positive":
            if other_w.lower() in positive_emotions:
                same_emotion_counter += 1
            elif other_w.lower() in negative_emotions:
                other_emotion_counter += 1

    return other_emotion_counter, same_emotion_counter


# Q6: Although the datafiles do not contain explicit information
# about whether their guesses were correct or not,
# it is often apparent from the transcript that they made a correct
# or incorrect choice. Can you write an algorithm that estimates
# for each dialogue how many guesses were correct / incorrect.
# A6: to do this we use two lists, one with conformation words and
# one with disconformation words. we count the amount of words in the
# s file. We estimate that this wil be about the amount
# of correct and incorrect guesses. Since we made these list ourself,
# so they are probably not complete
def q6(data):
    with open("./conformation_words.txt") as f:
        correct_words = f.read().split("\n")
    with open("./disconformation_words.txt") as f:
        false_words = f.read().split("\n")
    inter1_correct_words_total = 0
    inter2_correct_words_total = 0
    inter1_false_words_total = 0
    inter2_false_words_total = 0
    for key in data.keys():
        self_inter1, self_inter2, other_inter1, other_inter2 = word_string(data[key])
        inter1_words = self_inter1.split() + other_inter1.split()
        inter2_words = self_inter2.split() + other_inter2.split()
        for word in inter1_words:
            if word in correct_words:
                inter1_correct_words_total += 1
            if word in false_words:
                inter1_false_words_total += 1
        for word in inter2_words:
            if word in correct_words:
                inter2_correct_words_total += 1
            if word in false_words:
                inter2_false_words_total += 1
    print("Q6:\nInterface 1 has {0} conformation words and {1} disconformation words."
          .format(inter1_correct_words_total, inter1_false_words_total))
    print("Interface 2 has {0} conformation words and {1} disconformation words."
          .format(inter2_correct_words_total, inter2_false_words_total))


# Q7: Can you think of any other interesting measure(s)?
# Define them and compare both interfaces in a suitable graph.
# What is the average turn time? Turn meaning the time before
# the other person reacts or interupts.
def q7(data):
    turn_times_inter1 = []
    turn_times_inter2 = []
    total_turns_inter1 = 0
    total_turns_inter2 = 0
    for key in data.keys():
        time = [0] + data[key]['t'].split('¦')[3:-1]
        self = data[key]['s'].split('¦')
        time.append(0)
        this_turn_time = 0
        turn = None
        for i in range(len(self)):
            if turn is None:
                if self[i] == "":
                    turn = 'o'
                else:
                    turn = 's'
                this_turn_time += int(time[i])
            elif turn == 'o':
                if self[i] == "":
                    this_turn_time += int(time[i])
                else:
                    if i < data[key]['split'][0] and data[key]['split'][1] == 'inter1':
                        turn_times_inter1.append(this_turn_time + int(time[i]))
                        this_turn_time = 0
                        total_turns_inter1 += 1
                        turn = 's'
                    elif i < data[key]['split'][0] and data[key]['split'][1] == 'inter2':
                        turn_times_inter2.append(this_turn_time + int(time[i]))
                        this_turn_time = 0
                        total_turns_inter2 += 1
                        turn = 's'
                    elif i >= data[key]['split'][0] and data[key]['split'][1] == 'inter1':
                        turn_times_inter1.append(this_turn_time + int(time[i]))
                        this_turn_time = 0
                        total_turns_inter1 += 1
                        turn = 's'
                    elif i >= data[key]['split'][0] and data[key]['split'][1] == 'inter2':
                        turn_times_inter1.append(this_turn_time + int(time[i]))
                        this_turn_time = 0
                        total_turns_inter1 += 1
                        turn = 's'
            elif turn == 's':
                if self[i] == "":
                    if i < data[key]['split'][0] and data[key]['split'][1] == 'inter1':
                        turn_times_inter1.append(this_turn_time + int(time[i]))
                        this_turn_time = 0
                        total_turns_inter1 += 1
                        turn = 'o'
                    elif i < data[key]['split'][0] and data[key]['split'][1] == 'inter2':
                        turn_times_inter2.append(this_turn_time + int(time[i]))
                        this_turn_time = 0
                        total_turns_inter2 += 1
                        turn = 'o'
                    elif i >= data[key]['split'][0] and data[key]['split'][1] == 'inter1':
                        turn_times_inter1.append(this_turn_time + int(time[i]))
                        this_turn_time = 0
                        total_turns_inter1 += 1
                        turn = 'o'
                    elif i >= data[key]['split'][0] and data[key]['split'][1] == 'inter2':
                        turn_times_inter1.append(this_turn_time + int(time[i]))
                        this_turn_time = 0
                        total_turns_inter1 += 1
                        turn = 'o'
                else:
                    this_turn_time += int(time[i])
    avg_inter1 = round((sum(turn_times_inter1)/total_turns_inter1)/1000, 4)
    avg_inter2 = round((sum(turn_times_inter2)/total_turns_inter2)/1000, 4)
    print("Q7:\nThe average amount of turntime for interface 1 is {0} seconds".format(avg_inter1))
    print("The average amount of turntime for interface 2 is {0} seconds.".format(avg_inter2))


def main():
    raw_data = get_data()
    data = splitpoint(raw_data)
    q1andq2(data, 1)
    print()
    q1andq2(data, 2)
    print()
    q3(data)
    print()
    q4(data)
    print()
    q5(data)
    print()
    q6(data)
    print()
    q7(data)


if __name__ == "__main__":
    main()
