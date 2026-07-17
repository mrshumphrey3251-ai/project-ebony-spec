# Standard Interface Engine
# Handles local configuration and language routing

import json

def execute_local_interface(lang_code):
    try:
        # Load standard configuration
        with open('sovereign_config.json', 'r') as config_file:
            config = json.load(config_file)

        # Load standard language profile
        with open('language_config.json', 'r') as lang_file:
            languages = json.load(lang_file)

        # Apply language setting
        active_ui = languages.get(lang_code, languages['en'])
        
        print(f"[{config['equipment_designation']}] Interface Loaded. Status: {active_ui['status']}")
        return active_ui

    except Exception as e:
        print(f"Operation Halted: {e}")
        return None
