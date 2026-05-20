# SBS_Games: The Illumina Sequencing Simulator 

**SBS_Games** is an interactive, terminal-based educational game designed to teach the complex biochemistry, optics, and physics behind **Illumina Sequencing by Synthesis (SBS)**.

Instead of just looking at a FASTQ file, you take the driver's seat as both the **Bioinformatician** and the **Fluidics Controller**. You must interpret raw optical signals, manage chemical reactions, and deal with the inevitable entropy of a real sequencing run.

---

## Key Features

### 1. Dual Chemistry Modes (`SBS.simulator.py`)
Choose between the two primary detection systems used in modern genomics:
- **4-Channel Chemistry (e.g., MiSeq/HiSeq):** A traditional 1-to-1 mapping where each base (A, T, C, G) has its own unique fluorescent dye.
- **2-Channel Chemistry (e.g., NextSeq/NovaSeq):** A faster, more complex system using only two optical sensors (Blue and Green).

### 2. Loading Optimization (`cluster_density.py`)
Master the first step of any run: **Loading Concentration**.
- Seed clusters onto a 10x10 flowcell grid.
- Balance between low yield (underclustering) and overlapping signals (overclustering).
- Calculate your **Pass Filter (PF)** rate and see how much usable data you produced.

### 3. Index Hopping & Demultiplexing (`index_hopping.py`)
Sequence the 8bp sample barcode in a multiplexed pool.
- Experience the "interference" from other samples.
- See how miscalling a single base in the index leads to **Index Hopping**, where a read is assigned to the wrong sample.

### 4. Paired-End Bridge Turn (`paired_end_bridge.py`)
Flip the physical molecules to sequence the reverse side.
- Watch a text-based simulation of **Bridge Amplification**.
- Experience why **Read 2 (R2)** always has higher noise and lower quality scores than Read 1.

---

## Installation & Usage

### Prerequisites
- **Python 3.x**

### Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/malmarri/SBS_Games.git
   cd SBS_Games
   ```

2. **Choose your game:**
   ```bash
   python3 cluster_density.py    # Master loading
   python3 SBS.simulator.py      # Call bases and manage fluidics
   python3 index_hopping.py      # Resolve sample barcodes
   python3 paired_end_bridge.py  # Sequence the reverse strand
   ```

---

## 📖 How to Play

1. **Start the Run:** Select your chemistry (2-channel or 4-channel).
2. **Observe the Signal:** Look at the bar charts representing the optical intensity in each color channel.
3. **Call the Base:** Type `A`, `T`, `C`, or `G` based on the dominant signal.
   - *Tip:* In 2-Channel mode, no signal (Dark) means `G`!
4. **Maintain the Sequencer:** Type `cleave` when prompted to prepare the molecules for the next cycle.
5. **Survive the Run:** See if you can accurately sequence the full 20bp template before the dephasing noise makes the data unreadable.

---

## 🎓 Educational Goals
- Understand why phasing issues limit read length.
- Learn the difference between raw signal intensity and "called" bases.
- Visualize how 2-channel chemistry simplifies optics but complicates interpretation.
- Connect the physical process of fluidics to the quality of the final data.
