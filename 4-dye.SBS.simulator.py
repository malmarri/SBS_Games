import time
import random
import sys

# ANSI color codes
COLORS = {
    'A': '\033[91m',  # Red
    'T': '\033[92m',  # Green
    'C': '\033[94m',  # Blue
    'G': '\033[93m',  # Yellow
    'INFO': '\033[96m', # Cyan for educational pop-ups
    'RESET': '\033[0m'
}
COLOR_NAMES = {'A': 'Red', 'T': 'Green', 'C': 'Blue', 'G': 'Yellow'}
COMPLEMENTS = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

def generate_template(length=20):
    return ''.join(random.choice(['A', 'T', 'C', 'G']) for _ in range(length))

def print_slow(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_lesson(title, text):
    """Formats educational pop-ups to stand out in the terminal."""
    print(f"\n{COLORS['INFO']}" + "★"*50)
    print(f"  LESSON UNLOCKED: {title}")
    print("★"*50)
    # Simple text wrapping for terminal readability
    words = text.split(' ')
    line = "  "
    for word in words:
        if len(line) + len(word) > 46:
            print(line)
            line = "  " + word + " "
        else:
            line += word + " "
    print(line)
    print("★"*50 + f"{COLORS['RESET']}\n")
    input("Press [ENTER] to continue the sequencing run...")
    print("\n")

def play_advanced_sbs():
    print_slow("=== ADVANCED ILLUMINA SBS SIMULATOR ===")
    print_slow("Initializing Flow Cell Cluster (1,000 molecules)...")
    
    # Color Key Explanation
    print("\n--- FLUOROPHORE COLOR KEY ---")
    print(f"{COLORS['A']}Adenine (A) flashes Red{COLORS['RESET']}")
    print(f"{COLORS['T']}Thymine (T) flashes Green{COLORS['RESET']}")
    print(f"{COLORS['C']}Cytosine (C) flashes Blue{COLORS['RESET']}")
    print(f"{COLORS['G']}Guanine (G) flashes Yellow{COLORS['RESET']}")
    print("-----------------------------\n")
    
    template = generate_template(20) # Locked to 20 cycles
    called_sequence = ""
    
    # Cluster states (Start at 100% in sync)
    sync = 1.0
    phased = 0.0     
    pre_phased = 0.0 
    
    print_slow("Role: FLUIDICS CONTROLLER & BASE CALLER")
    print_slow("Goal: Sequence the 20-base template. Watch out for degrading signals!")
    print("="*40 + "\n")
    
    for i in range(len(template)):
        print(f"--- CYCLE {i+1}/20 ---")
        
        # 1. INCORPORATION 
        input("Press [ENTER] to flow nucleotides and trigger laser excitation...")
        
        # Calculate expected bases for the cluster
        current_base = COMPLEMENTS[template[i]]
        prev_base = COMPLEMENTS[template[i-1]] if i > 0 else None
        next_base = COMPLEMENTS[template[i+1]] if i < len(template)-1 else None
        
        # Aggregate signal colors based on cluster state
        signals = {'A': 0.0, 'T': 0.0, 'C': 0.0, 'G': 0.0}
        signals[current_base] += sync
        if prev_base:
            signals[prev_base] += phased
        if next_base:
            signals[next_base] += pre_phased
            
        # 2. LASER EXCITATION 
        print("Optical Sensor Output:")
        for base, intensity in signals.items():
            if intensity > 0.01: # Only show signals > 1%
                bar = "█" * int(intensity * 20)
                print(f"  {COLORS[base]}[{COLOR_NAMES[base]:<6}] {intensity*100:05.2f}% {bar}{COLORS['RESET']}")
        
        # 3. BASE CALLING
        call = input("\nBased on the dominant signal, call the base (A, T, C, G): ").upper()
        called_sequence += call
        
        if call != current_base:
            print(f"\033[91mWARNING: Incorrect base call! Expected {current_base}.\033[0m")
        else:
            print("Base call accepted.")

        # 4. CLEAVAGE 
        cleave_action = input("Type 'cleave' to remove terminators and fluorophores: ").strip().lower()
        
        if cleave_action != 'cleave':
            print("\033[91mCRITICAL ERROR: Cleavage skipped! Heavy phasing introduced.\033[0m")
            penalty = sync * 0.20
            sync -= penalty
            phased += penalty
        else:
            print("Cleavage successful.")
            natural_phasing = sync * 0.02
            natural_pre_phasing = sync * 0.02
            
            sync -= (natural_phasing + natural_pre_phasing)
            phased += natural_phasing
            pre_phased += natural_pre_phasing
            
        print("\n" + "="*40 + "\n")
        time.sleep(0.5)

        # EDUCATIONAL POP-UPS
        if (i + 1) == 5:
            print_lesson("The Reversible Terminator", 
                         "Why do we only sequence one base at a time? Illumina nucleotides have a chemical block on the 3' OH group called a 'reversible terminator'. This prevents the polymerase from adding multiple bases in a single cycle. The 'cleave' step you keep typing removes this block so the next cycle can begin!")
        elif (i + 1) == 10:
            print_lesson("Phasing and Pre-Phasing", 
                         "Notice the colors starting to mix? This is background noise. 'Phasing' happens when the cleavage step fails, leaving some molecules a step behind. 'Pre-phasing' happens when a nucleotide lacks a terminator, allowing molecules to jump a step ahead. Over many cycles, this ruins the signal.")
        elif (i + 1) == 15:
            print_lesson("Clusters and Signal-to-Noise Ratio", 
                         "Remember, you aren't looking at one DNA strand. The optical sensor is reading a 'cluster' of ~1,000 identical clonal strands. As phasing builds up, the true signal gets drowned out by the noise of the out-of-sync molecules. This is why read lengths have physical limits!")
        elif (i + 1) == 20:
            print_lesson("Phred Q-Scores", 
                         "How does the sequencer grade your data? It uses Phred Quality Scores (Q-scores). The software looks at the purity of the color signal to calculate the probability of an error. A Q30 score means there is a 1 in 1,000 chance of an incorrect base call (99.9% accuracy). High noise means low Q-scores!")

    print_slow("=== SEQUENCING RUN COMPLETE ===")
    true_complement = ''.join([COMPLEMENTS[b] for b in template])
    print(f"True Target Sequence: 5'-{true_complement}-3'")
    print(f"Your Called Sequence: 5'-{called_sequence}-3'")
    
    matches = sum(1 for x, y in zip(true_complement, called_sequence) if x == y)
    accuracy = (matches / len(template)) * 100
    print(f"\nBase Calling Accuracy: {accuracy:.1f}%")
    
    if accuracy == 100:
        print("Excellent work! You successfully navigated the cluster noise.")
    else:
        print("Signal noise caused base calling errors. In real life, this lowers your Q-scores!")

if __name__ == "__main__":
    try:
        play_advanced_sbs()
    except KeyboardInterrupt:
        print("\nRun aborted.")
