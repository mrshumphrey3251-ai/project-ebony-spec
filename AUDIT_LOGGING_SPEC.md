# TAMPER_EVIDENT_AUDIT_LOGGING: Cryptographic Hash Chaining & Hardware Ledgers

**Classification:** Gated Engineering Documentation / Cryptographic Security Layer
**Target Architecture:** TPM 2.0 / SHA-256 Append-Only Ledgers

This specification documents the cryptographically chained, append-only local event log system. Project Ebony fundamentally rejects standard, mutable `syslog` architectures. To guarantee absolute forensic integrity during a post-breach audit, all mechanical overrides, telemetry anomalies, and hardware authorizations must be mathematically sealed to prevent physical or digital tampering.

## 1. Sequential Block Chaining & Cryptographic Links
Every localized system state change is written to an immutable, append-only data structure stored within the LUKS2 encrypted NVMe partition.

* **Cryptographic Event Links:** Each individual log entry ($L_n$) is mathematically fused to the hash of the preceding entry ($H_{n-1}$) along with a deterministic hardware timestamp ($T_n$). The native C++ runtime calculates the new cryptographic block hash using strictly defined algorithms:
  $$H_n = \text{SHA-256}(L_n \parallel H_{n-1} \parallel T_n)$$
* **Hardware-Assisted Signatures:** The Jetson Orin CPU does not hold the signing keys in volatile memory. Log entries are passed to the local TPM 2.0 enclave, where they are instantly signed using the unexportable Attestation Identity Key (AIK). This architecture mathematically prevents an adversary with root OS privileges from retroactively altering or injecting false historical logs.

## 2. Tamper Detection Loops & State Verification
Logging is only effective if the system can autonomously detect a ledger manipulation in real-time.

* **Continuous Audit Daemons:** A dedicated, lightweight verification daemon executes within the highly prioritized `SCHED_FIFO` real-time pool. At deterministic intervals, this daemon hashes the entire active state ledger and verifies the root hash against the secure boot blocks sealed inside the TPM's Platform Configuration Registers (PCRs).
* **Automated Quarantine Triggers:** If the daemon detects an out-of-order log write, a missing sequential hash, or an invalid cryptographic signature, it registers a zero-day structural breach. The local node instantly self-executes the quarantine protocols defined in `ASSET_BLOCK_ISOLATION.md`, dropping its sub-GHz radio beacon and electrically severing the physical actuators before the compromised state can propagate to the physical fleet.
