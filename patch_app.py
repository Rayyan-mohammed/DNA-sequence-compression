import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the specific block of code up to "with tab1:"
pattern = r"""# Ensure sequence exists before replacing UI
if st\.sidebar\.button\("Analyze & Compress", type="primary"\):
    # Strip delimiters for validation check
    pure_sequence = sequence\.replace\('#', ''\)
    valid_len = len\(pure_sequence\)
    if valid_len < 3:
        st\.error\("Please enter a DNA sequence of at least 3 valid bases \(A, C, G, T\)\."\)
    else:
        # Progress Bar Logic
        progress_bar = st\.progress\(0, text="Initializing Suffix Tree Construction\.\.\."\)
        start_time = time\.time\(\)

        # Append '\$' as terminal character
        tree_seq = sequence \+ '\$'

        progress_bar\.progress\(20, text="Building Ukkonen's O\(n\) Suffix Tree\.\.\."\)
        tree = SuffixTree\(tree_seq\)
        st\.session_state\['tree'\] = tree
        st\.session_state\['sequence'\] = sequence
        st\.session_state\['pure_sequence'\] = pure_sequence

        progress_bar\.progress\(50, text="Analyzing Biological Metrics\.\.\."\)       

        # --- Tabbed Interface ---
        tab1, tab2, tab3, tab4, tab5, tab6 = st\.tabs\(\["Compression", "Sequence Analytics", "Search Engine", "AI Diagnostics", "Genes & Alignment", "BWT & 3D Protein"\]\)

        with tab1:
            st\.header\("Binary & Semantic Compression"\)

            progress_bar\.progress\(70, text="Running LZ77 Binary Compression Engine\.\.\."\)

            col1, col2, col3 = st\.columns\(3\)
            col1\.metric\("Original Length", f"\{len\(pure_sequence\)\} bases"\)       
            original_bytes = len\(pure_sequence\) # Assuming 1 byte per ASCII char
            col1\.caption\(f"Original size: \{original_bytes\} bytes \(ASCII\)"\)      

            # 1\. 2-Bit Compression
            two_bit_data, pad = encode_2bit\(pure_sequence\)
            two_bit_size = len\(two_bit_data\)
            col2\.metric\("2-Bit Encoding Size", f"\{two_bit_size\} bytes", f"\{\(1 - two_bit_size/original_bytes\)\*100:\.1f\}% reduction"\)

            # 2\. LZ77 Compression
            with st\.spinner\("Running LZ77 Compression\.\.\."\):
                compressor = LZ77Compressor\(\)
                lz77_tuples = compressor\.compress\(pure_sequence\)
                lz77_bytes, lz77_pad = serialize_lz77\(lz77_tuples\)
                lz77_size = len\(lz77_bytes\)

            col3\.metric\("LZ77 \+ Binary Size", f"\{lz77_size\} bytes", f"\{\(1 - lz77_size/original_bytes\)\*100:\.1f\}% reduction"\)"""

new_code = """# Ensure sequence exists before replacing UI
if st.sidebar.button("Analyze & Compress", type="primary"):
    st.session_state['analyze_clicked'] = True
    st.session_state['current_seq'] = sequence
    st.session_state['current_seq_id'] = seq_id

if st.session_state.get('analyze_clicked', False):
    sequence = st.session_state['current_seq']
    seq_id = st.session_state['current_seq_id']
    pure_sequence = sequence.replace('#', '')
    
    valid_len = len(pure_sequence)
    if valid_len < 3:
        st.error("Please enter a DNA sequence of at least 3 valid bases (A, C, G, T).")
    else:
        # Build cached items only if the sequence has changed
        if st.session_state.get('last_built_sequence') != sequence:
            progress_bar = st.progress(0, text="Initializing Suffix Tree Construction...")
            
            tree_seq = sequence + '$'
            progress_bar.progress(20, text="Building Ukkonen's O(n) Suffix Tree...")
            tree = SuffixTree(tree_seq)
            
            progress_bar.progress(50, text="Running LZ77 Binary Compression Engine...")
            two_bit_data, pad = encode_2bit(pure_sequence)
            compressor = LZ77Compressor()
            lz77_tuples = compressor.compress(pure_sequence)
            lz77_bytes, lz77_pad = serialize_lz77(lz77_tuples)

            # Cache the outputs
            st.session_state['tree'] = tree
            st.session_state['two_bit_data'] = two_bit_data
            st.session_state['two_bit_size'] = len(two_bit_data)
            st.session_state['lz77_bytes'] = lz77_bytes
            st.session_state['lz77_size'] = len(lz77_bytes)
            st.session_state['pure_sequence'] = pure_sequence
            st.session_state['sequence'] = sequence
            st.session_state['last_built_sequence'] = sequence
            
            progress_bar.empty()

        # Load from cache
        tree = st.session_state['tree']
        two_bit_data = st.session_state['two_bit_data']
        two_bit_size = st.session_state['two_bit_size']
        lz77_bytes = st.session_state['lz77_bytes']
        lz77_size = st.session_state['lz77_size']

        # --- Tabbed Interface ---
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Compression", "Sequence Analytics", "Search Engine", "AI Diagnostics", "Genes & Alignment", "BWT & 3D Protein"])

        with tab1:
            st.header("Binary & Semantic Compression")
            col1, col2, col3 = st.columns(3)
            col1.metric("Original Length", f"{len(pure_sequence)} bases")       
            original_bytes = len(pure_sequence)
            col1.caption(f"Original size: {original_bytes} bytes (ASCII)")      

            col2.metric("2-Bit Encoding Size", f"{two_bit_size} bytes", f"{(1 - two_bit_size/original_bytes)*100:.1f}% reduction")
            col3.metric("LZ77 + Binary Size", f"{lz77_size} bytes", f"{(1 - lz77_size/original_bytes)*100:.1f}% reduction")"""

import sys
if not re.search(pattern, content):
    print("Could not find the exact pattern!")
    sys.exit(1)
    
new_content = re.sub(pattern, new_code, content, count=1)
with open('app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Successfully patched app.py")