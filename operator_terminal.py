# Project Ebony: Standard Operator Terminal (Redacted)
# Unified terminal loop with integrated power management

import offline_nlp_processor
import standard_guillotine_veto
import local_biometric_auth
import standard_mesh_node
import standard_gpio_matrix
import standard_telemetry_engine
import standard_power_management

def run_terminal_loop():
    print("=== POWERING STANDARD EDGE NODE ===")
    
    sensor_hash = input("[Biometric Auth] Input Hash: ").strip()
    if not local_biometric_auth.verify_operator_biometrics(sensor_hash):
        print("CRITICAL: REJECTION. TERMINATING IGNITION.")
        return 

    standard_mesh_node.initialize_mesh_transceiver()
    standard_gpio_matrix.initialize_hardware_pins()
    print("--- TERMINAL LOGGED IN: SYSTEM ONLINE ---")
    
    try:
        while True:
            voice_input = input("\n[Acoustic Input] Enter Voice Command: ").strip()
            intended_pwm = offline_nlp_processor.process_acoustic_input(voice_input)

            radio_dist, sensor_dist = standard_telemetry_engine.execute_telemetry_sweep()

            if standard_mesh_node.scan_fleet_proximity(radio_dist):
                intended_pwm = 0.0

            final_pwm = standard_guillotine_veto.evaluate_spatial_veto(intended_pwm, sensor_dist)

            # Hardware Health Override
            health_status, hardware_veto = standard_power_management.evaluate_hardware_health()
            if hardware_veto:
                print("CRITICAL OVERRIDE: Hardware fault detected. Actuation severed.")
                final_pwm = 0.0

            standard_gpio_matrix.actuate_iron(final_pwm)
            
    except KeyboardInterrupt:
        print("\n[SYSTEM] Terminating loop.")
        
    print("=== RUN COMPLETED ===")

if __name__ == "__main__":
    run_terminal_loop()
