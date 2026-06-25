# Access Control Specification

This document details the decentralized, cryptographic, and biometric access control perimeters for the sovereign edge ecosystem.

## 1. Zero-Trust Local Perimeter
* **Air-Gapped Authentication:** All cryptographic token verification and identity checks must execute locally on native iron. The runtime rejects any dependencies on external wide-area network (WAN) authorization servers.
* **Hardware Cryptographic Sealing:** Symmetric and asymmetric operational keys are bound directly to the hardware Platform Configuration Registers (PCRs) via the local Trusted Platform Module (TPM 2.0).

## 2. Multi-Factor Token Handshakes
* Node-to-node session validation utilizes short-lived, post-quantum encrypted challenges.
* High-privilege mechanical overrides or configuration flashes require a local hardware handshake token combined with real-time biometric operator confirmation.
