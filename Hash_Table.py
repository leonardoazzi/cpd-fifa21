class HashTable(object):

    def __init__(self, size):

        self.items = [None] * size
        self.size = size

    def insert(self, item, key, pivot):

        index = self.hash(key)

        if self.items[index] is None:

            self.items[index] = [item]

        elif self.items[index][0][pivot] == key:
            
            self.items[index].append(item)

        else:

            while True:

                index = (index + 1) % self.size

                if self.items[index] is None:

                    self.items[index] = [item]
                    break

                if self.items[index] is not None and self.items[index][0][pivot] == key:

                    self.items[index].append(item)
                    break

    def search(self, key, pivot):

        index = self.hash(key)

        if self.items[index][0][pivot] == key:

            return self.items[index]

        while True:

            index = (index + 1) % self.size

            if self.items[index] is not None and self.items[index][0][pivot] == key:

                return self.items[index]
                
    def hash(self, key):

        hashsum = 0

        for character in range(len(key)):

            hashsum = (hashsum * 31) + ord(key[character])

        return hashsum % self.size