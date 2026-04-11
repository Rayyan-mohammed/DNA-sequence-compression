import streamlit as st

def render_tab5(pure_sequence, p_x):
    from analytics import find_orfs, smith_waterman_alignment
    st.header("🧬 Central Dogma Tracking: Open Reading Frames")
    st.write("Scans the entire chromosome searching for genetic ORFs (ATG to a Stop Codon) dynamically translating raw DNA instructions into mapped Protein/Amino Acid structures.")

    orfs = find_orfs(pure_sequence, min_protein_len=20)
    if orfs:
        st.success(f"Found {len(orfs)} potential protein-coding Open Reading Frames!")
        import pandas as pd

        # Show top 10 longest ORFs
        orf_data = []
        for i, orf in enumerate(orfs[:10]):
            orf_data.append({
                "Rank": i+1,
                "Start Index": orf['start'],
                "End Index": orf['end'],
                "Length (Aa)": orf['length'],
                "Protein Sequence": orf['protein'][:50] + "..." if len(orf['protein']) > 50 else orf['protein']
            })
        st.dataframe(pd.DataFrame(orf_data), use_container_width=True)

        # Plotly Visuals for ORFs
        lengths = [o['length'] for o in orfs]
        fig_orf = p_x.histogram(lengths, nbins=30, title="Protein Gene Density: Structural Distribution (Amino Acids)", labels={'value': 'Amino Acid Length'})
        st.plotly_chart(fig_orf)
    else:
        st.info("No large Protein-Coding sequences (ORFs) found. This chunk is structurally non-coding/regulatory.")

    st.divider()

    st.header("🔬 Global DNA Comparison Grid: Pairwise Sequence Alignment")
    st.write("Instead of linear compression, this algorithm computes genetic similarity maps. It's the ultimate DP computer science challenge (O(N*M)).")

    align_col1, align_col2 = st.columns(2)
    with align_col1:
        cmp_seq = st.text_area("Target Strand: Enter a 2nd smaller DNA Sequence to map:", "ACGTG").upper()
        cmp_seq = ''.join(c for c in cmp_seq if c in 'ACGT')
    with align_col2:
        val_match = st.number_input("Grid: Match Multiplier", min_value=1, max_value=10, value=2, step=1)
        val_miss = st.number_input("Grid: Mismatch Degrader", max_value=-1, value=-1, step=1)
        val_gap = st.number_input("Grid: Gap/Splice Penalty", max_value=-1, value=-2, step=1)

    if st.button("Launch Needleman-Wunsch / Smith-Waterman Alignment Engine"):
        if len(cmp_seq) < 3 or len(pure_sequence) < 3:
            st.error("Both inputs must contain structural bases for calculation.")
        elif len(cmp_seq) > 2000 or len(pure_sequence) > 2000:
            st.warning("Warning: DP matrix is O(N*M). Aligning grids larger than 2,000x2,000 blocks crashes RAM. Fetch a smaller sequence or reduce target.")
        else:
            with st.spinner("Building N-Dimensional Grid Map ..."):
                a1, a2, score = smith_waterman_alignment(pure_sequence, cmp_seq, val_match, val_miss, val_gap)
                st.metric("Matrix Confidence Score", score)

                st.write("**Target 1 (Primary):** `" + a1 + "`")
                st.write("**Target 2 (Compare):** `" + a2 + "`")

                matches = sum(1 for i, j in zip(a1, a2) if i == j and i != '-')
                total_len = max(len(a1), 1)
                if total_len > 0:
                    st.progress(matches / total_len, text=f"Total Genetic Conservation Map: {(matches / total_len)*100:.1f}%")