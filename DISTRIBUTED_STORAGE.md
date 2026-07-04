# DISTRIBUTED_STORAGE: Enclave Filesystems & Mesh Replication

**Classification:** Gated Engineering Documentation / Cryptographic Storage Layer
**Target Architecture:** NVMe Flash / LUKS2 (AES-256-XTS) / TPM 2.0

This document details the encrypted local storage blocks, append-only volume configurations, and peer-to-peer file replication mechanics across the edge mesh. Project Ebony nodes possess no reliance on cloud-based databases. Operational state, machine learning models, and system manifests must be preserved natively on the edge silicon, guaranteed against both sudden electro-mechanical power loss and direct physical extraction.

## 1. Encrypted Local Blocks & Hardware Sealing
All persistent storage on the edge node is treated as hostile territory. The operating system kernel is completely blind to the raw physical sectors.

* **LUKS2 Storage Sealing (AES-256-XTS):** All active partitions are locked behind hardware-bound disk encryption. The data is encrypted using the XTS mode, which mitigates block manipulation attacks on the physical flash matrix. For any plaintext block $P_j$, the physical cipher text $C_j$ is computed natively:
  $$C_j = E_K(P_j \oplus T_j) \oplus T_j$$
  *(Where $E_K$ is the AES encryption algorithm utilizing the volume key $K$, and $T_j$ is the cryptographic tweak generated from the physical sector index).*
* **TPM 2.0 Cryptographic Bounding:** The volume key $K$ is never written to disk. It is mathematically sealed inside the physical TPM 2.0 enclave and only released into volatile RAM if the Secure Boot chain (`SECURE_BOOT.md`) perfectly matches the Platform Configuration Registers (PCRs).
* **Flash-Optimized Journaling:** Sudden kinetic failures will drop voltage to the motherboard instantly. The local storage utilizes a strict Copy-on-Write (CoW) and atomic-journaling filesystem (e.g., F2FS). This mathematically guarantees that an interrupted write operation cannot result in a torn sector or corrupted index, ensuring the volume will always mount successfully upon cold-boot.

## 2. Peer Partition Synchronization & Mesh Redundancy
Local storage is inherently vulnerable to total physical destruction (e.g., asset immolation or crushing). Critical operational manifests and localized ML tuning parameters must survive the destruction of a single node.

* **Erasure-Coded File Chunks:** The node does not broadcast entire files over the highly constrained sub-GHz mesh. Instead, it utilizes Reed-Solomon Erasure Coding, $RS(n, k)$, dividing critical data into $k$ encrypted data chunks and generating $m$ parity chunks (where $n = k + m$).
* **Distributed Sub-GHz Replication:** These bit-packed chunks are gossiped across adjacent peer nodes over the 900 MHz FHSS link. 
* **Survivability Compute:** This architecture provides mathematical data redundancy without internet reliance. If the local cluster consists of $N$ nodes, the entire operational manifest can be perfectly reconstructed as long as the number of surviving nodes ($\mathbb{S}$) meets the strict recovery threshold:
  $$\mathbb{S} \ge k$$
  Even if multiple physical assets are simultaneously destroyed in a kinetic event, the remaining decentralized cluster natively reconstructs the destroyed nodes' operational ledgers, seamlessly redistributing the mechanical workloads.
