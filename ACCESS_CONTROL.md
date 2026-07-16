# ACCESS_CONTROL: Air-Gapped Authentication & Hardware-Bound Perimeters

**Classification:** Gated Engineering Documentation / Identity Layer
**Target Architecture:** Offline Zero-Trust Identity Mesh

This specification details the decentralized, cryptographic, and biometric access control perimeters for the sovereign edge ecosystem. Project Ebony fundamentally rejects wide-area network (WAN) dependencies for authorization; if an operator cannot mathematically prove their identity to the local iron while 100% air-gapped, access is denied.

## 1. Zero-Trust Local Perimeter

* **Air-Gapped Authentication:** All cryptographic token verification, role-based access control (RBAC), and identity checks execute natively on the local RT-PREEMPT kernel. There are no external OAuth, OIDC, or cloud-based Active Directory fallbacks. 
* **Hardware Cryptographic Sealing:** Symmetric and asymmetric operational keys are bound directly to the hardware Platform Configuration Registers (PCRs) via the local Trusted Platform Module (TPM 2.0). Extracting the identity ledger requires defeating the physical eFuses on the motherboard.

## 2. Multi-Factor Token Handshakes

* **Mesh Session Validation:** Node-to-node session validation utilizes short-lived, post-quantum encrypted challenges (ML-KEM-1024) to prevent replay attacks across the sub-GHz radio layer.
* **High-Privilege Mechanical Overrides:** Executing a configuration flash or a manual hydraulic bypass requires a strict localized handshake. The operator must present a physical hardware token (FIDO2/PIV) containing an ML-DSA-85 signature, combined with real-time biometric confirmation processed entirely inside the local secure enclave.

# ACTUATOR_CONTROL: J1939 CAN Bus Injection & Hydraulic Override Protocols

**Classification:** Gated Engineering Documentation / Cyber-Physical Control Layer
**Target Architecture:** Electro-Hydraulic Pilot Valves / J1939 CAN Bus

This specification outlines the direct, bare-metal injection mechanics used by Project Ebony to govern physical machinery without relying on OEM telematics or cloud-dependent APIs. True operational sovereignty dictates that intelligence must compile directly to the physical actuators.

## 1. Direct J1939 CAN Bus Injection

Project Ebony bypasses abstracted high-level machine controllers to interface directly with the primary J1939 CAN bus network.

* **Deterministic Framing:** The hardened C++ runtime constructs and injects raw CAN frames (PGNs) directly into the electro-hydraulic manifold controllers. 
* **Latency Guarantee:** By pinning the injection threads to `SCHED_FIFO` on the RT-PREEMPT kernel (as defined in `CORE_ENGINE.md`), the system guarantees a control loop transmission jitter of **< 5 ms**, enabling precise closed-loop PID control over steering and implement elevation.

## 2. State-Based Actuator Resolution

When the localized mesh fractures or transitions to offline store-and-forward routing, actuator state is resolved locally to prevent erratic machine behavior.

* **CRDT Actuator Convergence:** If conflicting macro-commands are received during a mesh split-brain scenario, the local node defers to the mathematically heavier state ledger (as resolved by the Merkle tree convergence in `CRDT_MERGE_MECHANIC.md`). 
* **Localized Sanity Bounding:** The local node enforces strict physical bounding boxes. Even if a valid cryptographic command requests a 100% actuator extension, the local sensor matrix will block the injection if the onboard IMU detects an unsafe chassis pitch or roll angle.

## 3. Deadman Fallback & Spring-Return Severance

Physical safety supersedes software instruction. If the cryptographic perimeter is breached, or the hardware watchdog detects a dropped `cgroups` thread:

* **Relay Severance:** The core engine drops the voltage on the localized solid-state relays (SSRs).
* **Spring-Return Immobilization:** Without active hold voltage, the IP69K linear actuators and hydraulic pilot valves immediately snap to their mechanical spring-return zero positions, locking the machinery's brakes and dropping all implements to the ground.
### Edge-Native Kernel Intercept (Phase 2)

To secure the localized mesh topology against internal bad actors or compromised secondary devices, the core processing node utilizes a two-tiered architectural intercept protocol.

* **Layer 1 (Network Bounding):** The primary execution runtime enforces a strict, hardcoded IP Whitelist at the socket level. Sockets originating from unregistered MAC/IP addresses are severed before thread allocation occurs, protecting the runtime from buffer overflow attacks or resource exhaustion on the local mesh.
* **Layer 2 (Application Gate):** Packets that pass the network bounding layer must then execute the cryptographic token handshake and conform perfectly to the immutable JSON schema before physical hardware manipulation is authorized.
