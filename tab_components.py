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
import time
import streamlit as st
import py3Dmol
from stmol import showmol
from bwt import get_bwt

def render_tab6(pure_sequence, px):
    st.header('🗜️ Burrows-Wheeler Transform (BWT) & FM-Index')
    st.write('The industry standard mapping technique behind Bowtie/BWA sequence aligners. Instead of simple LZ77 pattern references, BWT cyclically clusters matching characters locally forming massive identical runs perfect for Run-Length Encodings (RLE).')
    
    bwt_col, rle_col = st.columns(2)
    with bwt_col:
        st.subheader('BWT Encoding Engine')
        run_bwt = st.button('Transform DNA via BWT Matrix')
        if run_bwt:
            with st.spinner('Generating Matrix Map... (Capped at 5000 bases for UI memory)'):
                start = time.time()
                bwt_str, was_capped = get_bwt(pure_sequence, max_len=5000)
                st.metric('Transformation Time', f'{time.time() - start:.3f}s')
                st.success('Successfully generated BWT!')
                import re
                rle = [(m.group(1), len(m.group(0))) for m in re.finditer(r'(.)\\1*', bwt_str)]
                avg_run = sum(l for c, l in rle) / len(rle)
                st.write(f'**Average Consecutive Run-Length:** {avg_run:.2f} chars (Higher = Better Compression)')
                st.text_area('Last-Column Matrix Extract (BWT Output):', bwt_str, height=200)

    st.divider()
    st.header('🔬 3D Protein Visualizer: The Central Dogma Result')
    st.write('When DNA Translates into massive structural biology! This WebGL viewer allows real-time interactive atomic mapping.')
    st.info('Select a representative structural map. Translating random motifs directly into 3D requires advanced alpha-folding grids. We map known crystal layouts.')
    
    view_opt = st.selectbox('Select PDB Render Structure:', ['DNA Double-Helix (1BNA)', 'COVID-19 Protease (6LU7)', 'Human Hemoglobin (2HHB)'])
    pdb_map = {'DNA Double-Helix (1BNA)': '1BNA', 'COVID-19 Protease (6LU7)': '6LU7',  'Human Hemoglobin (2HHB)': '2HHB'}

    if st.button('Render Atomic Molecule', type='primary'):
        with st.spinner('Fetching PDB layout and mounting WebGL...'):
            viewer = py3Dmol.view(query=f\'pdb:{pdb_map[view_opt]}\')
            viewer.setStyle({'stick': {}})
            viewer.addSurface(py3Dmol.VDW, {'opacity': 0.5, 'color': 'spectrum'})
            viewer.zoomTo()
            viewer.spin(True)
            showmol(viewer, height=500, width=800)
            st.success('Atomic Map successfully rendered. Use your mouse to click and drag to view structure limits.')
