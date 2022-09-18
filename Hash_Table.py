class HashTable(object):

    def __init__(self, size):

        self.items = [None] * size
        self.size = size

    def insert(self, item, key):

        index = self.hash(key)

        if self.items[index] is None:

            self.items[index] = [item]

        else:

            self.items[index].append(item)

    def search(self, key, pivot, return_list):

        index = self.hash(key)
        output_list = []

        if self.items[index] is None:

            return None

        elif return_list == True:

            for item in self.items[index]:

                if item[pivot] == key:

                    output_list.append(item)

            if len(output_list) == 0:

                return None

            else:
                
                return output_list

        else:

            for item in self.items[index]:

                if item[pivot] == key:

                    return item

            return None

    def hash(self, key):

        hashsum = 0

        for character in range(len(key)):

            hashsum = (hashsum * 31) + ord(key[character])

        return hashsum % self.size