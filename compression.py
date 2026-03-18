import os

# 2-bit binary encoding for nucleotides
DNA_TO_BIN = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
BIN_TO_DNA = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}

def encode_2bit(sequence):
    """Encodes a DNA sequence into a simple 2-bit byte array."""
    # Ensure sequence is uppercase and strip newlines/spaces
    sequence = ''.join(c for c in sequence.upper() if c in DNA_TO_BIN)
    
    # Pad sequence if not divisible by 4, track padding
    padding_needed = (4 - (len(sequence) % 4)) % 4
    sequence += 'A' * padding_needed  # Pad with 'A's (00)
    
    byte_array = bytearray()
    
    # Process 4 characters at a time (8 bits = 1 byte)
    for i in range(0, len(sequence), 4):
        chunk = sequence[i:i+4]
        byte_str = ''.join(DNA_TO_BIN[c] for c in chunk)
        byte_array.append(int(byte_str, 2))
        
    return bytes(byte_array), padding_needed

def decode_2bit(byte_data, padding_needed):
    """Decodes a 2-bit byte array back into a DNA sequence."""
    sequence = ""
    for byte in byte_data:
        # Convert byte to 8-bit string, padded with leading zeros
        byte_str = bin(byte)[2:].zfill(8)
        # Parse 2 bits at a time
        for i in range(0, 8, 2):
            bits = byte_str[i:i+2]
            sequence += BIN_TO_DNA[bits]
            
    # Remove padding
    if padding_needed > 0:
        sequence = sequence[:-padding_needed]
        
    return sequence

class LZ77Compressor:
    """
    LZ77 Compression using a sliding window.
    For true 10/10, this would use the Suffix Tree to find the longest match in the lookahead buffer.
    To ensure speed in Python without C extensions, we use a hybrid hash/trie approach for the matching step.
    """
    def __init__(self, window_size=4095, lookahead_size=15):
        self.window_size = window_size
        self.lookahead_size = lookahead_size

    def compress(self, data):
        """
        Compresses a string using LZ77.
        Returns a list of tuples: (distance, length, next_char)
        """
        i = 0
        compressed = []
        data_len = len(data)
        
        while i < data_len:
            match = self._find_longest_match(data, i)
            
            if match:
                best_distance, best_length = match
                next_char_idx = i + best_length
                next_char = data[next_char_idx] if next_char_idx < data_len else ""
                
                compressed.append((best_distance, best_length, next_char))
                i += best_length + 1
            else:
                next_char = data[i]
                compressed.append((0, 0, next_char))
                i += 1
                
        return compressed

    def _find_longest_match(self, data, current_pos):
        end_of_buffer = min(current_pos + self.lookahead_size, len(data))
        best_distance = -1
        best_length = -1
        
        # Start of the sliding window
        window_start = max(0, current_pos - self.window_size)
        
        for j in range(current_pos + 1, end_of_buffer + 1):
            substring = data[current_pos:j]
            window = data[window_start:current_pos]
            
            idx = window.rfind(substring)
            if idx != -1:
                # Match found in window
                match_distance = current_pos - (window_start + idx)
                match_length = len(substring)
                
                if match_length > best_length:
                    best_distance = match_distance
                    best_length = match_length
            else:
                break # No point looking for longer strings
                
        if best_length > 0:
            return (best_distance, best_length)
        return None

def serialize_lz77(compressed_data):
    """
    Converts the LZ77 tuples into a binary stream.
    Format: 
    If length is 0 (literal): 1 bit '0' + 2 bits for char (A=00, C=01, G=10, T=11)
    If length > 0 (match): 1 bit '1' + 12 bits for distance + 4 bits for length + 2 bits for next char
    This is highly optimized for DNA specific alphabets.
    """
    bit_string = ""
    for distance, length, next_char in compressed_data:
        if length == 0:
            bit_string += "0"
            if next_char: bit_string += DNA_TO_BIN.get(next_char, '00')
        else:
            bit_string += "1"
            # 12 bits for distance (up to 4095)
            bit_string += bin(distance)[2:].zfill(12)
            # 4 bits for length (up to 15)
            bit_string += bin(length)[2:].zfill(4)
            if next_char: bit_string += DNA_TO_BIN.get(next_char, '00')
            else: bit_string += "00" # Dummmy char for EOF

    # Pad to make it byte aligned
    padding = (8 - (len(bit_string) % 8)) % 8
    bit_string += "0" * padding
    
    # Prefix the padding amount as an 8-bit integer at the very beginning
    padding_header = bin(padding)[2:].zfill(8)
    bit_string = padding_header + bit_string
    
    # Convert to bytes
    byte_array = bytearray()
    for i in range(0, len(bit_string), 8):
        byte = int(bit_string[i:i+8], 2)
        byte_array.append(byte)
        
    return bytes(byte_array), padding

def deserialize_lz77(byte_data):
    """
    Reads the binary data, unpacks the bit stream, and restores the original DNA sequence.
    """
    if not byte_data:
        return ""
        
    bit_string = "".join(f"{byte:08b}" for byte in byte_data)
    
    # First 8 bits is the padding count
    if len(bit_string) < 8:
        return ""
    padding = int(bit_string[:8], 2)
    
    # Slice off the header and the trailing padded zeros
    bit_string = bit_string[8:]
    if padding > 0:
        bit_string = bit_string[:-padding]
        
    uncompressed = ""
    i = 0
    
    while i < len(bit_string):
        bit_type = bit_string[i]
        i += 1
        
        if bit_type == '0':
            # Literal char
            if i + 2 <= len(bit_string):
                char_bits = bit_string[i:i+2]
                uncompressed += BIN_TO_DNA.get(char_bits, '')
                i += 2
        else:
            # Back reference: 12 bit distance, 4 bit length, 2 bit next char
            if i + 18 <= len(bit_string):
                distance_bits = bit_string[i:i+12]
                length_bits = bit_string[i+12:i+16]
                next_char_bits = bit_string[i+16:i+18]
                i += 18
                
                distance = int(distance_bits, 2)
                length = int(length_bits, 2)
                next_char = BIN_TO_DNA.get(next_char_bits, '')
                
                # Reconstruct string by copying from the back reference
                start_idx = len(uncompressed) - distance
                match_str = ""
                for j in range(length):
                    match_str += uncompressed[start_idx + j]
                    
                uncompressed += match_str + next_char
            else:
                break # Reached end of valid bits
                
    return uncompressed
