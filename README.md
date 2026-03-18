# 🧬 DNA Core: Advanced Genomic Compression & Analytics Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Algorithms](https://img.shields.io/badge/Algorithms-O(n)-brightgreen)
![Bioinformatics](https://img.shields.io/badge/Domain-Bioinformatics-purple)

**DNA Core** is a sophisticated, high-performance bioinformatics platform designed for the compression, analysis, and visualization of genomic sequences. 

Originally conceived as a rudimentary sequence compressor, this project has been engineered into a "10/10" professional-grade suite featuring $O(n)$ pattern matching, true byte-level binary compression workflows, and direct data pipelines to the National Center for Biotechnology Information (NCBI).

---

## ✨ Key Features

### 🚀 1. Algorithmic High-Performance Engine
* **Ukkonen's Suffix Tree ($O(n)$):** Implements a true linear-time Suffix Tree algorithm. Bypasses naive recursive limits, allowing for instantaneous indexing and pattern matching on massive string structures.
* **Fuzzy Pattern Matching (DFS):** Search for DNA motifs with mathematically configurable mismatch allowances (Levenshtein distances) to simulate and detect real biological mutations/SNPs.
* **Reverse Complement Scans:** Automatically processes and queries complementary bounding strands concurrently.

### 💾 2. True Binary Compression
* **LZ77 Sliding Window:** Maps and tokenizes repeated tandem substrings dynamically.
* **2-Bit Sequence Encoding:** Converts standard 8-bit ASCII representations (A, C, G, T) into tightly packed 2-bit architectural binary arrays (`.bin`), cutting baseline file sizes by explicitly 75% before LZ77 logic is applied. 
* **Zero-Loss Decoder System:** Includes a live validation parser testing payload integrity (Decompression testing mechanism).

### 🧬 3. Biological Analytics & Multi-Chromosome Architecture
* **Circos-Style Polar Plots:** If an uploaded FASTA file/NCBI fetch contains multiple genes/chromosomes, it beautifully renders proportional ring tracks depicting the literal genome architecture via Plotly.
* **K-mer Frequency Mapping:** Computes sequence substrings for isolating regulatory motifs.
* **Tandem Repeat (STR/VNTR) Detection:** Automatically detects back-to-back repetitive markers using continuous contiguous sequence scanning.
* **GC-Content Sliding Windows:** Uses interval overlapping sequences to output interactive graphs mapping GC vs. AT concentrations (critical for targeting horizontal gene transfers).

### ☁️ 4. Cloud Interoperability Hub
* **Direct NCBI Fetching (`Entrez`):** Skip local `.fasta` files. Directly type Sequence Accession IDs (e.g., `NM_000207.3`) into the app, and it will fetch the live verified genomic code over the cloud in seconds.
* **Multi-Coordinate Tracing:** Safely parses concatenated genome datasets using bounded strict `#` characters, ensuring overlapping calculations report absolute physical offsets mapping correctly to exact chromosome targets.

---

## 📂 Project Structure

```text
📁 DNA Sequence Compression/
│
├── 📄 app.py              # Main Streamlit dashboard orchestrating the UI and Logic.
├── 📄 suffix_tree.py      # Core implementation of Ukkonen's O(n) Suffix Tree algorithm.
├── 📄 compression.py      # Contains the LZ77 Compressor, 2-bit encoders, and deserializer engines.
├── 📄 analytics.py        # Abstract computational logic for K-Mers, STRs, and bio-metrics.
├── 📄 README.md           # Documentation for the project.
└── 📂 .venv/              # Isolated Python Virtual Environment.
```

---

## 🛠️ Installation & Setup

1. **Clone the Repository** and navigate to your folder:
   ```bash
   cd "DNA Sequence Compression"
   ```

2. **Activate your Virtual Environment** (depending on your OS):
   * *Windows (PowerShell):*
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   * *Mac/Linux:*
     ```bash
     source .venv/bin/activate
     ```

3. **Install Requirements:** (If not already installed)
   Ensure you have the required operational libraries:
   ```bash
   pip install streamlit plotly pandas biopython
   ```

---

## 💻 Usage

Run the web dashboard directly from your terminal using:

```bash
streamlit run app.py
```

### Navigating the UI:
1. **Input Parameters:** Use the sidebar to either upload a `.fasta` file or enter a valid NCBI Reference Sequence ID.
2. **Compression:** Navigate to the `Compression` tab to encode your string and download tightly packed `.bin` files. Verify decompression using the built-in validator.
3. **Sequence Analytics:** Use the `Sequence Analytics` tab to visually map chromosomes, parse out K-mers, review Tandem Repeats, and interact with the physical distribution of GC mapping.
4. **Search Engine:** Enter the `Search Engine` tab to use the Suffix Tree to instantly query your strand. Tweak the **Fuzzy Search Mismatches** slider to account for biological variances!

---

*Project successfully evolved into a real-world scientific analytical model.*