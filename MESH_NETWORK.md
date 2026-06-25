# Mesh Network Topology & Decentralized Protocol Architecture

This specification covers the physical layer settings, custom bit-packed schemas, and frequency-hopping mesh routing algorithms for the sub-GHz network array.

## 1. Frequency-Hopping Spread Spectrum (FHSS)
* **Pseudo-Random Hop Sequences:** Nodes synchronize timing bands locally using hardware clocks to jump across sub-GHz frequencies, mitigating localized jamming.
* **Zero-Parse Binary Framing:** Telemetry frames avoid standard heavy network protocols, relying on compressed FlatBuffer structures designed to maximize data density over low-bandwidth wires.

## 2. Dynamic Routing & Peer Disruption
* Implements ad-hoc distance-vector mesh routing, allowing disconnected field nodes to seamlessly self-heal network topology paths as assets move through physical terrain.
