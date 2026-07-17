# Standard Terminal Execution Loop (Amended with Hardware Actuation)
# Core loop for continuous localized command execution

import time
import operator_interface
import local_audit_logger
import offline_nlp_processor
import standard_guillotine_veto
import local_biometric_auth
import standard_mesh_node
import standard_gpio_matrix

def run_terminal_loop():
    print("POWERING NODE...")
    
    # 1. THE IDENTITY GATEKEEPER
    sensor_hash = input("[Scanner Active] Awaiting Identity Hash: ").strip()
    if not local_biometric_auth.verify_operator_biometrics(sensor_hash):
        print("ERROR: IDENTITY REJECTED. TERMINATING SEQUENCE.")
        return

    # 2. TERMINAL, MESH & HARDWARE INITIALIZATION
    print("INITIALIZING LOCAL INTEGRATED TERMINAL...")
    active_language = operator_interface.execute_local_interface('en')
    
    if not active_language:
        print("ERROR: Initialization failed. Standard Override Engaged.")
        local_audit_logger.secure_log_action("INIT", "FAILED")
        return

    if not standard_mesh_node.initialize_mesh_transceiver():
        print("ERROR: Mesh Transceiver failed. Asset isolated. Lockout Engaged.")
        return

    if not standard_gpio_matrix.initialize_hardware_pins():
        print("ERROR: Hardware Matrix failed. Relays severed.")
        return

    local_audit_logger.secure_log_action("INIT", "SUCCESS - FULL INTEGRATION ACTIVE")
    print("--- TERMINAL ACTIVE: SENSOR & HARDWARE CONTROL ENABLED ---")
    
    # 3. CONTINUOUS EXECUTION LOOP
    while True:
        try:
            standard_mesh_node.broadcast_asset_heartbeat("ACTIVE")

            voice_input = input("\n[Local Mic Active] Input Command: ").strip()
            if not voice_input:
                continue
                
            intended_pwm = offline_nlp_processor.process_acoustic_input(voice_input)
            
            # Network Level Veto
            simulated_incoming_radio_distance = 1800.0
            if standard_mesh_node.scan_fleet_proximity(simulated_incoming_radio_distance):
                print("NETWORK OVERRIDE: Perimeter breached via Mesh. Vetoing intent.")
                intended_pwm = 0.0
            
            # Local Sensor Level Veto
            simulated_distance_cm = 200.0
            final_pwm = standard_guillotine_veto.evaluate_spatial_veto(intended_pwm, simulated_distance_cm)
            
            # Hardware Actuation
            print(f"OUTPUT: Pushing verified {final_pwm}% to hardware.")
            standard_gpio_matrix.actuate_iron(final_pwm)
            
            if voice_input.lower() == "stop":
                break
                
            time.sleep(0.1)
            
        except KeyboardInterrupt:
            print("\nTerminal offline. Dropping hardware relays to 0.0%.")
            standard_gpio_matrix.actuate_iron(0.0)
            local_audit_logger.secure_log_action("OFFLINE", "DEFAULT HALT")
            break

if __name__ == "__main__":
    run_terminal_loop()
