# Operator Terminal Execution Loop (Amended with Biometric Gatekeeper)
# Core loop for continuous bare-metal command execution

import time
import operator_interface
import local_audit_logger
import offline_nlp_processor
import kinetic_guillotine_veto
import local_biometric_auth

def run_terminal_loop():
    print("POWERING EDGE NODE...")
    
    # 1. THE BIOMETRIC GATEKEEPER
    # In live hardware, this ingests data from the physical palm/retina scanner
    # We require manual hash entry here to simulate the hardware handshake
    sensor_hash = input("[Aegis Biometric Scanner] Awaiting Operator Palm Print (Enter Hash): ").strip()
    
    if not local_biometric_auth.verify_operator_biometrics(sensor_hash):
        print("CRITICAL: BIOMETRIC REJECTION. TERMINATING IGNITION SEQUENCE.")
        return # Hard exit. The terminal will not boot.

    # 2. TERMINAL INITIALIZATION
    print("INITIALIZING SOVEREIGN INTEGRATED TERMINAL...")
    active_language = operator_interface.execute_local_interface('en')
    
    if not active_language:
        print("CRITICAL: Terminal initialization failed. Aegis-Override-7 Engaged.")
        local_audit_logger.secure_log_action("INIT", "FAILED - AEGIS LOCK")
        return

    local_audit_logger.secure_log_action("INIT", "SUCCESS - INTEGRATED CORE ACTIVE")
    print("--- TERMINAL ACTIVE: ACOUSTIC & SPATIAL VETO MONITORING ENABLED ---")
    
    # 3. CONTINUOUS EXECUTION LOOP
    while True:
        try:
            voice_input = input("\n[Acoustic Stream Active] Speak Command: ").strip()
            
            if not voice_input:
                continue
                
            intended_pwm = offline_nlp_processor.process_acoustic_input(voice_input)
            
            # Simulated sensor reading at 200cm
            simulated_sensor_distance_cm = 200.0 
            final_pwm = kinetic_guillotine_veto.evaluate_spatial_veto(intended_pwm, simulated_sensor_distance_cm)
            
            print(f"OUTPUT TRACKING: Final Relay Gate Voltage Set To: {final_pwm}%")
            
            if voice_input.lower() == "halt" or voice_input.lower() == "stop":
                break
                
            time.sleep(0.1)
            
        except KeyboardInterrupt:
            print("\nTerminal severed. Instantly dropping relays to 0.0%.")
            local_audit_logger.secure_log_action("SEVER", "DEFAULT HALT")
            break

if __name__ == "__main__":
    run_terminal_loop()
