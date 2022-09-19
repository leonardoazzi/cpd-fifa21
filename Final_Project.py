# INFORMATION ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# INF01124 - Final Project
# Erick Larratéa Knoblich 00324422
# Leonardo Azzi Martins 00323721

# IMPORTS --------------------------------------------------------------------------------------------------------------------------------------------------------------------------

import Hash_Table, Trie_Tree, Table_It
import sys, os, csv, time
from operator import itemgetter

# FUNCTIONS ------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def Display_Menu():

    print(

        "A aplicação demorou " + str(time_taken) + " segundos para processar os dados.\n\n"
        "INF01124: FINAL PROJECT\n\n"
        "Funcionalidades:\n\n"
        "1. player <name or prefix>\n"
        "2. user <userID>\n"
        "3. top<N> ‘<position>’\n"
        "4. tags <list of tags>\n"
        
    )

def Sort_Information(information, pivot):

    information.sort(key = itemgetter(pivot), reverse = True)

    return information

def Search_1(user_input, trie_tree, hash_table, output):

    output.append(["SOFIFA ID", "NAME", "PLAYER POSITIONS", "GLOBAL RATING", "TIMES RATED"])        

    for name in trie_tree.words_from_prefixe(user_input):

        item = hash_table.search(name, 1, False)
        output.append(item)

    return output

def Search_2(user_input, direction, hash_table_1, hash_table_2, output):

    output.append(["SOFIFA ID", "NAME", "GLOBAL RATING", "TIMES RATED", "RATING"])
    
    info = hash_table_1.search(user_input, 0, True)

    information_1 = Sort_Information(info, 2)

    counter = 0

    for item_1 in information_1[::direction]:

        sofifa_id, rating = item_1[1], item_1[2]
        information_2 = hash_table_2.search(sofifa_id, 0, False)
        name, global_rating, times_rated = information_2[1], information_2[3], information_2[4]
        item_2 = sofifa_id, name, global_rating, times_rated, rating
        output.append(item_2)
        counter += 1

        if counter == 20:

            break

    return output

def Search_3(user_input, direction, top_bottom_x, top_bottom_player_positions, output):

    output.append(["SOFIFA ID", "NAME", "PLAYER POSITIONS", "GLOBAL RATING", "TIMES RATED"])
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

# Pesquisa sobre tags
def Search_4(user_input, hash_table, output):

    output.append(["SOFIFA ID", "NAME", "PLAYER POSITIONS", "GLOBAL RATING", "TIMES RATED"])
    counter = 0

    for pivot_item in hash_table.search(user_input[0], 5, True):

        pivot_item = pivot_item[:5]
        # print(pivot_item)

        # Se apenas uma tag for inserida
        if (len(user_input) == 1):
            
            output.append(pivot_item)

        # Se duas ou mais tags forem inseridas, faz o match
        else:

            for tag in user_input[1:]:
                
                for item in hash_table.search(tag, 5, True):

                    item = item[:5]

                    if pivot_item == item:

                        counter += 1

                        if counter == len(user_input) - 1:

                            counter = 0
                            output.append(pivot_item)
                            break
            
        counter = 0

    return output

# DATA PROCESSING ------------------------------------------------------------------------------------------------------------------------------------------------------------------

os.system('cls||clear')
print("Processing data...", end = "")
starting_time = time.time()
hash_table_1 = Hash_Table.HashTable(24697)
hash_table_2 = Hash_Table.HashTable(18947)
hash_table_3 = Hash_Table.HashTable(18947)
hash_table_4 = Hash_Table.HashTable(1499)
hash_table_x = Hash_Table.HashTable(24179999)
trie_tree = Trie_Tree.TrieTree()
top_bottom_player_positions, list_of_tags, output = [], [], []
error = False

# with open(os.path.join(sys.path[0], "rating.csv"), encoding = "utf8") as csv_file:
with open("rating.csv") as csv_file:

    times_rated, rating_sum, global_rating = 0, 0, 0
    csv_reader = csv.reader(csv_file, delimiter = ",")
    next(csv_reader)

    # with open(os.path.join(sys.path[0], "rating.csv"), encoding = "utf8") as auxiliary_csv_file:
    with open("rating.csv") as auxiliary_csv_file:

        auxiliary_csv_reader = csv.reader(auxiliary_csv_file, delimiter = ",")
        next(auxiliary_csv_reader)
        next(auxiliary_csv_reader)

        for row, auxiliary_row in zip(csv_reader, auxiliary_csv_reader):

            user_id, sofifa_id, rating = row[0], row[1], float(row[2])
            item = user_id, sofifa_id, rating
            hash_table_x.insert(item, user_id)
            auxiliary_sofifa_id = auxiliary_row[1]
            rating_sum += rating
            times_rated += 1

            if sofifa_id != auxiliary_sofifa_id:

                global_rating = '{:.6f}'.format(rating_sum / times_rated)
                item = sofifa_id, global_rating, times_rated
                hash_table_1.insert(item, sofifa_id)
                times_rated, rating_sum, global_rating = 0, 0, 0

