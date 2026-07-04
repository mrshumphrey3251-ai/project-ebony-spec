# CLUSTER_FEDERATION: Decentralized Consensus & CRDT Synchronization

**Classification:** Gated Engineering Documentation / Network Topology Layer
**Target Architecture:** Sub-GHz DAG Mesh / RT-PREEMPT Network Stack

This file outlines the local, peer-to-peer network consensus models used to synchronize state maps across disconnected edge nodes. Project Ebony fleets operate in highly fractured, GPS-denied, and WAN-severed environments. The localized mesh must autonomously resolve data conflicts, maintain state parity, and dynamically reconfigure routing topologies without reliance on a central cloud server.

## 1. Decentralized State Alignment & CRDT Mechanics
When a geographic cluster fractures due to terrain or RF jamming, sub-clusters continue to operate and generate local telemetry. When they physically reconnect, divergent data streams must merge seamlessly.

* **State-Based CRDTs (Conflict-free Replicated Data Types):** The node network relies on state-based CRDTs mapped via FlatBuffer payloads. The native C++ runtime merges divergent operational states ($S_A$ and $S_B$) using a mathematically defined join semi-lattice. The merge operator ($\sqcup$) is strictly commutative, associative, and idempotent:
  $$S_{merged} = S_A \sqcup S_B$$
  This guarantees that regardless of the order in which delayed sub-GHz packets arrive, all nodes eventually converge on the exact same mathematically provable state vector.
* **Quorum-Based Execution:** High-privilege network configurations (e.g., executing a fleet-wide cryptographic epoch roll or issuing a mass mechanical override) cannot be triggered unilaterally. The system requires cryptographic multi-signature validation from a strict quorum of verified physical peer nodes. For a total fleet size of $N$, the required quorum $Q$ must satisfy a strict majority:
  $$Q \ge \left\lfloor \frac{N}{2} \right\rfloor + 1$$
  Until this threshold of valid ML-KEM cryptographic signatures is reached, the local state change is held in a volatile pending queue.

## 2. Dynamic Cluster Election & Vertex Routing
The fleet architecture utilizes a Directed Acyclic Graph (DAG) for data routing, which relies on a primary gateway node for efficient backhaul. This introduces a potential single point of failure if that node is physically destroyed or jammed.

* **Automated Decentralized Election:** If the local mesh detects the primary gateway is offline (via missed hardware heartbeats), the remaining nodes immediately execute a decentralized election loop to nominate a new regional routing vertex.
* **Weighted Heuristic Algorithm:** Nodes do not vote randomly. Each active node computes its own fitness weight ($W_i$) natively, based on its current localized signal-to-noise ratio ($SNR_i$), available battery State of Charge ($SoC_i$), and current CPU compute load ($C_i$):
  $$W_i = \alpha (SoC_i) + \beta (SNR_i) - \gamma (C_i)$$
  *(Where $\alpha, \beta,$ and $\gamma$ are hardcoded environmental tuning coefficients).*
* **Seamless Handoff:** The nodes broadcast their fitness weights over the radio mesh. The node yielding the maximum $W_i$ is instantly elected as the new apex router. The DAG topology recalculates natively, rerouting all local FlatBuffer telemetry through the new vertex within milliseconds.
