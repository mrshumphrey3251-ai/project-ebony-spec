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
