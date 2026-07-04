# HARDWARE_DIRECTIVE: Register Access & IOMMU Enclaves

**Classification:** Gated Engineering Documentation / Base Hardware Abstraction Layer
**Target Architecture:** IOMMU / Linux `cgroup` v2 / Physical Registers

This file outlines the low-level hardware abstraction layers, safe register write sequences, and kernel-level cgroup device limits. Project Ebony assets rely on absolute hardware determinism. The system must mathematically guarantee that user-space software, ML inference loops, and standard OS applications cannot bypass the kernel to arbitrarily manipulate physical hardware registers or execute un-bound memory sweeps.

## 1. Direct Memory Mapping Safe Guards (IOMMU)
Allowing native C++ drivers to map physical memory directly introduces severe security vulnerabilities. The hardware architecture must enforce strict boundaries before translating virtual addresses to physical silicon.

* **Memory Protection Enclaves:** The system enforces strict memory boundaries utilizing the hardware IOMMU. The kernel intercepts all Direct Memory Access (DMA) requests from peripheral devices. The native virtual address ($V_{addr}$) must be mathematically verified against the strictly allocated page table ($P_{table}$) before physical translation is authorized:
  $$P_{addr} = \text{IOMMU\_Translate}(V_{addr}, P_{table})$$
  If a corrupted driver or malicious peripheral attempts to read or write a physical memory line outside its mathematically assigned bound ($V_{addr} \notin P_{table}$), the IOMMU hardware triggers an instantaneous bus fault, terminating the process natively and protecting the physical memory lines from access violations.
* **Kernel Resource Restraints (BPF/cgroups):** The node limits direct access to physical serial interfaces (SPI, I2C, CAN) using strict Linux kernel `cgroups` v2. The system attaches an eBPF (Extended Berkeley Packet Filter) program to the device control slice. The execution loop mathematically isolates device resources, ensuring that a user-space application thread ($T_u$) is strictly bounded:
  $$\text{Access}(T_u, \text{Device}) = \begin{cases} \text{Permit}, & \text{if } T_u \in G_{authorized} \\ \text{Deny}, & \text{otherwise} \end{cases}$$
  This physically severs unauthorized user-space applications from accessing critical hardware buses.

## 2. Hardwired Diagnostics Tracking & Ring Buffers
A compromised kernel or a sudden power loss can wipe volatile syslog data, masking the root cause of a catastrophic hardware failure. Low-level device health must be audited entirely independent of the main OS.

* **Dedicated Out-of-Band Memory:** The architecture logs low-level hardware event metrics (e.g., CPU thermal throttling vectors, bus fault interrupts, and IOMMU violation counts) directly to dedicated, independent non-volatile memory blocks (SPI NOR flash).
* **Deterministic Write Logging:** To prevent the storage medium from wearing out or halting the main execution loops during a flood of hardware faults, the logging daemon executes as a strict circular ring buffer. The mathematical pointer ($P_{write}$) overwrites the oldest diagnostic block ($B_i$) with $O(1)$ time complexity:
  $$P_{write} = (P_{write} + 1) \pmod{N_{blocks}}$$
  This enables independent, post-mortem device health audits that survive complete catastrophic kernel panics or primary NVMe drive failures.
