# OFFLINE_FIRMWARE_PATCH: Air-Gapped Propagation & PQ-Cryptographic Signing

**Classification:** Gated Engineering Documentation / Firmware Integrity Layer
**Target Architecture:** A/B Rootfs Partitions / TPM 2.0 / Post-Quantum (FIPS 204/ML-DSA)

This document establishes the cryptographic signing, local rollback, and peer-to-peer patch propagation rules for fully air-gapped system upgrades. Project Ebony assets cannot connect to the open internet to pull OTA (Over-The-Air) updates. Firmware patches are injected via physical vectors or propagated over the sub-GHz mesh. The system must autonomously verify, stage, and execute these payloads with mathematical certainty, neutralizing the risk of a corrupted update bricking a deployed node.

## 1. Post-Quantum Sign Verification & TPM Binding
Standard RSA/ECC signatures are increasingly vulnerable to store-now-decrypt-later quantum attacks. The edge node enforces strict Post-Quantum Cryptography (PQC) for all firmware updates.

* **Asymmetric Integrity Check (Lattice-Based):** Updates must be cryptographically signed by verified organizational root keys. The update engine validates signatures locally using FIPS 204 (ML-DSA) post-quantum algorithms before unpacking payloads into RAM. The native C++ runtime evaluates the signature vector ($\mathbf{z}$) and challenge polynomial ($c$). The firmware is mathematically rejected unless it satisfies the strict infinity norm boundary:
  $$||\mathbf{z}||_\infty < \gamma \quad \land \quad c = \text{Hash}(M \parallel \mathbf{w}_1)$$
  *(Where $\gamma$ is the maximum allowed coefficient bound in the polynomial ring, $M$ is the firmware payload, and $\mathbf{w}_1$ is the reconstructed commitment).* This mathematically guarantees that a quantum-capable adversary cannot forge a valid firmware payload.
* **TPM Hash Validation:** Verification keys are never stored in volatile memory. They are tied directly to hashes held securely inside the local Trusted Platform Module (TPM 2.0). The Platform Configuration Registers (PCRs) are checked against the root of trust, preventing side-channel interference or physical extraction of the validation certificates.

## 2. Automated Safe Rollbacks & Deterministic Watchdogs
A mathematical proof of signature does not guarantee a bug-free execution. If a verified patch causes a kernel panic or severs the kinetic control loops, the asset must self-heal instantly.

* **A/B Boot Block Architecture:** Staging updates happens within a strictly isolated A/B root filesystem architecture. The new image is flashed entirely to the inactive partition ($P_{standby}$) while the node operates on the active partition ($P_{active}$). 
* **Sanity Checklist & Watchdog Math:** Upon rebooting into the newly flashed partition, the RT-PREEMPT kernel initializes a dedicated hardware watchdog timer ($t_{wdog}$). The system must execute a local hardware sanity checklist (verifying IOMMU bounds, CAN bus access, and sub-GHz transceiver states) and report a successful boolean initialization vector ($\vec{C}_{init} = \mathbf{1}$) within the strict temporal window:
  $$\Delta t_{boot} \le t_{wdog}$$
* **Instant Kinetic Rollback:** If the new image fails the checklist ($\vec{C}_{init} \neq \mathbf{1}$) or if the kernel hangs causing $\Delta t_{boot} > t_{wdog}$, the hardware watchdog physically resets the CPU. The U-Boot bootloader instantly flips the boot flag, triggering an automated rollback to the stable alternative partition. The corrupted patch is mathematically quarantined, and the node returns to its operational baseline without requiring human intervention.
