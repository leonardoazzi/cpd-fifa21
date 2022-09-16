# INFORMATION ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# INF01124 - Final Project
# Erick Larratéa Knoblich 00324422
# Leonardo Azzi Martins 00323721

# IMPORTS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import Hash_Table, Trie_Tree, TableIt
import sys, os, csv, time
from operator import itemgetter
import pandas as pd
import streamlit as st

# FUNCTIONS ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def Display_Menu():

    print(

        "The application took " + str(time_taken) + " seconds to process the data.\n\n"
        "INF01124: FINAL PROJECT\n\n"
        "Functionalities:\n\n"
        "1. player <name or prefix>\n"
        "2. user top <userID>\n"
        "3. user bottom <userID>\n"
        "4. top<N> ‘<position>’\n"
        "5. bottom<N> ‘<position>’\n"
        "6. tags <list of tags>\n"
        
    )

def Quick_Sort(information, pivot):

    information.sort(key = itemgetter(pivot), reverse = True)

    return information

def Search_1(user_input, trie_tree, hash_table, output):

    output.append(["SOFIFA ID", "NAME", "PLAYER POSITIONS", "GLOBAL RATING", "TIMES RATED"])        

    for name in trie_tree.query(user_input):

        item = hash_table.search(name, 1)[0]
        output.append(item)

    return output

def Search_2(user_input, direction, hash_table_1, hash_table_2, output):

    output.append(["SOFIFA ID", "NAME", "GLOBAL RATING", "TIMES RATED", "RATING"])
    information_1 = hash_table_1.search(user_input, 0)
    auxiliary_output = []
    
    for item in information_1:

        sofifa_id, rating = item[1], item[2]
        information_2 = hash_table_2.search(sofifa_id, 0)[0]
        name, global_rating, times_rated = information_2[1], information_2[2], information_2[3]
        item_2 = sofifa_id, name, global_rating, times_rated, rating
        auxiliary_output.append(item_2)
    
    auxiliary_output = Quick_Sort(auxiliary_output, 4)

    for item_2 in auxiliary_output[::direction]:

        output.append(item_2)

    auxiliary_output.clear()
    return output

def Search_3(user_input, direction, top_bottom_x, top_bottom_player_positions, output):

    output.append(["SOFIDA ID", "NAME", "PLAYER POSITIONS", "GLOBAL RATING", "TIMES RATED"])
    player_positions = user_input[1:-1].split(", ")
    counter = 0

    for item in top_bottom_player_positions[::direction]:

        for player_position in player_positions:

            if player_position in item[2] and item[4] > 999 and item not in output:

                output.append(item)
                counter += 1

                if counter == int(top_bottom_x):

                    break
        
        if counter == int(top_bottom_x):

            break

    return output

def Search_4(user_input, hash_table, output):

    output.append(["SOFIDA ID", "NAME", "PLAYER POSITIONS", "GLOBAL RATING", "TIMES RATED"])
    counter = 0

    for pivot_item in hash_table.search(user_input[0], 5):

        pivot_item = pivot_item[:5]

        for tag in user_input[1:]:

            for item in hash_table.search(tag, 5):

                item = item[:5]

                if pivot_item == item:

                    counter += 1

                    if counter == len(user_input) - 1:

                        counter = 0
                        output.append(pivot_item)
                        break
            
        counter = 0

    return output


# APPLICATION ----------------------------------------------------------------------------------------------------------------------------------------------------------------------


# DATA PROCESSING ------------------------------------------------------------------------------------------------------------------------------------------------------------------

os.system('cls||clear')
print("Processing data...", end = "")
starting_time = time.time()
hash_table_1 = Hash_Table.HashTable(24697)
hash_table_2 = Hash_Table.HashTable(18947)
hash_table_3 = Hash_Table.HashTable(18947)
hash_table_4 = Hash_Table.HashTable(1499)
#hash_table_x = Hash_Table.HashTable(30000001)
trie_tree = Trie_Tree.TrieTree()
top_bottom_player_positions, list_of_tags, output = [], [], []
counter = 0
error = False

# with open(os.path.join(sys.path[0], "rating.csv"), encoding = "utf8") as csv_file:
with open("rating.csv") as csv_file:

    # end = len(pd.read_csv(os.path.join(sys.path[0], "rating.csv")))
    end = len(pd.read_csv("rating.csv"))
    times_rated, rating_sum, global_rating = 0, 0, 0
    csv_reader = csv.reader(csv_file, delimiter = ",")
    next(csv_reader)

    with open("rating.csv") as auxiliary_csv_file:
    # with open(os.path.join(sys.path[0], "rating.csv"), encoding = "utf8") as auxiliary_csv_file:

        auxiliary_csv_reader = csv.reader(auxiliary_csv_file, delimiter = ",")
        next(auxiliary_csv_reader)
        next(auxiliary_csv_reader)

        for row, auxiliary_row in zip(csv_reader, auxiliary_csv_reader):

            user_id, sofifa_id, rating = row[0], row[1], float(row[2])
            #item = user_id, sofifa_id, rating
            #hash_table_x.insert(item, user_id, 0)
            auxiliary_sofifa_id = auxiliary_row[1]
            rating_sum += rating
            times_rated += 1

            if(sofifa_id != auxiliary_sofifa_id):

                global_rating = '{:.6f}'.format(rating_sum / times_rated)
                item = sofifa_id, global_rating, times_rated
                hash_table_1.insert(item, sofifa_id, 0)
                times_rated, rating_sum, global_rating = 0, 0, 0

