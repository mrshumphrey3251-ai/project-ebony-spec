#!/usr/bin/env python3
# ===========================================================================
# [HVF EXECUTIVE DISCLAIMER]
# PROPERTY OF HUMPHREY VIRTUAL FARM.
# EACH FILE IS ENTIRELY OF MY OWN DESIGN, CREATED WITHOUT PREVIOUS KNOWLEDGE OF, OR DERIVATION FROM, ANY OTHER WORK.
# PUBLIC DISCLOSURE OF THIS ARCHITECTURAL BLUEPRINT IS FOR DEMONSTRATION ONLY.
# THIS DOES NOT GRANT USAGE, MODIFICATION, OR DISTRIBUTION RIGHTS.
# UNAUTHORIZED REPLICATION OR COMMERCIAL DEPLOYMENT IS STRICTLY PROHIBITED.
# ===========================================================================

import hashlib, json

class ForensicBlackBoxInterface:
    PROTOCOL_IDENTIFIER = "ZETA_v1"

    @staticmethod
    def verify_chain_entry(entry: dict) -> bool:
        check_entry = dict(entry)
        given_hash = check_entry.pop("chain_hash", "")
        canonical_bytes = json.dumps(check_entry, sort_keys=True).encode("utf-8")
        expected_hash = hashlib.sha256(canonical_bytes).hexdigest()
        return given_hash == expected_hash

if __name__ == "__main__":
    sample = {"seq": 1, "timestamp": 1783753814.0, "event": "TEST_EVENT", "details": {}, "prev_hash": "0" * 64}
    canonical = json.dumps(sample, sort_keys=True).encode("utf-8")
    sample["chain_hash"] = hashlib.sha256(canonical).hexdigest()
    assert ForensicBlackBoxInterface.verify_chain_entry(sample) == True
    print("--> 100% VERIFIED: Public ForensicBlackBoxInterface validated.")
