import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from suffix_tree import SuffixTree, compress_sequence
from compression import encode_2bit, LZ77Compressor, serialize_lz77
from analytics import get_top_kmers, find_tandem_repeats
from io import BytesIO
import time
from Bio import SeqIO

st.set_page_config(page_title="DNA Sequence Compression", page_icon="🧬", layout="wide")

st.title("🧬 Advanced DNA Sequence Compression & Analytics")
st.write("""
A 10/10 bioinformatics tool using Suffix Trees, LZ77 Binary Compression, and K-mer Analytics.
""")

# --- Sidebar Controls ---
st.sidebar.header("Input Data")
input_method = st.sidebar.radio("Input Method:", ["Text Input", "Upload FASTA File"])

sequence = ""
seq_id = "Custom"

if input_method == "Text Input":
    sequence = st.sidebar.text_area("Enter DNA Sequence:", "ACGTACGTGACG").upper().replace("\n", "").replace(" ", "")
else:
    uploaded_file = st.sidebar.file_uploader("Upload a .fasta file", type=["fasta", "fa", "txt"])
    if uploaded_file is not None:
        try:
            # Parse FASTA
            stringio = uploaded_file.getvalue().decode("utf-8")
            from io import StringIO
            records = list(SeqIO.parse(StringIO(stringio), "fasta"))
            if records:
                sequence = str(records[0].seq).upper()
                seq_id = records[0].id
                st.sidebar.success(f"Loaded {seq_id} (Length: {len(sequence)})")
        except Exception as e:
            st.sidebar.error(f"Error parsing file: {e}")

# Validate sequence
sequence = ''.join(c for c in sequence if c in 'ACGT')

