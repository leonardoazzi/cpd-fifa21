import sys, os, csv
import pandas as pd

i = 0
list_of_tags = []
test_list = []

with open(os.path.join(sys.path[0], "tags.csv"), encoding = "utf8") as csv_file:

    end = len(pd.read_csv(os.path.join(sys.path[0], "tags.csv"))) - 1
    csv_reader = csv.reader(csv_file, delimiter = ",")
    next(csv_reader)

    with open(os.path.join(sys.path[0], "tags.csv"), encoding = "utf8") as auxiliary_csv_file:

        auxiliary_csv_reader = csv.reader(auxiliary_csv_file, delimiter = ",")
        next(auxiliary_csv_reader)
        next(auxiliary_csv_reader)

        for row, auxiliary_row in zip(csv_reader, auxiliary_csv_reader):

            sofifa_id, tag = row[1], row[2]
            auxiliary_sofifa_id = auxiliary_row[1]
            i += 1

            if tag not in list_of_tags:

                list_of_tags.append(tag)

            if i == end:

                print("hi")

                for tag in list_of_tags:

                    item = sofifa_id, list_of_tags, tag
                    test_list.append(item)
                    print(test_list)

                list_of_tags.clear()

            else:

                if sofifa_id != auxiliary_sofifa_id:

                    for tag in list_of_tags:

                        item = sofifa_id, list_of_tags, tag
                        test_list.append(item)

                        if i < 100:

                            print(test_list)



                    list_of_tags.clear()

print(test_list)