# Project Ebony: Standard Operator Terminal (Redacted)
# Unified terminal loop for public architectural review

import offline_nlp_processor
import standard_guillotine_veto
import local_biometric_auth
import standard_mesh_node
import standard_gpio_matrix
import standard_telemetry_engine
import standard_audit_logger

def run_terminal_loop():
    print("=== POWERING STANDARD EDGE NODE ===")
    
    # 1. BIOMETRIC HANDSHAKE
    sensor_hash = input("[Biometric Auth] Input Hash: ").strip()
    if not local_biometric_auth.verify_operator_biometrics(sensor_hash):
        print("CRITICAL: REJECTION. TERMINATING IGNITION.")
        return 

    # 2. SUBSYSTEM ENGAGEMENT
    standard_mesh_node.initialize_mesh_transceiver()
    standard_gpio_matrix.initialize_hardware_pins()
    print("--- TERMINAL LOGGED IN: SYSTEM ONLINE ---")
    
    # 3. CONTINUOUS OVERWATCH
    print("\n[SYSTEM] Continuous Overwatch Active. Press Ctrl+C to stop.")
    while True:
        try:
            voice_input = input("\n[Acoustic Input] Enter Voice Command: ").strip()
            intended_pwm = offline_nlp_processor.process_acoustic_input(voice_input)

            # Ingest Standard Telemetry
            radio_dist, sensor_dist = standard_telemetry_engine.poll_standard_sensors()
            
            if standard_mesh_node.scan_fleet_proximity(radio_dist):
                intended_pwm = 0.0

            final_pwm = standard_guillotine_veto.evaluate_spatial_veto(intended_pwm, sensor_dist)
            standard_gpio_matrix.actuate_iron(final_pwm)
            
            # Execute Standard Logging
            standard_audit_logger.secure_log_action(voice_input, f"PWM: {final_pwm}")
            
        except KeyboardInterrupt:
            break
            
    print("\n=== SYSTEM OFFLINE ===")

if __name__ == "__main__":
    run_terminal_loop()
