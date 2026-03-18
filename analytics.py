import re
from collections import Counter

def get_top_kmers(sequence, k=3, top_n=10):
    """
    Finds the most frequent K-mers (substrings of length k) in the DNA sequence.
    Returns a list of tuples: [(kmer, count), ...]
    """
    if len(sequence) < k:
        return []
        
    # Generate all kmers
    kmers = [sequence[i:i+k] for i in range(len(sequence)-k+1)]
    
    # Count and return top N
    return Counter(kmers).most_common(top_n)

def find_tandem_repeats(sequence, min_pattern_len=2, max_pattern_len=15):
    """
    Detects Short Tandem Repeats (STRs) or Variable Number Tandem Repeats (VNTRs).
    Looks for patterns repeating consecutively back-to-back.
    """
    results = []
    found_spans = []  # To avoid reporting sub-repeats inside larger repeats
    
    # Look for repeats of varying motif lengths
    for pat_len in range(min_pattern_len, max_pattern_len + 1):
        # Regex: match a motif of strict length, followed by itself at least 2 more times (total 3+ times)
        pattern = r'([ACGT]{{{}}})\1{{2,}}'.format(pat_len)
        
        for match in re.finditer(pattern, sequence):
            start = match.start()
            end = match.end()
            
            # Check if this span is already covered by a larger tandem repeat observation
            is_sub_span = False
            for (fs, fe) in found_spans:
                if start >= fs and end <= fe:
                    is_sub_span = True
                    break
                    
            if not is_sub_span:
                motif = match.group(1)
                full_match = match.group(0)
                repeats = len(full_match) // pat_len
                
                results.append({
                    'Motif': motif,
                    'Repeats': repeats,
                    'Start Index': start,
                    'Total Length': len(full_match)
                })
                found_spans.append((start, end))
                
    # Sort by the most significant clinical/structural impact (longest overall repeated span)
    results = sorted(results, key=lambda x: x['Total Length'], reverse=True)
    return results
