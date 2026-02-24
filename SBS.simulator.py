import time
import random
import sys

# ANSI color codes for Terminal
COLORS = {
    'A': '\033[91m',       # Red
    'T': '\033[92m',       # Green
    'C': '\033[94m',       # Blue
    'G': '\033[93m',       # Yellow
    'RED': '\033[91m',
    'GREEN': '\033[92m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'MAGENTA': '\033[95m',
    'CYAN': '\033[96m',
    'INFO': '\033[96m',
    'RESET': '\033[0m'
}
COMPLEMENTS = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
COLOR_NAMES_4CH = {'A': 'Red', 'T': 'Green', 'C': 'Blue', 'G': 'Yellow'}

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
    print(f"\n{COLORS['INFO']}" + "★"*55)
    print(f"  LESSON UNLOCKED: {title}")
    print("★"*55)
    words = text.split(' ')
    line = "  "
    for word in words:
        if len(line) + len(word) > 51:
            print(line)
            line = "  " + word + " "
        else:
            line += word + " "
    print(line)
    print("★"*55 + f"{COLORS['RESET']}\n")
    input("Press [ENTER] to continue the sequencing run...")
    print("\n")

def print_crash_course():
    """Prints the shared educational crash course."""
    print(f"\n{COLORS['INFO']}=== HOW SBS WORKS ==={COLORS['RESET']}")
    print(f"{COLORS['CYAN']}• Sequencing by Synthesis (SBS):{COLORS['RESET']} A polymerase builds a complementary DNA strand one base at a time.")
    print(f"{COLORS['MAGENTA']}• Reversible Terminators:{COLORS['RESET']} Every nucleotide has a fluorescent dye AND a chemical block.")
    print(f"{COLORS['YELLOW']}• The Block:{COLORS['RESET']} This ensures the polymerase can only add EXACTLY ONE base per cycle.")
    print(f"{COLORS['GREEN']}• The Flash:{COLORS['RESET']} Lasers excite the dye, and cameras snap a picture to identify the base.\n")
    
    print(f"{COLORS['INFO']}=== CRITICAL BIOCHEMISTRY ==={COLORS['RESET']}")
    print(f"{COLORS['CYAN']}• Cleavage:{COLORS['RESET']} A chemical wash that snips off the dye and the terminator block, exposing the 3' OH group so the next base can attach.")
    print(f"{COLORS['RED']}• Phasing:{COLORS['RESET']} The enemy of sequencing! If cleavage fails on a molecule, it falls one cycle behind the rest of the cluster.")
    print(f"{COLORS['MAGENTA']}• Pre-Phasing:{COLORS['RESET']} If a nucleotide was missing its block, a molecule jumps one cycle ahead.")
    print(f"{COLORS['YELLOW']}• The Result:{COLORS['RESET']} Out-of-sync molecules create background noise, eventually destroying the Q-score!\n")
    print(f"{COLORS['INFO']}============================={COLORS['RESET']}\n")
    input("Press [ENTER] to review the optics key...")

def play_four_channel_sbs():
    print_slow("\n=== 4-CHANNEL SBS SIMULATOR (STANDARD CHEMISTRY) ===")
    print_slow("Initializing Flow Cell Cluster (1,000 molecules)...\n")
    time.sleep(0.5)

    print_crash_course()

    # Color Key Explanation
    print("\n--- 4-CHANNEL OPTICS KEY ---")
    print(f"{COLORS['A']}Adenine (A) flashes Red{COLORS['RESET']}")
    print(f"{COLORS['T']}Thymine (T) flashes Green{COLORS['RESET']}")
    print(f"{COLORS['C']}Cytosine (C) flashes Blue{COLORS['RESET']}")
    print(f"{COLORS['G']}Guanine (G) flashes Yellow{COLORS['RESET']}")
    print("----------------------------\n")
    
    template = generate_template(20) 
    called_sequence = ""
    sync = 1.0
    phased = 0.0     
    pre_phased = 0.0 
    
    print_slow("Role: FLUIDICS CONTROLLER & BASE CALLER")
    print_slow("Goal: Sequence the 20-base template. Watch out for degrading signals!")
    print("="*40 + "\n")
    
    for i in range(len(template)):
        print(f"--- CYCLE {i+1}/20 ---")
        input("Press [ENTER] to flow nucleotides and trigger laser excitation...")
        
        current_base = COMPLEMENTS[template[i]]
        prev_base = COMPLEMENTS[template[i-1]] if i > 0 else None
        next_base = COMPLEMENTS[template[i+1]] if i < len(template)-1 else None
        
        signals = {'A': 0.0, 'T': 0.0, 'C': 0.0, 'G': 0.0}
        signals[current_base] += sync
        if prev_base: signals[prev_base] += phased
        if next_base: signals[next_base] += pre_phased
            
        print("Optical Sensor Output:")
        for base, intensity in signals.items():
            if intensity > 0.01:
                bar = "█" * int(intensity * 20)
                print(f"  {COLORS[base]}[{COLOR_NAMES_4CH[base]:<6}] {intensity*100:05.2f}% {bar}{COLORS['RESET']}")
        
        call = input("\nBased on the dominant signal, call the base (A, T, C, G): ").upper()
        called_sequence += call
        
        if call != current_base:
            print(f"{COLORS['RED']}WARNING: Incorrect base call! Expected {current_base}.{COLORS['RESET']}")
        else:
            print("Base call accepted.")

        cleave_action = input("Type 'cleave' to chemical wash terminators and fluorophores: ").strip().lower()
        
        if cleave_action != 'cleave':
            print(f"{COLORS['RED']}CRITICAL ERROR: Cleavage skipped! Heavy phasing introduced.{COLORS['RESET']}")
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

        if (i + 1) == 5:
            print_lesson("The Reversible Terminator", "Why do we only sequence one base at a time? Illumina nucleotides have a chemical block on the 3' OH group called a 'reversible terminator'. This prevents the polymerase from adding multiple bases in a single cycle. The 'cleave' step removes this block so the next cycle can begin!")
        elif (i + 1) == 10:
            print_lesson("Phasing and Pre-Phasing", "Notice the colors starting to mix? This is background noise. 'Phasing' happens when the cleavage step fails, leaving some molecules a step behind. 'Pre-phasing' happens when a nucleotide lacks a terminator, allowing molecules to jump a step ahead.")
        elif (i + 1) == 15:
            print_lesson("Clusters and Signal-to-Noise Ratio", "Remember, you aren't looking at one DNA strand. The optical sensor is reading a 'cluster' of ~1,000 identical clonal strands. As phasing builds up, the true signal gets drowned out by the noise of the out-of-sync molecules. This limits read length!")
        elif (i + 1) == 20:
            print_lesson("Phred Q-Scores", "How does the sequencer grade your data? It uses Phred Quality Scores (Q-scores). The software looks at the purity of the color signal to calculate the probability of an error. A Q30 score means a 1 in 1,000 chance of an incorrect base call. High noise means low Q-scores!")

    end_game(template, called_sequence)


def play_two_channel_sbs():
    print_slow("\n=== 2-CHANNEL SBS SIMULATOR (XLEAP CHEMISTRY) ===")
    print_slow("Initializing Flow Cell Cluster (1,000 molecules)...\n")
    time.sleep(0.5)

    print_crash_course()

    # Color Key Explanation
    print("\n--- 2-CHANNEL OPTICS KEY ---")
    print(f"{COLORS['BLUE']}Cytosine (C) = Blue Image Only{COLORS['RESET']}")
    print(f"{COLORS['GREEN']}Thymine (T)  = Green Image Only{COLORS['RESET']}")
    print(f"Adenine (A)  = {COLORS['BLUE']}Blue{COLORS['RESET']} & {COLORS['GREEN']}Green{COLORS['RESET']} Images")
    print("Guanine (G)  = Dark (No Image/Signal)")
    print("----------------------------\n")
    
    template = generate_template(20)
    called_sequence = ""
    sync = 1.0
    phased = 0.0     
    pre_phased = 0.0 
    
    print_slow("Role: FLUIDICS CONTROLLER & BASE CALLER")
    print_slow("Goal: Sequence the 20-base template using only 2 images.")
    print("="*40 + "\n")
    
    for i in range(len(template)):
        print(f"--- CYCLE {i+1}/20 ---")
        input("Press [ENTER] to flow nucleotides and snap the 2 pictures...")
        
        current_base = COMPLEMENTS[template[i]]
        prev_base = COMPLEMENTS[template[i-1]] if i > 0 else None
        next_base = COMPLEMENTS[template[i+1]] if i < len(template)-1 else None
        
        blue_signal = 0.0
        green_signal = 0.0
        
        def add_signal(base, intensity):
            nonlocal blue_signal, green_signal
            if base == 'C': blue_signal += intensity
            elif base == 'T': green_signal += intensity
            elif base == 'A':
                blue_signal += intensity
                green_signal += intensity
            
        add_signal(current_base, sync)
        if prev_base: add_signal(prev_base, phased)
        if next_base: add_signal(next_base, pre_phased)
            
        print("Optical Sensor Output (2 Images Taken):")
        b_bar = "█" * int(blue_signal * 20)
        g_bar = "█" * int(green_signal * 20)
        
        if blue_signal < 0.01: b_bar = ""
        if green_signal < 0.01: g_bar = ""
            
        print(f"  {COLORS['BLUE']}[Blue Image ] {blue_signal*100:05.2f}% {b_bar}{COLORS['RESET']}")
        print(f"  {COLORS['GREEN']}[Green Image] {green_signal*100:05.2f}% {g_bar}{COLORS['RESET']}")
        
        call = input("\nBased on the two images, call the base (A, T, C, G): ").upper()
        called_sequence += call
        
        if call != current_base:
            print(f"{COLORS['RED']}WARNING: Incorrect base call! Expected {current_base}.{COLORS['RESET']}")
        else:
            print("Base call accepted.")

        cleave_action = input("Type 'cleave' to chemical wash terminators and fluorophores: ").strip().lower()
        
        if cleave_action != 'cleave':
            print(f"{COLORS['RED']}CRITICAL ERROR: Cleavage skipped! Heavy phasing introduced.{COLORS['RESET']}")
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

        if (i + 1) == 5:
            print_lesson("Two-Channel Chemistry", "Newer models use only 2 images (Blue and Green) instead of 4 colors. C is Blue, T is Green, A is a mix of both, and G has no dye. Taking half the pictures cuts sequencing time and data footprint in half!")
        elif (i + 1) == 10:
            print_lesson("The 'Dark G' Problem", "Because G is 'dark' (no signal), the sequencer can't easily tell the difference between a real G and a broken cluster that stopped emitting light. If a sample has too many Gs in a row (poly-G), the run quality drops.")
        elif (i + 1) == 15:
            print_lesson("Index Color Balancing", "During multiplexing, you must carefully design your index barcodes. If every sample in your pool has a 'G' at the first index position, the camera sees total darkness and the software gets lost. You must balance the colors!")
        elif (i + 1) == 20:
            print_lesson("Phasing in Two Colors", "Look at how the blue and green signals mixed up over time. If phasing causes a 'ghost' Blue signal and a 'ghost' Green signal to overlap on a Dark G cycle, the software might incorrectly call it an 'A'. Noise is trickier in 2-color chemistry!")

    end_game(template, called_sequence)

def end_game(template, called_sequence):
    """Calculates accuracy and prints the final output."""
    print_slow("=== SEQUENCING RUN COMPLETE ===")
    true_complement = ''.join([COMPLEMENTS[b] for b in template])
    print(f"True Target Sequence: 5'-{true_complement}-3'")
    print(f"Your Called Sequence: 5'-{called_sequence}-3'")
    
    matches = sum(1 for x, y in zip(true_complement, called_sequence) if x == y)
    accuracy = (matches / len(template)) * 100
    print(f"\nBase Calling Accuracy: {accuracy:.1f}%")
    
    if accuracy == 100:
        print(f"{COLORS['GREEN']}Excellent work! You successfully navigated the cluster noise.{COLORS['RESET']}")
    else:
        print(f"{COLORS['YELLOW']}Signal noise caused base calling errors. Check your cleavage steps!{COLORS['RESET']}")
    print("\n")


def main_menu():
    while True:
        print(f"{COLORS['INFO']}========================================={COLORS['RESET']}")
        print(f"{COLORS['INFO']}   ILLUMINA SBS SEQUENCING SIMULATOR     {COLORS['RESET']}")
        print(f"{COLORS['INFO']}========================================={COLORS['RESET']}")
        print("Select your sequencer chemistry to begin:\n")
        print("  1. 4-Channel Chemistry (e.g., MiSeq)")
        print("  2. 2-Channel XLEAP Chemistry (e.g., NextSeq 1000/2000)")
        print("  3. Exit Simulator\n")
        
        choice = input("Enter 1, 2, or 3: ").strip()
        
        if choice == '1':
            play_four_channel_sbs()
            input("Press [ENTER] to return to the Main Menu...")
        elif choice == '2':
            play_two_channel_sbs()
            input("Press [ENTER] to return to the Main Menu...")
        elif choice == '3':
            print_slow("Shutting down flow cell... Goodbye!")
            sys.exit()
        else:
            print(f"{COLORS['RED']}Invalid selection. Please try again.{COLORS['RESET']}\n")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nRun aborted by user. Shutting down...")
        sys.exit()

