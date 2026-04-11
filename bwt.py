def get_bwt(sequence, max_len=10000):
    """
    Computes the Burrows-Wheeler Transform (BWT) of a sequence.
    (O(N^2) naive sort implemented for sub-10,000 lengths to bypass MemoryErrors)
    """
    is_truncated = False
    if len(sequence) > max_len:
        sequence = sequence[:max_len]
        is_truncated = True
        
    s = sequence + '$'
    # Generate all cyclic rotations
    rotations = sorted(s[i:] + s[:i] for i in range(len(s)))
    # The BWT is simply the last column of the sorted matrix
    bwt_string = "".join(row[-1] for row in rotations)
    
    return bwt_string, is_truncated

def inverse_bwt(bwt_string):
    """
    Reconstructs the original sequence from the BWT string.
    This demonstrates the reversibility properties mapping Last-to-First loops.
    """
    table = [""] * len(bwt_string)
    for i in range(len(bwt_string)):
        table = sorted(bwt_string[i] + table[i] for i in range(len(bwt_string)))
        
    for row in table:
        if row.endswith('$'):
            return row.rstrip('$')
    return ""