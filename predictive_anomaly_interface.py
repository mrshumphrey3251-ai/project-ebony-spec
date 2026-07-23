#!/usr/bin/env python3

class PredictiveAnomalyInterface:
    PROTOCOL_IDENTIFIER = "THETA_v1"
    MIN_SAMPLE_RATE_HZ = 1000

    @staticmethod
    def validate_telemetry_frame(frame: dict) -> bool:
        required = ["jitter_ms", "shift_hz", "sample_rate"]
        if not all(k in frame for k in required):
            return False
        return frame["sample_rate"] >= PredictiveAnomalyInterface.MIN_SAMPLE_RATE_HZ

if __name__ == "__main__":
    frame = {"jitter_ms": 0.05, "shift_hz": 0.1, "sample_rate": 1000}
    assert PredictiveAnomalyInterface.validate_telemetry_frame(frame) == True
    print("--> 100% VERIFIED: Public PredictiveAnomalyInterface (Protocol Theta) printed and validated.")
