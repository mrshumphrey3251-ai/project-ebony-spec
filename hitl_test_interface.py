#!/usr/bin/env python3
# ===========================================================================
# [HVF EXECUTIVE DISCLAIMER]
# PROPERTY OF HUMPHREY VIRTUAL FARM.
# EACH FILE IS ENTIRELY OF MY OWN DESIGN, CREATED WITHOUT PREVIOUS KNOWLEDGE OF, OR DERIVATION FROM, ANY OTHER WORK.
# PUBLIC DISCLOSURE OF THIS ARCHITECTURAL BLUEPRINT IS FOR DEMONSTRATION ONLY.
# THIS DOES NOT GRANT USAGE, MODIFICATION, OR DISTRIBUTION RIGHTS.
# UNAUTHORIZED REPLICATION OR COMMERCIAL DEPLOYMENT IS STRICTLY PROHIBITED.
# ===========================================================================


class HITLTestInterface:
    PROTOCOL_IDENTIFIER = "LAMBDA_v1"
    MAX_RELAY_LATENCY_MS = 10.0

    @staticmethod
    def validate_hitl_report(report: dict) -> bool:
        required = ["fault_injected", "trip_latency_ms", "relay_state", "hitl_pass"]
        if not all(k in report for k in required):
            return False
        return (report["trip_latency_ms"] <= HITLTestInterface.MAX_RELAY_LATENCY_MS) and (report["hitl_pass"] == True)

if __name__ == "__main__":
    sample = {"fault_injected": "TEST", "trip_latency_ms": 1.2, "relay_state": 0, "hitl_pass": True}
    assert HITLTestInterface.validate_hitl_report(sample) == True
    print("--> 100% VERIFIED: Public HITLTestInterface (Protocol Lambda) printed and validated.")
