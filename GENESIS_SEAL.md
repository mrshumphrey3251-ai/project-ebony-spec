# GENESIS_SEAL: Initial Cryptographic Identity & Hardware Provisioning

**Classification:** Gated Engineering Documentation / Cryptographic Fiduciary Layer
**Target Architecture:** TPM 2.0 / eFuse OTP / Air-Gapped Initialization

This document details the first-boot cryptographic provisioning, master key generation, and non-volatile configuration freezing procedures. Project Ebony assets are born into hostile environments. A node's cryptographic identity cannot be assigned by a vulnerable cloud server; it must be generated natively on the bare metal during the initial physical instantiation. This guarantees the node is mathematically tethered to its specific physical chassis and completely immune to supply chain cloning.

## 1. Initial State Provisioning & eFuse Locking
The factory state of the edge silicon is inherently untrusted. The initial boot sequence must purge all manufacturing keys and permanently fuse the hardware to the organizational root of trust.

* **Hardware Root Verification (TPM 2.0):** Upon the first application of power, the RT-PREEMPT kernel erases all default manufacturing test keys. It provisions an isolated, node-specific cryptographic identity natively. The physical TPM 2.0 block generates the primary Attestation Identity Key (AIK) using the native Elliptic Curve base point ($G$) and a perfectly randomized internal private scalar ($d$):
  $$Q_{AIK} = d \cdot G$$
  This private key ($d$) is mathematically bound to the silicon and cannot be extracted by any physical or software-based side-channel attack.
* **Firmware Configuration Lock (OTP):** To prevent malicious field modifications or bootkit injections, the core system hardware settings are physically frozen. The node writes the cryptographic hash of the verified secure bootloader ($H_{boot}$) permanently to the silicon's One-Time Programmable (OTP) eFuses:
  $$H_{boot} = \text{SHA-384}(F_{loader})$$
  Once the electron state of the physical eFuse is altered, the transition is thermodynamically and mathematically irreversible. The motherboard will strictly halt the boot process if future firmware attempts do not perfectly match this burned hardware hash.

## 2. Master Identity Syncing & Zero-Trust Registration
A newly minted node must establish its existence without relying on wide-area network (WAN) interactions, cloud databases, or vulnerable DNS routing.

* **Genesis Block Generation:** The edge node generates a primary identity matrix block ($I_{genesis}$) natively. This block serves as the absolute root of the node's local CRDT ledger (`FIDUCIARY_LAYER_LEDGER.md`).
* **Cryptographic Binding:** The Genesis Block mathematically binds the physical hardware serial ID ($HW_{ID}$), the TPM-generated public key ($Q_{AIK}$), and the ultra-precise hardware timestamp ($t_0$) of the first boot:
  $$I_{genesis} = \text{SHA-384}(HW_{ID} \parallel Q_{AIK} \parallel t_0)$$
* **Mesh Propagation:** This immutable matrix is broadcast over the localized sub-GHz mesh. Adjacent peer nodes ingest $I_{genesis}$, mathematically verify the cryptographic signature against the localized organizational root certificate, and authorize the new node to participate in the physical consensus pool, completing the initial handshake with zero external network dependencies.
