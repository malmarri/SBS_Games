import random
import time
import sys

def run_sim():
    print("\n" + "="*65)
    print("LEVEL 1: CLUSTER DENSITY OPTIMIZATION")
    print("="*65)
    print("Goal: Load the flowcell at the perfect concentration (pM).")
    print("Perfect Range: 650 - 1000 pM")
    print("-" * 65)
    print("TRADEOFF:")
    print("- Too low  (< 650)  = Clean signals but very low data yield.")
    print("- Too high (> 1000) = Overclustering: signals overlap and fail PF.")
    
    try:
        val = input("\nEnter loading concentration (Suggested: 100 - 1500 pM): ")
        conc = int(val)
    except ValueError:
        print("Invalid input. Using default 800 pM.")
        conc = 800

    print("\n[SYSTEM] Seeding DNA clusters onto flowcell surface...")
    time.sleep(0.5)
    
    # Simulation Parameters
    # Grid 40x40 = 1600 possible sites
    size = 40
    grid = []
    total_clusters = 0
    usable_reads = 0

    # Occupancy Probability Scaling:
    # We want 1000 pM to be "comfortably crowded" (~50% occupancy)
    # 2000 pM = 1.0 probability (100% occupancy / solid dots)
    prob = min(conc / 2000.0, 1.0)

    for r in range(size):
        row = []
        for c in range(size):
            if random.random() < prob:
                row.append("●")
                total_clusters += 1
            else:
                row.append(" ")
        grid.append(row)

    # Visualization: Show a representative 10x10 slice to the user
    # We pick the center slice for consistency
    print("\n[IMAGE ANALYSIS] Visualizing Tile Slice (10x10 zoom):")
    print("+" + "---+" * 10)
    for r in range(15, 25):
        print("| " + " | ".join(grid[r][15:25]) + " |")
        print("+" + "---+" * 10)

    # Pass Filter (PF) Logic
    # A cluster passes PF if it is uniquely identifiable (not too many neighbors).
    # In this crowded model, we allow up to 2 neighbors (signal deconvolution).
    for r in range(size):
        for c in range(size):
            if grid[r][c] == "●":
                neighbors = 0
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < size and 0 <= nc < size:
                            if grid[nr][nc] == "●":
                                neighbors += 1
                
                # PF Pass if signal is sufficiently isolated
                if neighbors <= 2:
                    usable_reads += 1

    pf_rate = (usable_reads / total_clusters * 100) if total_clusters > 0 else 0
    
    print(f"\n--- RUN METRICS (Full Flowcell) ---")
    print(f"Clusters Seeded:       {total_clusters}")
    print(f"Pass Filter (PF) Reads: {usable_reads}")
    print(f"PF Rate:               {pf_rate:.1f}%")

    print("\n--- SEQUENCER REPORT ---")
    if total_clusters == 0:
        print("RESULT: FLOWCELL EMPTY.")
        
    elif 650 <= conc <= 1000:
        # Success Zone: Yield should be high and PF should be respectable (>40% in this dense model)
        if usable_reads > 350:
            print(f"RESULT: PERFECT LOADING ({conc} pM)!")
            print("Excellent yield. You have maximized the flowcell data capacity.")
        else:
            print(f"RESULT: BORDERLINE. You're in the right pM range, but stochastic seeding was poor.")
            
    elif conc < 650:
        print(f"RESULT: UNDERCLUSTERED ({conc} pM).")
        print("The signals are clean, but you have very few reads. Waste of a sequencing run.")
        
    else: # conc > 1000
        print(f"RESULT: OVERCLUSTERED ({conc} pM)!")
        print("Too many dots! Signals are overlapping so much they cannot be resolved.")
        print("PF rate has crashed, leading to low data quality.")

if __name__ == "__main__":
    run_sim()
