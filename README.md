# 🧬 Advanced DNA Sequence Compression & Analytics

A comprehensive bioinformatics and computer science portfolio project built to perform industry-grade analysis, binary compression, and visualization of genetic data. 

Built using **Python 3**, **Streamlit**, and **Plotly**, this application bridges the gap between raw data manipulation and interactive biological research. It features highly optimized data structures (O(n) Suffix Trees), classical string transformations (BWT), and modern Machine Learning heuristics.

## ✨ Features & Capabilities

### 🗜️ 1. High-Performance Text Algorithms (Compression & Searching)
*   **Ukkonen's Suffix Tree (O(n)):** Builds an exact suffix tree for the entire sequence in linear time. Used for sub-string searching, extracting Longest Repeated Substrings (LRS), and feeding exact pattern matches.
*   **LZ77 Binary Compression:** Translates repetitive DNA motifs into (distance, length, character) back-references and serializes the output directly to binary .bin files, reducing genetic map sizes significantly.
*   **2-Bit Nucleotide Encoding:** An industry-standard mathematical compression mapping A, C, G, T to deterministic 2-bit bytes representing a hard 75% structural reduction.
*   **Burrows-Wheeler Transform (BWT):** Employs string block rotations and lexicographical sorting, paving the way for maximum RLE (Run-Length Encoding) often used in modern aligners like Bowtie & BWA.

### 🔬 2. Biological Analytics & The Central Dogma
*   **Pairwise Sequence Alignment:** Dynamic Programming (Needleman-Wunsch / Smith-Waterman) to compute genetic similarity score maps with adjustable gap/mismatch penalties (O(N*M) complexity constraint).
*   **Open Reading Frame (ORF) Detection:** Dynamically scans the DNA sequence for ATG (Start) and TAA/TAG/TGA (Stop) codons, automatically compiling the longest protein-coding amino acid chains.
*   **K-mer Motif Polling:** A sliding window computational matrix tracking the frequency of K-length sequences representing repeating fragments. 
*   **Tandem Repeats Finder:** Extracts continuous short tandem repeats (STRs/VNTRs) commonly used in forensic criminal genetics.

### 🤖 3. Predictive Modeling (AI Diagnostics)
*   **DNABERT Model Simulation:** Hooks into the Hugging Face 	ransformers layout logic to analyze genetic text context and estimate Promoter site confidence scores, mapping possible regulatory areas (simulated within Streamlit constraints).

### 🖥️ 4. 3D WebGL Protein Rendering
*   **PDB Atomic Integrations:** Utilizes py3Dmol and stmol to interactively render crystal structures directly within the UI. Real-time zooming and spatial tracking for representations of AlphaFold or known X-Ray structures.

### 📡 5. Direct Data Bridging
*   **Integrated Sample References:** Local mappings of COVID-19, Human BRCA1, E.coli, and Synthetic datasets.
*   **NCBI Entrez Cloud Sync:** Allows direct pulling of .fasta structures from the National Center for Biotechnology Information (NCBI) using valid Accession IDs. 

---

## 🛠️ Tech Stack
*   **Languages:** Python 3.11+
*   **Core Libraries:** streamlit, pandas, 
umpy, iopython, plotly
*   **Advanced Rendering:** stmol, py3Dmol
*   **Environment:** Mapped via equirements.txt for out-of-the-box Streamlit Community Cloud hosting.

---

## 🚀 Installation & Local Development

1. **Clone the repository:**
   \\\ash
   git clone https://github.com/Rayyan-mohammed/DNA-sequence-compression.git
   cd DNA-sequence-compression
   \\\

2. **Create a Virtual Environment (Optional but Recommended):**
   \\\ash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\Activate
   \\\

3. **Install Dependencies:**
   \\\ash
   pip install -r requirements.txt
   \\\

4. **Launch the Application:**
   \\\ash
   streamlit run app.py
   \\\
   
5. **Using the App:**
   - Select an input method from the sidebar (Text, Local FASTA, Datasets, or NCBI).
   - Press **Analyze & Compress**.
   - Navigate the top Tabs to explore different algorithms (Compression, Alignment, BWT, 3D Proteins).

---

## 📝 File Overview
*   **\pp.py\**: Main entry point; builds Streamlit UI layout and manages state caching.
*   **\suffix_tree.py\**: Ukkonen's O(n) Suffix Tree algorithm implementation logic.
*   **\lz77_compression.py\**: Serialization mapping and 2-bit + LZ77 encoder models.
*   **\nalytics.py\**: K-mers, Tandem Repeats, ORFs, and Smith-Waterman matrices.
*   **\wt.py\**: Burrows-Wheeler formatting mathematics.
*   **\	ab_components.py\**: Modular abstraction isolating heavy UI elements from the main application thread.
*   **\i_engine.py\**: Simulated NLP transformer heuristic engine setup.

---

*This application was successfully designed to marry intense backend computer science optimization to intuitive, interactive frontend biology capabilities.*
