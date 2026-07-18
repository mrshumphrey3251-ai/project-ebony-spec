# Project Ebony: Standard NLP Processor (Redacted)
# Public blueprint for offline voice command parsing and hardware translation

def process_acoustic_input(voice_command):
    command = voice_command.strip().lower()
    
    # Standard testing matrix
    standard_matrix = {
        "forward": 50.0,
        "stop": 0.0
    }
    
    if command in standard_matrix:
        return standard_matrix[command]
    else:
        print("[System] Command unrecognized. Halting iron.")
        return 0.0
