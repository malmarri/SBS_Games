import random
import time
import sys

def run_sim():
    print("\n" + "="*65)
    print("LEVEL 1: CLUSTER DENSITY OPTIMIZATION (Recalibrated)")
    print("="*65)
    print("Goal: Load the flowcell at the perfect concentration (pM).")
    print("Goal Range: 650 - 1000 pM")
    print("-" * 65)
    print("TRADEOFF:")
    print("- Too low  (< 650)  = Clean signals but very few reads (Underclustered).")
    print("- Too high (> 1000) = Signals overlap, optics can't distinguish (Overclustered).")
    
    try:
        val = input("\nEnter loading concentration (Suggested range 100-1500 pM): ")
        conc = int(val)
    except ValueError:
        print("Invalid input. Using default 800 pM.")
        conc = 800

    print("\nInitializing Flowcell Surface...")
    time.sleep(0.5)
    print("Seeding DNA clusters...")
    time.sleep(0.5)
    
    # Grid 20x20 (400 possible spots)
    size = 20
    grid = []
    total_clusters = 0
    usable_reads = 0

    # Probability scaling adjusted so 1000 pM starts hitting the limit
    # 1000 pM = 12.5% occupancy in this model
    prob = min(conc / 8000.0, 1.0)

    for r in range(size):
        row = []
        for c in range(size):
            if random.random() < prob:
                row.append("●")
                total_clusters += 1
            else:
                row.append(" ")
        grid.append(row)

    # Visualization (Sample 10x10 area to avoid cluttering terminal)
    print("\nFlowcell Optics (Representing a 10x10 tile subset):")
    print("+" + "---+" * 10)
    for r in range(10):
        print("| " + " | ".join(grid[r][:10]) + " |")
        print("+" + "---+" * 10)

    # PF Filter Logic (Illumina Pass Filter)
    # A cluster passes PF if it is "monoclonal" - in our grid, it fails if 
    # it has 2 or more neighbors (allowing 1 neighbor simulates signal robustness)
    for r in range(size):
        for c in range(size):
            if grid[r][c] == "●":
                neighbors = 0
                # Check 8 neighbors (Moore neighborhood)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < size and 0 <= nc < size:
                            if grid[nr][nc] == "●":
                                neighbors += 1
                
                # PF Pass if it has 1 or 0 neighbors (simulating modern cluster isolation)
                if neighbors <= 1:
                    usable_reads += 1

    pf_rate = (usable_reads / total_clusters * 100) if total_clusters > 0 else 0
    
    print(f"\n--- OPTICAL ANALYSIS ---")
    print(f"Total Clusters Seeded: {total_clusters}")
    print(f"Pass Filter (PF) Reads: {usable_reads} (Clean, unique signals)")
    print(f"PF Rate:               {pf_rate:.1f}%")

    print("\n--- FINAL REPORT ---")
    if total_clusters == 0:
        print("RESULT: FLOWCELL EMPTY. Did you forget to add DNA?")
    
    elif 650 <= conc <= 1000:
        if pf_rate > 70:
            print(f"RESULT: PERFECT LOADING ({conc} pM)!")
            print("Excellent balance between high data yield and signal purity.")
        else:
            print(f"RESULT: BORDERLINE. Yield was high but signal noise is increasing.")
            
    elif conc < 650:
        print(f"RESULT: UNDERCLUSTERED ({conc} pM).")
        print("The lane is very clean, but you're only using a fraction of the sequencer's power.")
        print("Action: Increase concentration to the 650-1000 pM range.")
        
    else: # conc > 1000
        print(f"RESULT: OVERCLUSTERED ({conc} pM)!")
        print("Too many clusters! Signals are bleeding together.")
        print("Action: Decrease concentration. Reagents were wasted on uncallable data.")

if __name__ == "__main__":
    run_sim()
