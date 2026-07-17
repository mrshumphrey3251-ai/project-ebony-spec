# Project Ebony: Standard Mesh Node
# Decentralized, off-grid radio communication for fleet awareness

import local_audit_logger
import json

# Standard Mesh Configurations
STANDARD_FREQ_MHZ = 900.0
STANDARD_PROXIMITY_ALERT_CM = 1500.0  

def initialize_mesh_transceiver():
    try:
        with open('sovereign_config.json', 'r') as config_file:
            config = json.load(config_file)
            
        print(f"POWERING RADIO. Asset [{config['equipment_designation']}] joining Mesh.")
        return True
    except Exception as e:
        print("ERROR: Transceiver failed. Asset isolated.")
        local_audit_logger.secure_log_action("MESH_INIT", "FAILED")
        return False

def broadcast_asset_heartbeat(current_status="ACTIVE"):
    packet = f"[HEARTBEAT] STATUS: {current_status} | SECURE_TX"
    print(f"MESH TX: Transmitting heartbeat -> {packet}")

def scan_fleet_proximity(incoming_radio_distance_cm):
    if incoming_radio_distance_cm <= STANDARD_PROXIMITY_ALERT_CM:
        print(f"WARNING: Asset detected at {incoming_radio_distance_cm}cm via Mesh.")
        local_audit_logger.secure_log_action("MESH_SCAN", f"ALERT - {incoming_radio_distance_cm}cm")
        return True 
    return False

if __name__ == "__main__":
    if initialize_mesh_transceiver():
        broadcast_asset_heartbeat()
        scan_fleet_proximity(1000.0)
