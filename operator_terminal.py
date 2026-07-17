# Standard Terminal Execution Loop (Amended with Voice & Safety Veto)
# Core loop for continuous localized command execution

import time
import operator_interface
import local_audit_logger
import offline_nlp_processor
import standard_guillotine_veto

def run_terminal_loop():
    print("INITIALIZING LOCAL INTEGRATED TERMINAL...")
    active_language = operator_interface.execute_local_interface('en')
    
    if not active_language:
        print("ERROR: Initialization failed. Standard Override Engaged.")
        local_audit_logger.secure_log_action("INIT", "FAILED")
        return

    local_audit_logger.secure_log_action("INIT", "SUCCESS")
    print("--- TERMINAL ACTIVE: LOCAL VOICE & SAFETY MONITORING ENABLED ---")
    
    while True:
        try:
            voice_input = input("\n[Local Mic Active] Input Command: ").strip()
            
            if not voice_input:
                continue
                
            intended_pwm = offline_nlp_processor.process_acoustic_input(voice_input)
            
            # Standard safety perimeter check
            simulated_distance_cm = 200.0
            final_pwm = standard_guillotine_veto.evaluate_spatial_veto(intended_pwm, simulated_distance_cm)
            
            print(f"OUTPUT: Relay Output Set To: {final_pwm}%")
            
            if voice_input.lower() == "stop":
                break
                
            time.sleep(0.1)
            
        except KeyboardInterrupt:
            print("\nTerminal offline. Dropping to 0.0%.")
            local_audit_logger.secure_log_action("OFFLINE", "DEFAULT HALT")
            break

if __name__ == "__main__":
    run_terminal_loop()
