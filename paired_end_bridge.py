import random
import time

def run_sim():
    print("\n" + "="*50)
    print("LEVEL 3: PAIRED-END BRIDGE AMPLIFICATION")
    print("="*50)
    print("You have successfully finished Read 1.")
    print("Now, we must flip the DNA to sequence the other side (Read 2).")
    
    input("\nPress ENTER to start Bridge Amplification turnover...")
    
    print("\n1. Denaturing DNA molecules...")
    time.sleep(1)
    print("2. Molecules bending to find surface primers (Bridge formation)...")
    time.sleep(1)
    print("3. Synthesizing complementary strand...")
    time.sleep(1)
    print("4. Cleaving original Forward strand...")
    time.sleep(1)
    print("5. REVERSE STRAND READY.")

    print("\nStarting Read 2 sequencing...")
    print("Note: Starting noise is higher because the cluster has aged.")
    
    template = "".join(random.choice("ATCG") for _ in range(10))
    sync = 0.8  # Lower starting sync for R2
    phased = 0.1
    pre_phased = 0.1

    for cycle in range(10):
        true_base = template[cycle]
        
        # Calculate muddier signal
        intensities = {b: 0.0 for b in "ATCG"}
        intensities[true_base] += sync
        
        # Add phasing noise from random bases
        for _ in range(2):
            intensities[random.choice("ATCG")] += (phased / 2)
            intensities[random.choice("ATCG")] += (pre_phased / 2)

        print(f"\nRead 2 - Cycle {cycle+1} Intensities:")
        for b, val in intensities.items():
            bar = "█" * int(val * 20)
            print(f"{b}: {bar} ({val:.2f})")
        
        call = input("Call base: ").upper()
        
        # Increase entropy
        sync -= 0.04
        phased += 0.02
        pre_phased += 0.02

    print("\nREAD 2 COMPLETE.")
    print("Notice how the signals became unreadable much faster than Read 1?")

if __name__ == "__main__":
    run_sim()
