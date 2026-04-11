<div align="center">
  <h1>🧬 Advanced DNA Sequence Compression & Bioinformatics Analytics App</h1>
  <p><i>An Industry-Grade, High-Performance Computational Biology Suite.</i></p>
  
  ![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue?style=for-the-badge&logo=python)
  ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
  ![Bioinformatics](https://img.shields.io/badge/Bioinformatics-O(n)_Complexity-success?style=for-the-badge)
  ![Plotly](https://img.shields.io/badge/Plotly-Data_Viz-indigo?style=for-the-badge&logo=plotly)
  ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)
</div>

<br>

## 🔬 Project Overview

This repository houses an advanced, portfolio-grade **DNA Sequence Compression and Analytics Engine** designed to bridge the gap between raw genetic data and interactive biological research. It was built from the ground up to solve complex Computer Science problems applied to Genomics, combining rigorous mathematical mappings, **O(n)** algorithmic data structures, and WebGL-based atomic rendering within a seamless UI.

Whether you are pulling live genomes from the **NCBI Entrez Cloud**, finding Open Reading Frames (ORFs) to translate DNA into Proteins, or compressing raw ATCG strings via Ukkonen's Suffix Trees and LZ77 mechanisms—this tool exposes powerful algorithms directly to the browser.

---

## 🌟 Comprehensive Feature Architecture

### 🗜️ 1. High-Performance Text Algorithms (Compression & Search)
*   **Ukkonen's Suffix Tree (O(n)):** Bypasses brute-force `O(n²)` search limitations by dynamically constructing a suffix tree in linear time. This structure is the backbone for identifying Longest Repeated Substrings (LRS) and exact pattern tracking.
*   **LZ77 + 2-Bit Binary Compression Pipeline:** 
    *   Maps biological sequences (`A_00`, `C_01`, `G_10`, `T_11`) into hard 2-bit bytes immediately reducing raw memory overhead by 75%.
    *   Passes data into a Ziv-Lempel (LZ77) sliding-window compressor, exploiting biological repeats mapped by the Suffix tree to substitute massive chunks with `(distance, length, next_char)` reference tuples. Supports lossless binary `.bin` export and decoding.
*   **Burrows-Wheeler Transform (BWT):** Employs lexicographical string rotations to group DNA motifs into repetitive character blocks. This unlocks extreme Run-Length Encoding (RLE) compressibility—the foundational math behind high-end aligners like Bowtie and BWA.

### 🧬 2. Biological Analytics & The Central Dogma
*   **Smith-Waterman Dynamic Programming (O(N * M)):** Implements pairwise sequence alignment using an N-Dimensional Grid. Users can tweak Match Multipliers, Mismatch Degraders, and Gap/Splice Penalties to generate biological conservation scores between target strands.
*   **Open Reading Frame (ORF) Detection:** Parses structural DNA for Initiation (`ATG`) and Termination (`TAA`, `TAG`, `TGA`) codons. Once isolated, the engine mimics the biological Ribosome, translating the genetic code directly into Amino Acid / Protein sequences.
*   **K-mer Frequency Analysis:** Uses a sliding-window array to plot (via Plotly) overlapping sub-sequences of length `K`. Essential for genome assembly, error-correction, and mapping promoter regions. 
*   **Tandem Repeats Finder (STR/VNTR):** Detects consecutive structural repeats in the sequence, commonly utilized in DNA fingerprinting and forensic mapping.

### 🔬 3. 3D Atomic Protein Rendering (WebGL)
*   **Py3DMol & stmol Integration:** Translates the conceptual DNA findings into visual massive structural biology. Through interactive WebGL canvases, users can render, rotate, and zoom into real PDB (Protein Data Bank) crystal frameworks like COVID-19 Protease, Human Hemoglobin, or standard DNA Double-Helices natively in the browser.

### 🤖 4. AI & Machine Learning Diagnostics 
*   **DNABERT Simulation Engine:** Integrates simulated HuggingFace NLP transformer logic to analyze genetic text context and estimate Promoter Site Confidence Scores. Demonstrates the capability of treating genetic chains as natural language for large language models (LLMs).

---

## 📡 Data Bridging & Import Methods
- **Raw Text:** Manual copy-pasting of short experimental sequences.
- **Benchmarking Datasets:** Pre-loaded reference FASTA mappings (SARS-CoV-2, E.Coli, BRCA1, Synthetic combinations).
- **Upload Workspace:** Local `.fasta` parsing support using Biopython.
- **NCBI Entrez API Sync:** Bypass local storage entirely by fetching current reference genomes directly from the National Center for Biotechnology Information cloud infrastructure via Accession ID (e.g., `NC_045512`).

---

## 🛠️ Technology Stack
*   **Frontend / Framework:** Streamlit
*   **Language / Backend:** Python 3.11+
*   **Mathematics & Analytics:** `numpy`, `pandas`, `scipy`
*   **Bioinformatics Tools:** `biopython`
*   **Visualization:** `plotly`, `py3Dmol`, `stmol`
*   **Version Control:** Git, Streamlit Community Cloud architecture.

---

## ⚙️ Local Installation & Development

If you'd like to run and test this code on your local machine, follow these instructions to use the isolated virtual environment setup:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Rayyan-mohammed/DNA-sequence-compression.git
   cd DNA-sequence-compression
   ```

2. **Create and Activate a Virtual Environment:**
   *   **Windows:**
       ```bash
       python -m venv .venv
       .\.venv\Scripts\activate
       ```
   *   **Mac/Linux:**
       ```bash
       python3 -m venv .venv
       source .venv/bin/activate
       ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Application:**
   ```bash
   streamlit run app.py
   ```
   *(Your browser will automatically open to `http://localhost:8502`)*

---

## 📂 Repository Structure
```text
├── app.py                  # Core application entrypoint & Streamlit state manager
├── analytics.py            # Biological algorithms (Smith-Waterman DP, ORFs, K-mers)
├── bwt.py                  # Burrows-Wheeler Transform string manipulation math
├── lz77_compression.py     # Binary bit-packing & Tuple serialization dictionaries
├── suffix_tree.py          # O(n) Ukkonen Suffix Tree node and edge traversal classes
├── ai_engine.py            # HuggingFace NLP simulator logic
├── tab_components.py       # Decoupled UI modules parsing analytics & Py3D WebGL viewers
├── requirements.txt        # Isolated OS-agnostic Pip dependency locking
└── datasets/               # Folder housing sample .fasta test files
```

---
<div align="center">
  <i>Designed to marry intense backend computer science optimization to intuitive, interactive frontend biology capabilities.</i>
</div>
# 🧬 Advanced DNA Sequence Compression & Analytics

A comprehensive bioinformatics and computer science portfolio project built to perform industry-grade analysis, binary compression, and visualization of genetic data. 

Built using **Python 3**, **Streamlit**, and **Plotly**, this application bridges the gap between raw data manipulation and interactive biological research. It features highly optimized data structures (O(n) Suffix Trees), classical string transformations (BWT), and modern Machine Learning heuristics.

## ✨ Features & Capabilities

### 🗜️ 1. High-Performance Text Algorithms (Compression & Searching)
*   **Ukkonen\'s Suffix Tree (O(n)):** Builds an exact suffix tree for the entire sequence in linear time. Used for sub-string searching, extracting Longest Repeated Substrings (LRS), and feeding exact pattern matches.
*   **LZ77 Binary Compression:** Translates repetitive DNA motifs into (distance, length, character) back-references and serializes the output directly to binary .bin files, reducing genetic map sizes significantly.
*   **2-Bit Nucleotide Encoding:** An industry-standard mathematical compression mapping \A\, \C\, \G\, \T\ to deterministic 2-bit bytes representing a hard 75% structural reduction.
*   **Burrows-Wheeler Transform (BWT):** Employs string block rotations and lexicographical sorting, paving the way for maximum RLE (Run-Length Encoding) often used in modern aligners like Bowtie & BWA.

### 🔬 2. Biological Analytics & The Central Dogma
*   **Pairwise Sequence Alignment:** Dynamic Programming (Needleman-Wunsch / Smith-Waterman) to compute genetic similarity score maps with adjustable gap/mismatch penalties (O(N*M) complexity constraint).
*   **Open Reading Frame (ORF) Detection:** Dynamically scans the DNA sequence for \ATG\ (Start) and \TAA/TAG/TGA\ (Stop) codons, automatically compiling the longest protein-coding amino acid chains.
*   **K-mer Motif Polling:** A sliding window computational matrix tracking the frequency of K-length sequences representing repeating fragments. 
*   **Tandem Repeats Finder:** Extracts continuous short tandem repeats (STRs/VNTRs) commonly used in forensic criminal genetics.

### 🤖 3. Predictive Modeling (AI Diagnostics)
*   **DNABERT Model Simulation:** Hooks into the Hugging Face \	ransformers\ layout logic to analyze genetic text context and estimate Promoter site confidence scores, mapping possible regulatory areas (simulated within Streamlit constraints).

### 🖥️ 4. 3D WebGL Protein Rendering
*   **PDB Atomic Integrations:** Utilizes \py3Dmol\ and \stmol\ to interactively render crystal structures directly within the UI. Real-time zooming and spatial tracking for representations of AlphaFold or known X-Ray structures.

### 📡 5. Direct Data Bridging
*   **Integrated Sample References:** Local mappings of COVID-19, Human BRCA1, E.coli, and Synthetic datasets.
*   **NCBI Entrez Cloud Sync:** Allows direct pulling of \.fasta\ structures from the National Center for Biotechnology Information (NCBI) using valid Accession IDs. 

---

## 🛠️ Tech Stack
*   **Languages:** Python 3.11+
*   **Core Libraries:** \streamlit\, \pandas\, umpy\, \iopython\, \plotly*   **Advanced Rendering:** \stmol\, \py3Dmol*   **Environment:** Mapped via equirements.txt\ for out-of-the-box Streamlit Community Cloud hosting.

---

## 🚀 Installation & Local Development

1. **Clone the repository:**
   \\ash
   git clone https://github.com/Rayyan-mohammed/DNA-sequence-compression.git
   cd DNA-sequence-compression
   \
2. **Create a Virtual Environment (Optional but Recommended):**
   \\ash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\\Scripts\\Activate
   \
3. **Install Dependencies:**
   \\ash
   pip install -r requirements.txt
   \
4. **Launch the Application:**
   \\ash
   streamlit run app.py
   \   
5. **Using the App:**
   - Select an input method from the sidebar (Text, Local FASTA, Datasets, or NCBI).
   - Press **Analyze & Compress**.
   - Navigate the top Tabs to explore different algorithms (Compression, Alignment, BWT, 3D Proteins).

---

## 📝 File Overview
*   **\pp.py\**: Main entry point; builds Streamlit UI layout and manages state caching.
*   **\suffix_tree.py\**: Ukkonen\'s O(n) Suffix Tree algorithm implementation logic.
*   **\lz77_compression.py\**: Serialization mapping and 2-bit + LZ77 encoder models.
*   **\nalytics.py\**: K-mers, Tandem Repeats, ORFs, and Smith-Waterman matrices.
*   **\wt.py\**: Burrows-Wheeler formatting mathematics.
*   **\	ab_components.py\**: Modular abstraction isolating heavy UI elements from the main application thread.
*   **\i_engine.py\**: Simulated NLP transformer heuristic engine setup.

---

*This application was successfully designed to marry intense backend computer science optimization to intuitive, interactive frontend biology capabilities.*
