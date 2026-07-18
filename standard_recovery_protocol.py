# Project Ebony: Standard Asset Recovery Protocol (Redacted)
# Public blueprint for emergency hardware extraction

import standard_gpio_matrix

def execute_standard_extraction():
    print("!!! INITIATING STANDARD RECOVERY !!!")
    
    # Standard manual override verification
    override_key = input("[Override] Enter Key: ").strip()
    
    if override_key != "STANDARD_KEY_1":
        print("REJECTION. ASSET LOCKED.")
        return

    print("--- OVERRIDE ACCEPTED. ENGAGING MANUAL CRAWL. ---")
    standard_gpio_matrix.initialize_hardware_pins()

    try:
        while True:
            # Standard crawl speed
            standard_gpio_matrix.actuate_iron(20.0)
            
    except KeyboardInterrupt:
        print("\n[SYSTEM] Recovery terminated.")
        standard_gpio_matrix.actuate_iron(0.0)

if __name__ == "__main__":
    execute_standard_extraction()
