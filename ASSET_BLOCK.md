# ASSET_BLOCK_ISOLATION: Cryptographic Quarantine & Mechanical Interlock

**Classification:** Gated Engineering Documentation / Threat Mitigation Layer
**Target Architecture:** Sub-GHz DAG Mesh / Solid-State Interlocks

This specification outlines the localized cryptographic quarantine and logical sever sequences used to immediately disable compromised hardware modules. Project Ebony operates under strict zero-trust parameters; if a node begins broadcasting anomalous telemetry or fails its localized hardware attestation, the mesh network autonomously excises it without waiting for WAN intervention or remote command.

## 1. Distributed Cryptographic Quarantine (Node Revocation Arrays)
If a peer node detects physical tampering, irregular execution jitter, or invalid cryptographic signatures, it immediately broadcasts a high-priority revocation beacon over the 900 MHz FHSS link.

* **Byzantine Fault Tolerant (BFT) Consensus:** The local sub-GHz radio mesh utilizes a decentralized consensus algorithm to quarantine the rogue asset. The local fleet successfully isolates the target node provided the number of malicious or compromised nodes ($f$) does not exceed the mathematical Byzantine threshold of the total local peers ($N$):
  $$f \le \left\lfloor \frac{N-1}{3} \right\rfloor$$
* **Epoch Eviction:** Once consensus is reached, all neighboring nodes immediately drop the compromised node's public key from the active ML-KEM cryptographic epoch. Any further FlatBuffer packets transmitted by the isolated node are dropped directly at the physical MAC layer, completely deafening it to the rest of the fleet.

## 2. Localized Ephemeral Purge & Storage Severance
Simultaneous to the external mesh revocation, if the compromised node's internal watchdog detects a perimeter breach or a `cgroups` execution violation, it triggers a self-contained quarantine.

* **Volatile Memory Scrub:** The memory controller executes a hardware-level Direct Memory Access (DMA) purge, overwriting all active runtime registers, state ledgers, and ML-KEM session keys in RAM with cryptographic noise.
* **LUKS2 Drive Unmount:** The RT-PREEMPT kernel violently unmounts the primary LUKS2 NVMe storage partitions. The TPM 2.0 module receives a hardware reset command, instantly flushing the decryption keys from its Platform Configuration Registers (PCRs). The node is rendered logically inert, with its storage mathematically sealed.

## 3. Mechanical Interlock Engagement
An isolated, deafened node cannot be permitted to maintain physical authority over kinetic machinery.

* **ECU & Actuator Drop:** The digital execution loops immediately halt all J1939 CAN bus PGN injections. 
* **Galvanic Disconnect:** Following the protocols defined in `ANALOG_OVERRIDE.md`, the local hardware watchdog drops voltage to the primary solid-state SCADA relays. Downstream Engine Control Units (ECUs) and electro-hydraulic proportional valves are instantly severed from the digital core, forcing all heavy machinery directly into a hardened, spring-return mechanical safe-state (brakes locked, implements grounded).
