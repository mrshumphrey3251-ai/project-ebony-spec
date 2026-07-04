# PROJECT_EBONY: Hardware Directive & Register-Level Access Specification

**Document Version:** 1.0.3 (2026 Release Track)
**Classification:** Gated Engineering Documentation / Hardware Abstraction Layer (HAL)
**Target Architecture:** NVIDIA Jetson Orin NX 

This specification defines the low-level hardware abstraction layers (HAL), safe register write sequences, direct memory access (DMA) safeguards, and kernel-level device limitations required to protect physical computing blocks. To guarantee operational sovereignty, the edge node strictly enforces physical isolation between application logic and raw silicon.

---

## 1. Direct Memory Mapping Safeguards & DMA Isolation

When dealing with high-speed sensor ingestion (I2S audio arrays, CAN bus vehicle streams, and thermal optics), user-space applications must never have unrestricted access to physical memory addresses. Project Ebony enforces a hard mathematical boundary between application logic and physical memory registers.

### Phase A: Memory Protection Enclaves (IOMMU Routing)
* **Direct Memory Access (DMA) Restraints:** The system utilizes the hardware Input-Output Memory Management Unit (IOMMU) to create strict memory protection enclaves. Native C++ device drivers are restricted to specific, pre-allocated physical memory ranges ($\mathbb{P}_{valid}$).
* **Address Validation Math:** For any virtual address ($V_A$) requested by an application thread, the IOMMU maps it to a physical address ($P_A$). The hardware allows the execution if and only if the mapped address falls strictly within the pre-allocated base and limit bounds:
  $$P_A \in [P_{base}, P_{limit}]$$
* **Buffer Overflow Defense & Hardware Isolation:** If an application thread (such as the TensorRT-LLM engine or Whisper-v3 ASR parser) attempts a malicious or accidental pointer write resulting in $P_A \notin \mathbb{P}_{valid}$, the kernel’s memory management subsystem intercepts the instruction natively. Instead of triggering a global kernel panic, the system violently drops the offending thread, preserving absolute stability on the primary hardware buses.

### Phase B: Kernel Device Access Restraints (cgroups v2)
Project Ebony explicitly blocks user-space applications from directly opening, reading, or writing to raw hardware interfaces (e.g., `/dev/mem`). All hardware communication paths are strictly mediated by Linux kernel control groups (`cgroups v2` device controllers). 

Physical serial and audio lines (such as I2S pins, SPI interfaces for the TPM, and internal UART lanes) are isolated using hard device-whitelisting rules:

```text
[User-Space Application Thread]
       │
       ▼ (Tries to access raw hardware device)
[cgroups v2 Device Filter] ───► REJECTED (If not explicitly whitelisted)
       │
       ▼ (Validated Node Only)
[Kernel Device Driver]
       │
       ▼ (Safe Controlled Execution)
[Physical Hardware Pin]