if st.sidebar.button("Analyze & Compress", type="primary"):
    if len(sequence) < 3:
        st.error("Please enter a DNA sequence of at least 3 valid bases (A, C, G, T).")
    else:
        # Progress Bar Logic
        progress_bar = st.progress(0, text="Initializing Suffix Tree Construction...")
        start_time = time.time()
        
        # Append '$' as terminal character
        tree_seq = sequence + '$'
        
        progress_bar.progress(20, text="Building Ukkonen's O(n) Suffix Tree...")
        tree = SuffixTree(tree_seq)
        st.session_state['tree'] = tree
        st.session_state['sequence'] = sequence
        
        progress_bar.progress(50, text="Analyzing Biological Metrics...")
        
        # --- Tabbed Interface ---
        tab1, tab2, tab3 = st.tabs(["Compression", "Sequence Analytics", "Search Engine"])
        
        with tab1:
            st.header("Binary & Semantic Compression")
            
            progress_bar.progress(70, text="Running LZ77 Binary Compression Engine...")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Original Length", f"{len(sequence)} bases")
            original_bytes = len(sequence) # Assuming 1 byte per ASCII char
            col1.caption(f"Original size: {original_bytes} bytes (ASCII)")
            
            # 1. 2-Bit Compression
            two_bit_data, pad = encode_2bit(sequence)
            two_bit_size = len(two_bit_data)
            col2.metric("2-Bit Encoding Size", f"{two_bit_size} bytes", f"{(1 - two_bit_size/original_bytes)*100:.1f}% reduction")
            
            # 2. LZ77 Compression
            with st.spinner("Running LZ77 Compression..."):
                compressor = LZ77Compressor()
                lz77_tuples = compressor.compress(sequence)
                lz77_bytes, lz77_pad = serialize_lz77(lz77_tuples)
                lz77_size = len(lz77_bytes)
                
            col3.metric("LZ77 + Binary Size", f"{lz77_size} bytes", f"{(1 - lz77_size/original_bytes)*100:.1f}% reduction")
            
            # Download Buttons
            st.download_button("Download 2-Bit Encoded (.bin)", data=two_bit_data, file_name=f"{seq_id}_2bit.bin")
            st.download_button("Download LZ77 Encoded (.bin)", data=lz77_bytes, file_name=f"{seq_id}_lz77.bin")
            
            st.info("The LZ77 compression algorithm leverages repeated sequences (which our Suffix Tree identifies) to replace duplicate DNA strands with back-references, drastically reducing file size for highly repetitive genomes.")

            st.subheader("Decompression Decoder Test")
            if st.button("Test Payload Decompression Validity"):
                from compression import deserialize_lz77
                with st.spinner("Decoding binary stream..."):
                    restored_sequence = deserialize_lz77(lz77_bytes)
                    if restored_sequence == sequence:
                        st.success("✅ DECOMPRESSION SUCCESS: The unpacked binary exactly matches the original DNA Sequence with zero loss!")
                    else:
                        st.error("❌ DECOMPRESSION FAILED: Data got corrupted.")
                        st.write(f"Original Length: {len(sequence)}")
                        st.write(f"Restored Length: {len(restored_sequence)}")

        with tab2:
                st.header("Biological Analysis")
                
                # 1. K-mer Analysis
                st.subheader("1. K-mer Frequency Analysis")
                st.write("K-mers are substrings of length `k`. Finding frequent K-mers is vital for genome assembly and identifying regulatory motifs.")
                k_val = st.slider("Select K-mer length (k):", min_value=2, max_value=12, value=3)
                top_kmers = get_top_kmers(sequence, k=k_val, top_n=10)
                
                if top_kmers:
                    kmer_labels = [item[0] for item in top_kmers]
                    kmer_counts = [item[1] for item in top_kmers]
                    fig_kmers = px.bar(x=kmer_labels, y=kmer_counts, 
                                       labels={'x': 'K-mer Motif', 'y': 'Frequency'},
                                       title=f"Top 10 most frequent {k_val}-mers",
                                       color=kmer_counts, color_continuous_scale="Viridis")
                    st.plotly_chart(fig_kmers)
                else:
                    st.write("Sequence too short for this K value.")

                # 2. Tandem Repeats
                st.subheader("2. Tandem Repeats (STRs / VNTRs)")
                st.write("Tandem repeats occur when a pattern of nucleotides repeats directly back-to-back. These are often used as genetic markers for diseases or DNA profiling.")
                tandems = find_tandem_repeats(sequence)
                if tandems:
                    import pandas as pd
                    st.dataframe(pd.DataFrame(tandems), hide_index=True, use_container_width=True)
                else:
                    st.info("No significant contiguous tandem repeats found in this sequence.")
                
                # 3. LRS
                st.subheader("3. Longest Repeated Substring (Suffix Tree)")
                lrs = tree.longest_repeated_substring()
                st.code(lrs)
                st.write(f"Length: {len(lrs)} bases. (This is the longest pattern that appears at least twice *anywhere* in the genome, found algorithmically in O(n) time via the Suffix Tree).")
                
                # 4. Nucleotide Composition (Plotly)
                st.subheader("4. Global Composition")
                counts = {'A': sequence.count('A'), 'C': sequence.count('C'), 
                          'G': sequence.count('G'), 'T': sequence.count('T')}
                fig = px.bar(x=list(counts.keys()), y=list(counts.values()), 
                             labels={'x': 'Nucleotide', 'y': 'Frequency'},
                             title="Nucleotide Composition",
                             color=list(counts.keys()),
                             color_discrete_map={'A':'#1f77b4', 'C':'#ff7f0e', 'G':'#2ca02c', 'T':'#d62728'})
                st.plotly_chart(fig)
                
                st.subheader("GC-Content Window Analysis")
                window_size = max(10, len(sequence)//20)
                if window_size > 0:
                    gc_content = []
                    for i in range(0, len(sequence) - window_size + 1, max(1, window_size//5)):
                        window = sequence[i:i+window_size]
                        gc = (window.count('G') + window.count('C')) / window_size * 100
                        gc_content.append((i, gc))
                    
                    if gc_content:
                        x_vals = [item[0] for item in gc_content]
                        y_vals = [item[1] for item in gc_content]
                        fig_gc = px.line(x=x_vals, y=y_vals, labels={'x': 'Sequence Position', 'y': 'GC %'}, title=f"GC Content (Window = {window_size})")
                        st.plotly_chart(fig_gc)
                
                # --- Export Analytics ---
                st.divider()
                st.subheader("Export Analytics Report")
                import pandas as pd
                
                # Build an overview dictionary
                analytics_summary = {
                    "Metric": [
                        "Sequence Length", 
                        "Count A", "Count C", "Count G", "Count T", 
                        "Longest Repeated Substring Length",
                        "Tandem Repeat Loci Count"
                    ],
                    "Value": [
                        len(sequence),
                        counts['A'], counts['C'], counts['G'], counts['T'],
                        len(lrs),
                        len(tandems) if tandems else 0
                    ]
                }
                
                df_summary = pd.DataFrame(analytics_summary)
                csv_data = df_summary.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="Download Analytics Summary (.csv)",
                    data=csv_data,
                    file_name=f"{seq_id}_analytics.csv",
                    mime="text/csv"
                )

        with tab3:
            st.header("O(m) Fast Suffix Tree Search")
            st.info("The Suffix tree guarantees O(m) search time (where m is the length of your query) regardless of how massive the genome gets.")

# Separated search input so it works without requiring re-building the tree
if 'tree' in st.session_state:
    st.divider()
    search_col1, search_col2 = st.columns([3, 1])
    with search_col1:
        pattern = st.text_input("Enter DNA Motif/Pattern to search:", key="search_bar").upper()
    with search_col2:
        st.write("") # Spacer
        st.write("") # Spacer
        reverse_comp = st.checkbox("Also Search Reverse Complement", value=True)

    if pattern:
        pattern = ''.join(c for c in pattern if c in 'ACGT')
        if pattern:
            tree = st.session_state['tree']
            seq = st.session_state['sequence']
            
            results = tree.find_all_occurrences(pattern)
            
            if reverse_comp:
                complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
                rc_pattern = "".join(complement.get(c, c) for c in reversed(pattern))
                rc_results = tree.find_all_occurrences(rc_pattern)
                st.write(f"Reverse Complement (`{rc_pattern}`): Found {len(rc_results)} times")
                results.extend(rc_results)
                
            st.success(f"Pattern '{pattern}' found {len(results)} times!")
            
            if results:
                # Show results in a dataframe/table
                import pandas as pd
                df = pd.DataFrame({"Position (Index)": sorted(list(set(results)))})
                st.dataframe(df, use_container_width=True)
                
                # Download search results
                csv_hits = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Search Hits (.csv)",
                    data=csv_hits,
                    file_name=f"{seq_id}_search_{pattern}.csv",
                    mime="text/csv"
                )
