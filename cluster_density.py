import random
import time
import sys

def run_sim():
    print("\n" + "="*60)
    print("LEVEL 1: CLUSTER DENSITY OPTIMIZATION")
    print("="*60)
    print("Goal: Load the flowcell at the perfect concentration (pM).")
    print("Goal Statistics: Aim for ~80% PF Rate and >100 Usable Reads.")
    print("-" * 60)
    print("TRADEOFF:")
    print("- Too low  = Clean signals but very few reads (Underclustered).")
    print("- Too high = Signals overlap, optics can't distinguish them (Overclustered).")
    
    try:
        val = input("\nEnter loading concentration (Suggested range 100-1000 pM): ")
        conc = int(val)
    except ValueError:
        print("Invalid input. Using default 400 pM.")
        conc = 400

    print("\nInitializing Flowcell Surface...")
    time.sleep(0.5)
    print("Seeding DNA clusters...")
    time.sleep(0.5)
    
    # Grid 20x20
    size = 20
    grid = []
    total_clusters = 0
    usable_reads = 0

    # Probability of a cluster landing in a spot
    # 1000 pM = 50% occupancy in this model
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

    # Visualization (Sample 10x10 area to avoid cluttering terminal)
    print("\nFlowcell Optics (Representing a 10x10 tile subset):")
    print("+" + "---+" * 10)
    for r in range(10):
        print("| " + " | ".join(grid[r][:10]) + " |")
        print("+" + "---+" * 10)

    # PF Filter Logic (Illumina Pass Filter)
    # A cluster passes PF if it is "monoclonal" - in our grid, it fails if 
    # it has ANY neighbor (including diagonals) that interferes with its signal.
    for r in range(size):
        for c in range(size):
            if grid[r][c] == "●":
                is_collision = False
                # Check 8 neighbors (Moore neighborhood)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0: continue
                        nr, nc = r+dr, c+dc
                        if 0 <= nr < size and 0 <= nc < size:
                            if grid[nr][nc] == "●":
                                is_collision = True
                                break
                    if is_collision: break
                
                if not is_collision:
                    usable_reads += 1

    pf_rate = (usable_reads / total_clusters * 100) if total_clusters > 0 else 0
    
    print(f"\n--- OPTICAL ANALYSIS ---")
    print(f"Total Clusters Seeded: {total_clusters}")
    print(f"Pass Filter (PF) Reads: {usable_reads} (Clean, unique signals)")
    print(f"PF Rate:               {pf_rate:.1f}%")

    print("\n--- FINAL REPORT ---")
    if total_clusters == 0:
        print("RESULT: FLOWCELL EMPTY. Did you forget to add DNA?")
    elif pf_rate > 70 and usable_reads > 80:
        print("RESULT: PERFECT LOADING! High data yield and clean signals.")
        print("You've mastered the first step of the Sequencing Run.")
    elif usable_reads < 30 and pf_rate > 80:
        print("RESULT: UNDERCLUSTERED. The run was clean, but you wasted 80% of the lane's capacity.")
        print("Action: Increase concentration for the next run.")
    elif pf_rate < 40:
        print("RESULT: OVERCLUSTERED! Most signals overlapped and were rejected by the image analysis.")
        print("Action: Decrease concentration. This run is a massive waste of reagents.")
    else:
        print("RESULT: SUB-OPTIMAL. You have some data, but the signal-to-noise ratio is poor.")
        print("Try to find the 'Goldilocks' zone between yield and purity.")

if __name__ == "__main__":
    run_sim()