# with open(os.path.join(sys.path[0], "players.csv"), encoding = "utf8") as csv_file:
with open("players.csv") as csv_file:

    csv_reader = csv.reader(csv_file, delimiter = ",")
    next(csv_reader)

    for row in csv_reader:

        sofifa_id, name, player_positions = row[0], row[1], row[2]
        trie_tree.insert(name)
        information = hash_table_1.search(sofifa_id, 0, False)

        if information is None:

            global_rating, times_rated = 0, 0

        else:

            global_rating, times_rated = information[1], information[2]

        item = sofifa_id, name, player_positions, float(global_rating), times_rated
        hash_table_2.insert(item, name)
        hash_table_3.insert(item, sofifa_id)
        top_bottom_player_positions.append(item)

# with open(os.path.join(sys.path[0], "tags.csv"), encoding = "utf8") as csv_file:
with open("tags.csv") as csv_file:

    csv_reader = csv.reader(csv_file, delimiter = ",")
    next(csv_reader)

    # with open(os.path.join(sys.path[0], "tags.csv"), encoding = "utf8") as auxiliary_csv_file:
    with open("tags.csv") as auxiliary_csv_file:

        auxiliary_csv_reader = csv.reader(auxiliary_csv_file, delimiter = ",")
        next(auxiliary_csv_reader)
        next(auxiliary_csv_reader)

        for row, auxiliary_row in zip(csv_reader, auxiliary_csv_reader):

            sofifa_id, tag = row[1], row[2]
            auxiliary_sofifa_id = auxiliary_row[1]

            if tag == "":

                continue

            if tag not in list_of_tags:

                list_of_tags.append(tag)

            if sofifa_id != auxiliary_sofifa_id:

                information = hash_table_3.search(sofifa_id, 0, False)

                if information is None:

                    continue

                sofifa_id, name, player_positions, global_rating, times_rated = information[0], information[1], information[2], information[3], information[4]

                for tag in list_of_tags:

                    item = sofifa_id, name, player_positions, global_rating, times_rated, tag
                    hash_table_4.insert(item, tag)

                list_of_tags.clear()

top_bottom_player_positions = Sort_Information(top_bottom_player_positions, 3)
ending_time = time.time()
time_taken = '{:.6f}'.format(ending_time - starting_time)
os.system('cls||clear')
Display_Menu()


# APPLICATION ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

def search(user_input):
    global output, error

    output.clear()

    Display_Menu()
    # user_input = input("Input the functioanlity: ").split(" ", 1)

    user_input = user_input.split(" ") # Cria um array de palavras
    print("Input: ", user_input)

    # Comando
    type_input = user_input[0]  # player / user / top<N> / tags

    # Parâmetro
    param_input = user_input[1:] # <name> / <userID> / '<position>' / <list of tags>

    # 2.1 Pesquisas sobre o nome de jogadores
    # player <name or prefix>
    if type_input == "player":
        
        output = Search_1(param_input[0], trie_tree, hash_table_2, output)

    # 2.2 Pesquisas sobre jogadores revisados por usuários
    # Esta pesquisa deve retornar a lista com no máximo 20 jogadores revisados pelo usuário e para
    # cada jogador mostrar a nota dada pelo usuário, a média global e a contagem de avaliações. A
    # lista deve ser ordenada pela nota dada pelo usuário de maneira decrescente (maiores notas
    # primeiro). 
    #
    # user <userID>
    elif type_input == "user":
        
        quant_input = param_input[0]

        if quant_input.isdigit():
            direction = 1
            output = Search_2(quant_input, direction, hash_table_x, hash_table_3, output)
        else:
            print("\nInvalid input!")
            error = True
            return

    # 2.3 Pesquisas sobre os melhores jogadores de uma determinada posição
    # Esta pesquisa tem por objetivo retornar a lista de jogadores com melhores notas de uma dada
    # posição. Para evitar que um jogador seja retornando com uma boa média mas com poucas
    # avaliações, esta consulta somente deve retornar os melhores jogadores com no mínimo 1000
    # avaliações. Para gerenciar o número de jogadores a serem retornados, a consulta deve
    # receber como parâmetro um número N que corresponde ao número máximo de jogadores a
    # serem retornados. O resultado da consulta deve estar ordenado da maior para a menor
    # avaliação. 
    # 
    # top<N> '<position>'

    elif type_input[0:3] == "top" and type_input[3:].isdigit():

        n_input = user_input[0][3:]
        pos_input = user_input[1]

        direction, top_bottom_x = 1, user_input[0][3:]
        output = output = Search_3(n_input, direction, top_bottom_x, top_bottom_player_positions, output)

    # 2.4 Pesquisas sobre ‘tags’ de jogadores
    # Esta pesquisa tem por objetivo explorar a lista de tags adicionadas por cada usuário em cada
    # revisão. Para uma lista de tags dada como entrada, a pesquisa deve retornar a lista de
    # jogadores que estão associados a interseção de um conjunto de tags.
    #
    # tags <list of tags>

    elif type_input == "tags":

        input = []

        for idx, line in enumerate(param_input):
            tags = param_input[idx].strip("''")
            input.append(tags)

        output = Search_4(input, hash_table_4, output)

    else:

        print("\nInvalid input!")
        error = True
        return

    if error == False:

        print()
        Table_It.printTable(output, useFieldNames = True)

        return output
        

    # user_input = input("\nInput 'E' to finish the application or input anything else to continue the application: ")

    # if user_input == "E":

    #     output.clear()
    #     os.system('cls||clear')
    #     return 0

    # else:

        # output.clear()
        # error = False
        # os.system('cls||clear')