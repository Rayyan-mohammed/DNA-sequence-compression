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


# ==========================================
# ADVANCED BIOLOGY: THE CENTRAL DOGMA
# ==========================================
CODON_TABLE = {'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M', 'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T', 'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K', 'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R', 'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L', 'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P', 'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q', 'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R', 'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V', 'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A', 'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E', 'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G', 'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S', 'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L', 'TAC':'Y', 'TAT':'Y', 'TAA':'_', 'TAG':'_', 'TGC':'C', 'TGT':'C', 'TGA':'_', 'TGG':'W'}

def translate_to_protein(dna_sequence, start_idx=0):
    protein = []
    for i in range(start_idx, len(dna_sequence) - 2, 3):
        codon = dna_sequence[i:i+3]
        aa = CODON_TABLE.get(codon, 'X')
        if aa == '_':
            break
        protein.append(aa)
    return ''.join(protein)

def find_orfs(sequence, min_protein_len=20):
    orfs = []
    for frame in range(3):
        for i in range(frame, len(sequence) - 2, 3):
            if sequence[i:i+3] == 'ATG':
                protein = translate_to_protein(sequence, start_idx=i)
                if len(protein) >= min_protein_len:
                    end_idx = i + (len(protein) * 3) + 3
                    is_nested = any([i >= o['start'] and end_idx <= o['end'] for o in orfs])
                    if not is_nested:
                        orfs.append({'start': i, 'end': end_idx, 'frame': frame + 1, 'protein': protein, 'length': len(protein)})
    return sorted(orfs, key=lambda x: x['length'], reverse=True)

# ==========================================
# ADVANCED ALGORITHMS: DP ALIGNMENT
# ==========================================
def smith_waterman_alignment(seq1, seq2, match_score=2, mismatch_penalty=-1, gap_penalty=-1):
    import numpy as np
    n, m = len(seq1), len(seq2)
    score_matrix = np.zeros((n + 1, m + 1), dtype=int)
    max_score, max_pos = 0, (0, 0)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            match = score_matrix[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_penalty)
            delete = score_matrix[i - 1][j] + gap_penalty
            insert = score_matrix[i][j - 1] + gap_penalty
            score_matrix[i][j] = max(0, match, delete, insert)
            if score_matrix[i][j] >= max_score:
                max_score = score_matrix[i][j]
                max_pos = (i, j)
    align1, align2 = '', ''
    i, j = max_pos
    while score_matrix[i][j] > 0:
        current_score = score_matrix[i][j]
        diagonal_score = score_matrix[i - 1][j - 1]
        if seq1[i - 1] == seq2[j - 1] or current_score == diagonal_score + mismatch_penalty:
            align1 += seq1[i - 1]
            align2 += seq2[j - 1]
            i -= 1; j -= 1
        elif current_score == score_matrix[i - 1][j] + gap_penalty:
            align1 += seq1[i - 1]
            align2 += '-'
            i -= 1
        else:
            align1 += '-'
            align2 += seq2[j - 1]
            j -= 1
    return align1[::-1], align2[::-1], max_score
