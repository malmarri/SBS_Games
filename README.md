# SBS_Games: The Illumina Sequencing Simulator 🧬

**SBS_Games** is an interactive, terminal-based educational game designed to teach the complex biochemistry, optics, and physics behind **Illumina Sequencing by Synthesis (SBS)**.

Instead of just looking at a FASTQ file, you take the driver's seat as both the **Bioinformatician** and the **Fluidics Controller**. You must interpret raw optical signals, manage chemical reactions, and deal with the inevitable entropy of a real sequencing run.

---

## 🕹️ Key Features

### 1. Dual Chemistry Modes
Choose between the two primary detection systems used in modern genomics:
- **4-Channel Chemistry (e.g., MiSeq/HiSeq):** A traditional 1-to-1 mapping where each base (A, T, C, G) has its own unique fluorescent dye.
- **2-Channel Chemistry (e.g., NextSeq/NovaSeq):** A faster, more complex system using only two optical sensors (Blue and Green) to identify four bases through signal combinations—including the infamous **"Dark G"**.

### 2. The Phasing & Pre-phasing Model
The game simulates a "cluster" of 1,000 identical DNA molecules. As cycles progress, your cluster will naturally lose synchronicity:
- **Phasing:** Some molecules fail to cleave their terminators and fall one cycle behind.
- **Pre-phasing:** Some molecules fail to incorporate a terminator and jump one cycle ahead.
Watch your "Optical Sensor Output" get "muddier" as the run progresses, perfectly illustrating why Phred Q-scores drop at the end of a read.

### 3. Interactive Fluidics Control
You aren't just calling bases. After every incorporation, you must manually trigger the **Cleave** step. 
- **Success:** Keeps your cluster mostly in sync.
- **Failure:** Skip a cleave, and your cluster dephases rapidly, making future base calls nearly impossible.

### 4. Embedded Micro-Lessons
At key milestones (Cycles 5, 10, 15, and 20), the game pauses to explain the science behind what you're seeing:
- How Reversible Terminators work.
- The physics of Bridge Amplification.
- The mathematical derivation of Phred Quality Scores.

---

## 🚀 Installation & Usage

### Prerequisites
- **Python 3.x**

### Quick Start
1. **Clone the repository:**
   ```bash
   git clone https://github.com/malmarri/SBS_Games.git
   cd SBS_Games
   ```

2. **Run the simulator:**
   ```bash
   python3 SBS.simulator.py
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
- Understand why deamination and dephasing limit read length.
- Learn the difference between raw signal intensity and "called" bases.
- Visualize how 2-channel chemistry simplifies optics but complicates interpretation.
- Connect the physical process of fluidics to the quality of the final data.

---

**Developed by:** Mohamed Al-Marri
**License:** MIT
