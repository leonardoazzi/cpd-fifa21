class TrieTreeNode:

    def __init__(self, char):

        self.char = char
        self.is_end = False
        self.children = {}

class TrieTree(object):

    def __init__(self):

        self.root = TrieTreeNode("")
    
    def insert(self, word):

        node = self.root
        
        for char in word:

            if char in node.children:

                node = node.children[char]

            else:

                new_node = TrieTreeNode(char)
                node.children[char] = new_node
                node = new_node
        
        node.is_end = True
        
    def depth_first_search(self, node, prefix):

        if node.is_end:

            self.output.append((prefix + node.char))
        
        for child in node.children.values():

            self.depth_first_search(child, prefix + node.char)
        
    def words_from_prefixe(self, x):

        self.output = []
        node = self.root
        
        for char in x:

            if char in node.children:

                node = node.children[char]

            else:

                return []
        
        self.depth_first_search(node, x[:-1])

        return sorted(self.output, key = lambda x: x[1], reverse = True)