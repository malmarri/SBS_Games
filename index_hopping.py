import random
import time

def run_sim():
    print("\n" + "="*50)
    print("LEVEL 2: INDEX HOPING & DEMULTIPLEXING")
    print("="*50)
    print("Goal: Call the 8bp sample index (barcode).")
    print("Warning: Interference from other samples in the pool may occur.")
    
    samples = {
        "A": "ATGCATGC",
        "B": "CGTAGCTA",
        "C": "GGTTAACC"
    }
    
    target_label = random.choice(["A", "B", "C"])
    target_index = samples[target_label]
    user_calls = ""

    print(f"\nSequencing Index for Cluster Sample...")
    time.sleep(1)

    for cycle in range(8):
        true_base = target_index[cycle]
        
        # Simulate signal
        # Add 'hopping' noise from other barcodes
        noise_bases = [samples[k][cycle] for k in samples if k != target_label]
        
        print(f"\nCycle {cycle+1} Signal Intensities:")
        bases = ['A', 'T', 'C', 'G']
        for b in bases:
            intensity = 0
            if b == true_base:
                intensity += random.uniform(0.6, 0.9)
            if b in noise_bases:
                intensity += random.uniform(0.1, 0.3) # Hopping noise
            
            bar = "█" * int(intensity * 20)
            print(f"{b}: {bar} ({intensity:.2f})")
        
        call = input("Call the base (A,T,C,G): ").upper()
        user_calls += call

    print(f"\nUser Index Call: {user_calls}")
    print(f"True Sample Index: {target_index}")

    if user_calls == target_index:
        print(f"\nSUCCESS: Read assigned to Sample {target_label} correctly.")
    else:
        # Check if it matches another sample
        assigned_to = "UNKNOWN"
        for k, v in samples.items():
            if user_calls == v:
                assigned_to = k
        
        if assigned_to != "UNKNOWN":
            print(f"\nFAILURE: INDEX HOPPING! Read mis-assigned to Sample {assigned_to}.")
        else:
            print(f"\nFAILURE: UNASSIGNED READ. Sequence does not match any valid index.")

if __name__ == "__main__":
    run_sim()