with open("players.csv") as csv_file:
# with open(os.path.join(sys.path[0], "players.csv"), encoding = "utf8") as csv_file:

    csv_reader = csv.reader(csv_file, delimiter = ",")
    next(csv_reader)

    for row in csv_reader:

        sofifa_id, name, player_positions = row[0], row[1], row[2]
        trie_tree.insert(name)
        information = hash_table_1.search(sofifa_id, 0)[0]
        global_rating, times_rated = information[1], information[2]
        item = sofifa_id, name, player_positions, global_rating, times_rated
        hash_table_2.insert(item, name, 1)
        hash_table_3.insert(item, sofifa_id, 0)
        top_bottom_player_positions.append(item)

with open("tags.csv") as csv_file:
# with open(os.path.join(sys.path[0], "tags.csv"), encoding = "utf8") as csv_file:

    counter = 0
    end = len(pd.read_csv("tags.csv"))
    # end = len(pd.read_csv(os.path.join(sys.path[0], "tags.csv")))
    csv_reader = csv.reader(csv_file, delimiter = ",")
    next(csv_reader)

    with open( "tags.csv") as auxiliary_csv_file:
    # with open(os.path.join(sys.path[0], "tags.csv"), encoding = "utf8") as auxiliary_csv_file:

        auxiliary_csv_reader = csv.reader(auxiliary_csv_file, delimiter = ",")
        next(auxiliary_csv_reader)
        next(auxiliary_csv_reader)

        for row, auxiliary_row in zip(csv_reader, auxiliary_csv_reader):

            sofifa_id, tag = row[1], row[2]
            auxiliary_sofifa_id = auxiliary_row[1]
            counter += 1

            if tag == "":

                continue

            if tag not in list_of_tags:

                list_of_tags.append(tag)

            if counter == end - 1:

                information = hash_table_3.search(sofifa_id, 0)[0]
                sofifa_id, name, player_positions, global_rating, times_rated = information[0], information[1], information[2], information[3], information[4]

                for tag in list_of_tags:

                    item = sofifa_id, name, player_positions, global_rating, times_rated, tag
                    hash_table_4.insert(item, tag, 5)

                list_of_tags.clear()

            elif sofifa_id != auxiliary_sofifa_id:

                information = hash_table_3.search(sofifa_id, 0)[0]
                sofifa_id, name, player_positions, global_rating, times_rated = information[0], information[1], information[2], information[3], information[4]

                for tag in list_of_tags:

                    item = sofifa_id, name, player_positions, global_rating, times_rated, tag
                    hash_table_4.insert(item, tag, 5)

                list_of_tags.clear()

top_bottom_player_positions = Quick_Sort(top_bottom_player_positions, 3)
ending_time = time.time()
time_taken = '{:.6f}'.format(ending_time - starting_time)
os.system('cls||clear')

# Display_Menu()
# user_input = input("Input the functioanlity: ").split(" ", 1)

@st.cache
def search(user_input):
    global output
    
    user_input = user_input.split(" ", 1)

    if user_input[0] == "player":

        output = Search_1(user_input[1], trie_tree, hash_table_2, output)
        return output

    elif user_input[0][0:3] == "top" and user_input[0][3:].isdigit():

        direction, top_bottom_x = 1, user_input[0][3:]
        output = output = Search_3(user_input[1], direction, top_bottom_x, top_bottom_player_positions, output)

    elif user_input[0][0:6] == "bottom" and user_input[0][6:].isdigit():

        direction, top_bottom_x = -1, user_input[0][6:]
        output = output = Search_3(user_input[1], direction, top_bottom_x, top_bottom_player_positions, output)

    #elif user_input[0][0:4] == "user" and user_input[1][0:3] == "top" and user_input[1][4:].isdigit():

        #direction = 1
        #output = Search_2(user_input[1][4:], direction, hash_table_x, hash_table_3, output)

    #elif user_input[0][0:4] == "user" and user_input[1][0:6] == "bottom" and user_input[1][7:].isdigit():

        #direction = -1
        #output = Search_2(user_input[1][7:], direction, hash_table_x, hash_table_3, output)

    elif user_input[0] == "tags":

        user_input = user_input[1][1:-1].split("' '")
        output = Search_4(user_input, hash_table_4, output)

    else:

        print("\nInvalid input!")
        error = True

    if error == False:

        print()
        TableIt.printTable(output, useFieldNames = True)
        output.clear()

    user_input = input("\nInput 'E' to finish the application or input anything else to continue the application: ")

    if user_input == "E":

        output.clear()
        os.system('cls||clear')
        return 0

    else:

        output.clear()
        error = False
        os.system('cls||clear')

print("Calling all. This is our last cry before our eternal silence.")
# Display_Menu()
# user_input = input("Input the functioanlity: ").split(" ", 1)
# main(user_input)


if __name__ == "__main__":
    main()
