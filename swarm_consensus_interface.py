#!/usr/bin/env python3

class SwarmConsensusInterface:
    PROTOCOL_IDENTIFIER = "IOTA_v1"
    CONSENSUS_THRESHOLD_PERCENT = 51.0

    @staticmethod
    def validate_vote_payload(payload: dict) -> bool:
        required = ["voting_node", "target_node", "yes_votes", "total_nodes"]
        return all(k in payload for k in required)

if __name__ == "__main__":
    payload = {"voting_node": "N1", "target_node": "N2", "yes_votes": 2, "total_nodes": 3}
    assert SwarmConsensusInterface.validate_vote_payload(payload) == True
    print("--> 100% VERIFIED: Public SwarmConsensusInterface (Protocol Iota) printed and validated.")
