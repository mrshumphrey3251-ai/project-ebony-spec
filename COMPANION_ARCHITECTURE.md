# COMPANION_ARCHITECTURE: Human-Asset Synchronization & Cryptographic LOTO

**Classification:** Gated Engineering Documentation / Human-Machine Interface (HMI) Layer
**Target Architecture:** NVIDIA Jetson GPU / Local AR/VR Sandbox / TPM 2.0

This document outlines the decentralized specifications for The Companion—the local, interactive interface layer of Project Ebony running natively on edge silicon. This architecture enforces zero-trust physical safety through immersive, latency-bound training and un-bypassable hardware lockdowns, effectively neutralizing human operational error.

## 1. LOTO-by-Training (Cryptographic Verification)
Traditional industrial Lockout/Tagout (LOTO) protocols rely on passive, analog mechanisms (padlocks and paper tags) which are highly vulnerable to physical bypass and human negligence. Project Ebony replaces these archaic practices with a hardware-enforced, cryptographic gate tied directly to real-time operator competency validation.

* **The Silicon Lock:** The local control rail, ignition circuits, and PLC override mechanisms are maintained in a hardened, un-bootable state by default. The primary solid-state SCADA relays remain physically open, governed by keys held strictly within the TPM 2.0 secure enclave.
* **Dynamic Safety Credentialing & Competency Decay:** The physical asset refuses to pass ignition voltages until the native C++ runtime processes a cryptographically signed authorization token ($T_{auth}$) from the Companion interface.
* **The Requirement:** Authorization is granted if and only if the biologically verified operator (via `BIOMETRIC_IDENTITY.md`) has successfully logged a passing score in the specific synthetic training sandbox. The system computes the operator's retained competency $C(t)$ using a temporal decay function natively:
  $$C(t) = C_0 e^{-\lambda (t - t_{train})}$$
  *(Where $C_0$ is the verified training score, $t_{train}$ is the timestamp of the completed simulation, and $\lambda$ is the strict task-specific memory decay constant).* * **Galvanic Release:** The TPM releases the relay decryption keys to the RT-PREEMPT kernel if, and only if, the current competency score mathematically exceeds the absolute safety threshold ($C(t) \ge C_{critical}$). If the temporal validation window expires, the asset mechanically bricks itself to that specific operator until re-certification is completed locally.

## 2. Immersive AR/VR Synthetic Sandbox & Edge Rendering
To eliminate accidents caused by untrained personnel or unexpected field anomalies, operators are required to interface with the asset digitally before executing physical manipulation. 

* **Zero-Cloud Emulation:** The Companion generates a 1:1 high-fidelity synthetic environment directly on the Jetson Orin's GPU. The physical properties of the simulation—hydraulic pressures, terrain friction coefficients, and center-of-gravity dynamics—are continuously mirrored from the asset's live telemetry ledgers.
* **Motion-to-Photon Determinism:** To prevent operator disorientation and ensure perfect kinematic parity between the digital sandbox and physical controls, the AR/VR render pipeline is strictly bounded. The total system latency ($L_{total}$) must not exceed the human vestibular limit:
  $$L_{total} = L_{ingest} + L_{compute} + L_{render} + L_{display} \le 18 \text{ ms}$$
  By executing the simulation entirely on the localized edge-silicon and bypassing external network hops, the node mathematically guarantees zero-latency interaction.
* **Physical Handoff:** Once the operator successfully executes the hazardous operation within the physical parameters of the sandbox without registering a kinetic fault, the Companion generates the required cryptographic hash, writes it to the local audit ledger (`TAMPER_EVIDENT_AUDIT_LOGGING.md`), and instantly unlocks the physical analog controls.
