import time
import random
import sys

# ANSI color codes for Terminal
COLORS = {
    'BLUE': '\033[94m',
    'GREEN': '\033[92m',
    'INFO': '\033[96m',
    'RESET': '\033[0m'
}
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

def play_two_channel_sbs():
    print_slow("=== 2-CHANNEL SBS SIMULATOR ===")
    print_slow("Initializing Flow Cell Cluster (1,000 molecules)...")
    
    # Color Key Explanation
    print("\n--- 2-CHANNEL OPTICS KEY ---")
    print(f"{COLORS['BLUE']}Cytosine (C) = Blue Image Only{COLORS['RESET']}")
    print(f"{COLORS['GREEN']}Thymine (T)  = Green Image Only{COLORS['RESET']}")
    print(f"Adenine (A)  = {COLORS['BLUE']}Blue{COLORS['RESET']} & {COLORS['GREEN']}Green{COLORS['RESET']} Images")
    print("Guanine (G)  = Dark (No Image/Signal)")
    print("----------------------------\n")
    
    template = generate_template(20)
    called_sequence = ""
    
    # Cluster states
    sync = 1.0
    phased = 0.0     
    pre_phased = 0.0 
    
    print_slow("Role: FLUIDICS CONTROLLER & BASE CALLER")
    print_slow("Goal: Sequence the 20-base template using only 2 images.")
    print("="*40 + "\n")
    
    for i in range(len(template)):
        print(f"--- CYCLE {i+1}/20 ---")
        
        # 1. INCORPORATION 
        input("Press [ENTER] to flow nucleotides and snap the 2 pictures...")
        
        current_base = COMPLEMENTS[template[i]]
        prev_base = COMPLEMENTS[template[i-1]] if i > 0 else None
        next_base = COMPLEMENTS[template[i+1]] if i < len(template)-1 else None
        
        blue_signal = 0.0
        green_signal = 0.0
        
        def add_signal(base, intensity):
            nonlocal blue_signal, green_signal
            if base == 'C':
                blue_signal += intensity
            elif base == 'T':
                green_signal += intensity
            elif base == 'A':
                blue_signal += intensity
                green_signal += intensity
            # G adds nothing (Dark)
            
        add_signal(current_base, sync)
        if prev_base: add_signal(prev_base, phased)
        if next_base: add_signal(next_base, pre_phased)
            
        # 2. LASER EXCITATION (Show the two images)
        print("Optical Sensor Output (2 Images Taken):")
        b_bar = "█" * int(blue_signal * 20)
        g_bar = "█" * int(green_signal * 20)
        
        # Only show > 1% to avoid terminal clutter
        if blue_signal < 0.01: b_bar = ""
        if green_signal < 0.01: g_bar = ""
            
        print(f"  {COLORS['BLUE']}[Blue Image ] {blue_signal*100:05.2f}% {b_bar}{COLORS['RESET']}")
        print(f"  {COLORS['GREEN']}[Green Image] {green_signal*100:05.2f}% {g_bar}{COLORS['RESET']}")
        
        # 3. BASE CALLING
        call = input("\nBased on the two images, call the base (A, T, C, G): ").upper()
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
            print_lesson("Two-Channel Chemistry", 
                         "Newer models use only 2 images (Blue and Green) instead of 4 colors. C is Blue, T is Green, A is a mix of both, and G has no dye. Taking half the pictures cuts sequencing time and data footprint in half!")
        elif (i + 1) == 10:
            print_lesson("The 'Dark G' Problem", 
                         "Because G is 'dark' (no signal), the sequencer can't easily tell the difference between a real G and a broken cluster that stopped emitting light. If a sample has too many Gs in a row (poly-G), the run quality drops.")
        elif (i + 1) == 15:
            print_lesson("Index Color Balancing", 
                         "During multiplexing, you must carefully design your index barcodes. If every sample in your pool has a 'G' at the first index position, the camera sees total darkness and the software gets lost. You must balance the colors!")
        elif (i + 1) == 20:
            print_lesson("Phasing in Two Colors", 
                         "Look at how the blue and green signals mixed up over time. If phasing causes a 'ghost' Blue signal and a 'ghost' Green signal to overlap on a Dark G cycle, the software might incorrectly call it an 'A'. Noise is trickier in 2-color chemistry!")

    print_slow("=== SEQUENCING RUN COMPLETE ===")
    true_complement = ''.join([COMPLEMENTS[b] for b in template])
    print(f"True Target Sequence: 5'-{true_complement}-3'")
    print(f"Your Called Sequence: 5'-{called_sequence}-3'")
    
    matches = sum(1 for x, y in zip(true_complement, called_sequence) if x == y)
    accuracy = (matches / len(template)) * 100
    print(f"\nBase Calling Accuracy: {accuracy:.1f}%")
    
    if accuracy == 100:
        print("Excellent work! You successfully navigated the 2-color cluster noise.")
    else:
        print("Signal noise caused base calling errors. Check your cleavage steps!")

if __name__ == "__main__":
    try:
        play_two_channel_sbs()
    except KeyboardInterrupt:
        print("\nRun aborted.")
