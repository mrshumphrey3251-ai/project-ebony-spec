# Project Ebony: Standard Mesh Node (Redacted)
# Public blueprint for basic fleet radio initialization and proximity scanning

def initialize_mesh_transceiver():
    print("[Radio] Standard fleet transceiver online.")
    return True

def scan_fleet_proximity(radio_distance_mm):
    # Standard generic testing perimeter
    STANDARD_FLEET_ZONE = 1000.0
    
    if radio_distance_mm <= STANDARD_FLEET_ZONE:
        print("[Radio] Friendly unit proximity warning. Restricting movement.")
        return True
    else:
        return False
