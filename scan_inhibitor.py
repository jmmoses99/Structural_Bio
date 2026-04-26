from pymol import cmd

def scan_for_inhibitor():
    best_state = 1
    max_contacts = 0
    ligand = "glp_poses"
    protein = "rec"
    
    # Check how many poses are actually in the object
    num_states = cmd.count_states(ligand)
    print(f"\n--- SCANNING {num_states} POSES ---")
    
    for i in range(1, num_states + 1):
        # Select ligand atoms in pose 'i' within 3.5A of protein 'rec' (state 1)
        # Using a temporary selection avoids GUI lag
        count = cmd.select("temp_idx", f"({ligand} and state {i}) within 3.5 of ({protein} and state 1)")
        
        if count > max_contacts:
            max_contacts = count
            best_state = i
            
    if max_contacts > 0:
        print(f"Best State Found: {best_state}")
        print(f"Contact Atoms: {max_contacts}")
        
        # Lock in the winner
        cmd.set("state", best_state)
        cmd.create("winner_pose", ligand, best_state, 1)
        cmd.color("orange", "winner_pose")
        cmd.zoom("winner_pose", 10)
        
        # Compare to crystal ligand if it exists
        if "xtal-lig" in cmd.get_names():
            cmd.dist("overlap", "winner_pose", "xtal-lig", mode=2)
            print("Visualizing overlap with crystal ligand...")
            
        print("SUCCESS: Best pose isolated as 'winner_pose'.")
    else:
        print("FAILED: No contacts found. The poses might be in a different coordinate space.")

# Execute
scan_for_inhibitor()

