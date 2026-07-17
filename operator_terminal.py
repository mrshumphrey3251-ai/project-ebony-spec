# Standard Terminal Execution Loop
# Core loop for continuous localized command execution

import time
import operator_interface

def run_terminal_loop():
    print("INITIALIZING LOCAL TERMINAL...")
    
    active_language = operator_interface.execute_local_interface('en')
    
    if not active_language:
        print("ERROR: Terminal initialization failed. Standard-Override Engaged. Locking system.")
        return

    print("--- TERMINAL ACTIVE ---")
    while True:
        try:
            command = input(f"Awaiting input [{active_language['start']} / {active_language['stop']}]: ").strip().lower()
            
            if command == "stop":
                print(f"EXECUTING: {active_language['stop']}. Halting operations.")
                break
            elif command == "start":
                print(f"EXECUTING: {active_language['start']}. Engaging sequence.")
            else:
                print("Unrecognized parameter. System holds current state.")
                
            time.sleep(0.1)
            
        except KeyboardInterrupt:
            print(f"\nTerminal offline. {active_language['stop']} executed.")
            break

if __name__ == "__main__":
    run_terminal_loop()
