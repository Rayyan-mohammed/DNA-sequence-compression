import sys
sys.setrecursionlimit(2000000)

class Node:
    def __init__(self, start, end=None):
        self.start = start
        self.end = end
        self.children = {}
        self.suffix_link = None
        self.suffix_index = -1

class SuffixTree:
    '''
    A true O(n) Suffix Tree using Ukkonen's Algorithm.
    Allows processing of very large DNA sequences in linear time.
    '''
    def __init__(self, text):
        self.text = text
        self.size = len(text)
        self.root = Node(-1, -1)
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        self.remainder = 0
        self.leaf_end = -1
        
        self.build()
        self.set_suffix_index(self.root, 0)

    def edge_length(self, node):
        if node == self.root:
            return 0
        end = self.leaf_end if node.end is None else node.end
        return end - node.start + 1

    def walk_down(self, curr_node):
        length = self.edge_length(curr_node)
        if self.active_length >= length:
            self.active_edge += length
            self.active_length -= length
            self.active_node = curr_node
            return True
        return False

    def build(self):
        for i in range(self.size):
            self.extend(i)

    def extend(self, pos):
        self.leaf_end = pos
        self.remainder += 1
        last_new_node = None

        while self.remainder > 0:
            if self.active_length == 0:
                self.active_edge = pos

            char = self.text[self.active_edge]

            if char not in self.active_node.children:
                self.active_node.children[char] = Node(pos)
                if last_new_node is not None:
                    last_new_node.suffix_link = self.active_node
                    last_new_node = None
            else:
                next_node = self.active_node.children[char]
                if self.walk_down(next_node):
                    continue
                
                if self.text[next_node.start + self.active_length] == self.text[pos]:
                    if last_new_node is not None and self.active_node != self.root:
                        last_new_node.suffix_link = self.active_node
                        last_new_node = None
                    self.active_length += 1
                    break
                
                split_end = next_node.start + self.active_length - 1
                split_node = Node(next_node.start, split_end)
                self.active_node.children[char] = split_node

                split_node.children[self.text[pos]] = Node(pos)
                next_node.start += self.active_length
                split_node.children[self.text[next_node.start]] = next_node

                if last_new_node is not None:
                    last_new_node.suffix_link = split_node
                last_new_node = split_node

            self.remainder -= 1
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remainder + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link if self.active_node.suffix_link else self.root

    def set_suffix_index(self, node, label_height):
        if not node: return
        is_leaf = True
        for child in node.children.values():
            is_leaf = False
            self.set_suffix_index(child, label_height + self.edge_length(child))
        if is_leaf:
            node.suffix_index = self.size - label_height

    def find_all_occurrences(self, pattern):
        node = self.root
        i = 0
        pat_len = len(pattern)
        
        while i < pat_len:
            char = pattern[i]
            if char not in node.children:
                return []
            child = node.children[char]
            edge_len = self.edge_length(child)
            j = 0
            while i < pat_len and j < edge_len:
                if pattern[i] != self.text[child.start + j]:
                    return []
                i += 1
                j += 1
            node = child
            
        results = []
        self._get_leaves(node, results)
        return sorted(results)

    def _get_leaves(self, node, results):
        if node.suffix_index != -1:
            results.append(node.suffix_index)
        for child in node.children.values():
            self._get_leaves(child, results)

    def longest_repeated_substring(self):
        max_len = 0
        lrs_end_pos = 0
        
        def dfs(node, total_len):
            nonlocal max_len, lrs_end_pos
            is_leaf = node.suffix_index != -1
            if not is_leaf:
                for child in node.children.values():
                    dfs(child, total_len + self.edge_length(child))
                if node != self.root:
                    substr_edge = self.text[node.end - total_len + 1 : node.end + 1]
                    # Make sure we don't count the unique termination character in repeats
                    if '$' not in substr_edge and total_len > max_len:
                        max_len = total_len
                        lrs_end_pos = node.end

        dfs(self.root, 0)
        if max_len == 0:
            return ""
        return self.text[lrs_end_pos - max_len + 1 : lrs_end_pos + 1]

def compress_sequence(text, lrs):
    if not lrs or len(lrs) < 2:
        return text.replace('$', ''), 1.0
    
    # Simple dictionary-like compression: replace LRS with a token
    token = f"<{lrs}>"
    compressed = text.replace(lrs, token)
    
    # Calculate compression ratio
    original_size = len(text)
    # Token sizes: in a real compressor, a pointer takes fewer bits. We'll simulate it.
    compressed_size = len(compressed)
    
    ratio = original_size / compressed_size if compressed_size > 0 else 1.0
    return compressed.replace('$', ''), ratio

