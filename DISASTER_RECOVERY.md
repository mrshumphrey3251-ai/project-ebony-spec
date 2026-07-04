# DISASTER_RECOVERY: Cold-State Restoration & Mesh Re-Initialization

**Classification:** Gated Engineering Documentation / Cryptographic Recovery Layer
**Target Architecture:** Air-Gapped Media / TPM 2.0 / Sub-GHz DAG Mesh

This specification handles the localized cold-restore sequences, backup snapshot mount rules, and bare-metal recovery handshakes. Project Ebony fleets operate under zero-trust, zero-connectivity constraints. If a physical compute block suffers catastrophic failure or triggers a `TAMPER_RESPONSE.md` purge, it must be rebuilt locally via strict cryptographic gating, entirely bypassing cloud-based recovery APIs.

## 1. Localized Bare-Metal Restores & Cryptographic Unsealing
A compromised or blank hardware node is mathematically prevented from booting into an operational state until physical trust is re-established locally.

* **Air-Gapped Recovery Media:** The re-initialization sequence mandates a direct, physical hardware connection (via a tamper-evident maintenance port). The U-Boot sequence halts until it mathematically verifies the local operator's biometric token. The system strictly enforces the Cosine Similarity distance ($S_c \ge \tau_{bio}$) as defined in `BIOMETRIC_IDENTITY.md` before authorizing the memory controller to read the external re-flash media.
* **LUKS2 Backup Re-Mounting:** Once the base OS image is flashed, the system must restore its operational configurations. The RT-PREEMPT kernel queries the local TPM 2.0 enclave. If the hardware integrity checks (eFuses and Secure Boot chains) pass, the TPM releases the LUKS2 Volume Key (VK) to natively decrypt the local backup snapshots, returning the physical node to a localized baseline state ($S_{baseline}$).

## 2. Peer-Driven State Sync & CRDT Catch-up
A newly flashed, baseline node possesses outdated environmental and operational telemetry. Permitting it to immediately execute kinetic actions would cause catastrophic physical collisions. 

* **Passive Sub-GHz Query:** The recovered node activates its SDR transceiver in a heavily restricted read-only mode, querying adjacent mesh vertices over the 900 MHz FHSS channel for the current consensus network state map.
* **CRDT State Merging:** The node downloads the missing telemetry deltas ($\Delta S$) from surrounding verified peers. The native C++ runtime rebuilds the local operational ledger by mathematically merging the baseline snapshot with the union of the received delta states via Conflict-free Replicated Data Types (CRDT):
  $$S_{current} = S_{baseline} \sqcup \left( \bigcup_{j=1}^{k} \Delta S_j \right)$$
  *(Where $\sqcup$ represents the associative, commutative merge operator, and $k$ represents the number of verified peer nodes providing state deltas).*
* **Operational Handoff:** The node computes the Merkle root hash of its newly constructed $S_{current}$ ledger. If, and only if, this hash perfectly matches the Byzantine Fault Tolerant (BFT) quorum hash of the local fleet, the RT-PREEMPT kernel lifts the mechanical interlocks, restoring full electro-hydraulic authority to the node.
