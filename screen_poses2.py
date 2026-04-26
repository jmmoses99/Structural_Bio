from pymol import cmd

# Configuration
SESSION = "Docking.pse"
LIGAND = "glp_poses"
PROTEIN = "rec"
CUTOFF = 3.6

def run_screen():
    # Load the session
    cmd.load(SESSION)
    
    best_state = 0
    max_contacts = 0
    num_states = cmd.count_states(LIGAND)
    
    print(f"--- Scanning {num_states} poses against {PROTEIN} ---")

    for i in range(1, num_states + 1):
        # Select atoms in ligand state 'i' within 3.6A of protein state 1
        count = cmd.select("temp", f"({LIGAND} and state {i}) within {CUTOFF} of ({PROTEIN} and state 1)")
        
        if count > max_contacts:
            max_contacts = count
            best_state = i
            
        if i % 200 == 0:
            print(f"  Progress: {i}/{num_states}...")

    if max_contacts > 0:
        print("\n--- RESULTS ---")
        print(f"BEST POSE: State {best_state}")
        print(f"CONTACT ATOMS: {max_contacts}")
        print(f"VERDICT: Strongest binder identified.")
        
        # Save the winner as a separate PDB for later
        cmd.set("state", best_state)
        cmd.save("best_inhibitor_pose.pdb", f"{LIGAND} and state {best_state}")
        print(f"ACTION: Saved best pose to 'best_inhibitor_pose.pdb'")
    else:
        print("\nFAILED: No contacts found. Check object names or increase cutoff.")

# Execute
run_screen()

