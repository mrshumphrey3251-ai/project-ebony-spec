# SECURE_BOOT: Hardware Root of Trust & Cryptographic Bootchain Specification

**Classification:** Gated Engineering Documentation / Cryptographic Bedrock
**Target Architecture:** NVIDIA Jetson Orin NX (ARM64) / FIPS-Compliant Offline Nodes

This specification defines the multi-stage hardware verification sequences, cryptographic partition validation, and TPM-bound measurement routines required for first-stage execution. Project Ebony rejects software-only security paradigms; absolute operational sovereignty requires an unbroken chain of trust anchored directly into the physical silicon.

## 1. Cryptographic Chain-of-Trust

The boot sequence follows a strict hardware-gated progression. If any stage fails cryptographic validation, execution halts immediately.

```text
[Physical Silicon: eFuses] 
       │ 
       ▼ (Validates SHA-3072 Signature) 
[First-Stage Boot ROM & UEFI] 
       │ 
       ▼ (Measures Hashes into PCRs) 
[Discrete Hardware: TPM 2.0] 
       │ 
       ▼ (Releases Decryption Key via SPI Bus) 
[Encrypted Storage: LUKS2 NVMe]# Project Ebony: Secure Boot & Hardware Root of Trust Specification
Document Version: 1.0.2 (2026 Release Track)
Classification: Gated Engineering Documentation / Cryptographic Bedrock

This specification defines the multi-stage hardware verification sequences, cryptographic partition validation, and TPM-bound measurement routines required for first-stage execution on the NVIDIA Jetson Orin NX architecture.

---

## 1. Cryptographic Chain-of-Trust Validation

Project Ebony rejects all software-only security paradigms. Absolute operational sovereignty requires an unbroken chain of trust anchored directly into the physical silicon of the node.

[Physical Silicon: eFuses]
│
▼ (Validates Signature)
[First-Stage Bootloader: UEFI]
│
▼ (Measures Hashes into PCRs)
[Trusted Platform Module: TPM 2.0]
│
▼ (Releases Decryption Key)
[Encrypted Storage: LUKS2 NVMe]


### Phase A: Hardware Boot ROM Anchoring (The Genesis Seal)
1. **The Public Key Hash (PKH):** During the initial factory provisioning phase, the operator's SHA-3072 cryptographic public key hash is permanently burned into the physical programmable fuses (**eFuses**) of the Jetson Orin NX processor.
2. **First-Stage Interception Block:** When power hits the board, the hardcoded, un-writable On-Chip Boot ROM initializes first. Before it executes a single line of the primary bootloader (UEFI), it hashes the bootloader binary and compares it directly to the fused keys.
3. **Hardware Lockout:** If the signatures do not match perfectly—indicating a supply-chain interception or localized hardware tampering—the processor immediately executes a hardware-level execution halt. The system refuses to boot.

### Phase B: Measured Boot Verification (PCR Logging)
1. Once the primary bootloader passes the physical eFuse verification, it assumes control and initializes the discrete **TPM 2.0 chip** over the SPI bus.
2. The bootloader scans the kernel image, the device tree blobs (hardware configurations), and the initial RAM disk (initramfs) before execution.
3. It generates cryptographic SHA-256 hashes of these components and "extends" them into the TPM’s **Platform Configuration Registers (PCRs)**—specifically targeting **PCR 0, 4, and 5**. 
4. This creates an un-falsifiable historical record of the exact state of the software at the moment of boot.

---

## 2. Partition Mounting & Storage Lockouts

The system will not trust its own storage drive until the hardware registers prove the operating system has not been modified.

### Phase C: The TPM 2.0 State Resealing Handshake
1. The primary storage architecture of Project Ebony relies on a high-speed PCIe Gen4 x4 NVMe M.2 SSD formatted with **LUKS2 full-disk encryption**.
2. The pass-phrase required to decrypt this NVMe storage volume is **sealed** natively inside the TPM 2.0 secure storage index.
3. **The Enforcement Rule:** The TPM will only release the decryption passphrase if, and only if, the current values inside PCR 0, 4, and 5 exactly match the frozen, signed engineering baseline.

### Phase D: Tamper Lockout Cascade
If an adversary removes the NVMe storage drive to read its contents on an unauthorized machine, or if they attempt to modify the early boot scripts on the drive, the system executes an automated lockout cascade:
* The kernel hash changes due to the modifications.
* The bootloader attempts to extend this incorrect hash into the TPM registers.
* The TPM detects that the current PCR state does not match the frozen baseline profile.
* **The Result:** The TPM permanently locks the storage index and refuses to release the LUKS2 decryption key. The operating system fails to mount, leaving the entire NVMe storage block looking like randomized, mathematically unbreakable noise.

---

## 3. Post-Boot Runtime Separation (cgroups Isolation)

Once the core operating engine successfully decrypts and initializes, it immediately segregates the hardware resources using kernel-level control groups (**cgroups v2**). This guarantees that a sudden spike in heavy AI workloads can never starve critical vehicle control or sensor buses.

| Resource Pool | Target Components | Allocation Constraints | Scheduling Priority |
| :--- | :--- | :--- | :--- |
| **Pool Alpha (System Core)** | MAVLink, J1939 CAN Bus, Modbus RTU, I2S Audio | 2 Dedicated CPU Cores / 2GB RAM / 0% GPU | Real-Time (`SCHED_FIFO`) |
| **Pool Beta (Cognitive Layer)** | TensorRT-LLM, Whisper-v3 local ASR streams | 4 CPU Cores / 12GB RAM / 100% DLA & GPU | Standard Batch (`SCHED_OTHER`) |
| **Pool Gamma (Mesh Mesh)** | Sub-GHz Radio Stack, FlatBuffer Handshakes | 2 CPU Cores / 2GB RAM / 0% GPU | High-Priority I/O |

If Pool Beta (the local AI models) hits 100% utilization during a heavy targeting or tracking sequence, the Linux kernel violently throttles the training and inference threads via these hard boundaries. The primary vehicle flight controllers, actuator lines, and mesh radios continue to execute with sub-millisecond determinism.

