import random
import time

def run_sim():
    print("\n" + "="*50)
    print("LEVEL 1: CLUSTER DENSITY OPTIMIZATION")
    print("="*50)
    print("Goal: Load the flowcell at the perfect concentration (pM).")
    print("Too low = Wasted space. Too high = Overclustering (overlapping signals).")
    
    try:
        conc = int(input("\nEnter loading concentration (Suggested range 100-500 pM): "))
    except ValueError:
        print("Invalid input. Using default 200 pM.")
        conc = 200

    print("\nInitializing Flowcell...")
    time.sleep(1)
    
    # Grid 10x10
    grid = []
    total_clusters = 0
    collisions = 0
    usable_reads = 0

    # Probability of a cluster landing in a spot
    prob = conc / 1000.0

    for r in range(10):
        row = []
        for c in range(10):
            if random.random() < prob:
                row.append("●")
                total_clusters += 1
            else:
                row.append(" ")
        grid.append(row)

    # Visualization
    print("\nFlowcell Surface (10x10 sample area):")
    print("+" + "---+" * 10)
    for row in grid:
        print("| " + " | ".join(row) + " |")
        print("+" + "---+" * 10)

    # Calculate Collisions (simplified: if neighbors exist)
    for r in range(10):
        for c in range(10):
            if grid[r][c] == "●":
                # Check neighbors
                is_collision = False
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < 10 and 0 <= nc < 10:
                        if grid[nr][nc] == "●":
                            is_collision = True
                            break
                if is_collision:
                    collisions += 1
                else:
                    usable_reads += 1

    pf_rate = (usable_reads / total_clusters * 100) if total_clusters > 0 else 0
    
    print(f"\n--- RUN STATISTICS ---")
    print(f"Total Clusters Seeded: {total_clusters}")
    print(f"Collisions Detected:   {collisions}")
    print(f"Pass Filter (PF) Reads: {usable_reads}")
    print(f"PF Rate:               {pf_rate:.1f}%")

    if pf_rate > 85 and usable_reads > 20:
        print("\nRESULT: PERFECT LOADING! High data yield and clean signals.")
    elif usable_reads < 10:
        print("\nRESULT: UNDERCLUSTERED. You wasted most of the flowcell capacity.")
    elif pf_rate < 50:
        print("\nRESULT: OVERCLUSTERED! Most signals are overlapping and uncallable.")
    else:
        print("\nRESULT: SUB-OPTIMAL. Try adjusting the concentration for better yield.")

if __name__ == "__main__":
    run_sim()
