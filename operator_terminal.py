# Standard Terminal Execution Loop (Amended with Audit Logging)
# Core loop for continuous localized command execution

import time
import operator_interface
import local_audit_logger

def run_terminal_loop():
    print("INITIALIZING LOCAL TERMINAL...")
    active_language = operator_interface.execute_local_interface('en')
    
    if not active_language:
        print("ERROR: Terminal initialization failed. Standard-Override Engaged. Locking system.")
        local_audit_logger.secure_log_action("INIT", "FAILED - OVERRIDE ENGAGED")
        return

    local_audit_logger.secure_log_action("INIT", "SUCCESS")
    print("--- TERMINAL ACTIVE ---")
    
    while True:
        try:
            command = input(f"Awaiting input [{active_language['start']} / {active_language['stop']}]: ").strip().lower()
            
            if command == "stop":
                print(f"EXECUTING: {active_language['stop']}. Halting operations.")
                local_audit_logger.secure_log_action(command, "EXECUTED - HALT")
                break
            elif command == "start":
                print(f"EXECUTING: {active_language['start']}. Engaging sequence.")
                local_audit_logger.secure_log_action(command, "EXECUTED - SEQUENCE ENGAGED")
            else:
                print("Unrecognized parameter. System holds current state.")
                local_audit_logger.secure_log_action(command, "DENIED - UNKNOWN")
                
            time.sleep(0.1)
            
        except KeyboardInterrupt:
            print(f"\nTerminal offline. {active_language['stop']} executed.")
            local_audit_logger.secure_log_action("OFFLINE", "EXECUTED - DEFAULT HALT")
            break

if __name__ == "__main__":
    run_terminal_loop()
