#!/usr/bin/env python3

class GPIOActuationInterface:
    PROTOCOL_IDENTIFIER = "ETA_v1"
    REQUIRED_PINS = {
        "MAIN_POWER_CONTACTOR": 18,
        "BUS_ISOLATION_RELAY":  23,
        "STATUS_BEACON":        24
    }

    @staticmethod
    def validate_pin_configuration(config: dict) -> bool:
        for pin_name, expected_pin in GPIOActuationInterface.REQUIRED_PINS.items():
            if config.get(pin_name) != expected_pin:
                return False
        return True

if __name__ == "__main__":
    vendor_config = {"MAIN_POWER_CONTACTOR": 18, "BUS_ISOLATION_RELAY": 23, "STATUS_BEACON": 24}
    assert GPIOActuationInterface.validate_pin_configuration(vendor_config) == True
    print("--> 100% VERIFIED: Public GPIOActuationInterface (Protocol Eta) validated.")
