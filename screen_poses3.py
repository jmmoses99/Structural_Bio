from pymol import cmd

# Configuration
SESSION = "Docking.pse"
LIGAND = "glp_poses"
PROTEIN = "rec"
CUTOFF = 3.6
MIN_CONTACTS = 15  # Updated for a stricter, higher-quality filter

def run_screen():
    # Load the session
    cmd.load(SESSION)
    num_states = cmd.count_states(LIGAND)
    
    # List to store candidates that pass the 15-contact threshold
    all_scores = []

    print(f"--- Scanning {num_states} poses ---")
    print(f"--- Minimum Contact Threshold: {MIN_CONTACTS} ---")

    for i in range(1, num_states + 1):
        # Select atoms in ligand state 'i' within 3.6A of protein
        count = cmd.select("temp", f"({LIGAND} and state {i}) within {CUTOFF} of ({PROTEIN} and state 1)")
        
        # Only keep if it meets the stricter criteria
        if count >= MIN_CONTACTS:
            all_scores.append((count, i))

    # Sort descending by contact count
    all_scores.sort(key=lambda x: x[0], reverse=True)
    
    # Grab top 5 from the qualified list
    top_5_raw = all_scores[:5]

    top_inhibitors_list = []
    
    if not top_5_raw:
        print(f"\nWARNING: No poses found with at least {MIN_CONTACTS} contacts.")
        return []

    print("\n--- TOP 5 INHIBITORS (STRICT FILTER) ---")
    print(f"{'Rank':<6} | {'State':<10} | {'Contacts':<10}")
    print("-" * 32)

    for rank, (contacts, state) in enumerate(top_5_raw, 1):
        entry = {"rank": rank, "state": state, "contacts": contacts}
        top_inhibitors_list.append(entry)
        
        print(f"{entry['rank']:<6} | {entry['state']:<10} | {entry['contacts']:<10}")
        
        # Save each to a unique PDB
        cmd.save(f"top_{rank}_state_{state}.pdb", f"{LIGAND} and state {state}")

    print(f"\nACTION: Saved {len(top_inhibitors_list)} files.")
    return top_inhibitors_list

# Execute the script
top_5 = run_screen()

