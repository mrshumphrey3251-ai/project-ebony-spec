#!/usr/bin/env python3

class ScadaBridgeInterface:
    PROTOCOL_IDENTIFIER = "KAPPA_v1"

    @staticmethod
    def validate_wrapped_frame(frame: dict) -> bool:
        ebony = frame.get("ebony_frame", {})
        sig = frame.get("signature", "")
        required = ["protocol", "bridge_id", "can_id", "raw_payload"]
        return all(k in ebony for k in required) and len(sig) == 64

if __name__ == "__main__":
    sample = {
        "ebony_frame": {"protocol": "KAPPA_v1", "bridge_id": "B1", "can_id": "0x18FEF000", "raw_payload": "00"},
        "signature": "0" * 64
    }
    assert ScadaBridgeInterface.validate_wrapped_frame(sample) == True
    print("--> 100% VERIFIED: Public ScadaBridgeInterface (Protocol Kappa) printed and validated.")
