# SUB_GHZ_RADIO_PROTOCOL: Physical RF Modulation & Mesh Baseband

**Classification:** Gated Engineering Documentation / Physical Network Layer
**Target Architecture:** 900 MHz ISM Band / LoRa & FSK Hybrid Modulation

This specification defines the bare-metal radio frequency (RF) mechanics used by Project Ebony to maintain deterministic state synchronization when primary cellular (Private 5G/LTE) interfaces suffer catastrophic link failure. The system operates strictly within the sub-GHz spectrum to maximize penetration through heavy industrial infrastructure and dense foliage.

## 1. Hybrid Modulation Strategy
To balance the extreme range of LoRa with the higher throughput requirements of local actuator synchronization, the physical MAC layer actively switches modulation schemes based on instantaneous Received Signal Strength Indicator (RSSI) and Signal-to-Noise Ratio (SNR).

* **FSK (Frequency-Shift Keying):** Utilized for close-proximity ( $< 1 \text{ km}$ ), line-of-sight synchronization. Yields deterministic latency ( $< 20 \text{ ms}$ ) at $250 \text{ kbps}$.
* **LoRa (Long Range Spread Spectrum):** Utilized for deep-penetration, non-line-of-sight telemetry (up to $15 \text{ km}$ ). Operates with high spreading factors (SF9-SF12) to decode signals below the noise floor, mathematically bounded by the Shannon-Hartley theorem for bandwidth constraints:
  $$C = B \log_2\left(1 + \frac{S}{N}\right)$$

## 2. Frequency Hopping & Interference Mitigation
Industrial environments are highly contested RF zones. To prevent malicious jamming and mitigate multipath fading from moving heavy machinery, the node utilizes a synchronized Frequency Hopping Spread Spectrum (FHSS).

* **Hop Synchronization:** The mesh cycles through 50 discrete channels within the 902–928 MHz band.
* **Deterministic Dwell Time:** The radio transceivers (e.g., Semtech SX1262) remain on a specific frequency for exactly $400 \text{ ms}$ before executing a synchronized microsecond hop. The hop sequence is seeded by the current ML-KEM cryptographic epoch (see `POST_QUANTUM_CRYPTO.md`), making the pattern entirely unpredictable to external listeners.

## 3. Hardware-Enforced Duty Cycles
To comply with FCC Part 15 regulations and prevent network flooding, the physical transceiver is hard-coded with a 1% transmission duty cycle constraint. Software cannot override this limit, forcing the application layer to aggressively compress payloads.
# FLATBUFFER_SERIALIZATION: Zero-Copy Telemetry & Data Packing

**Classification:** Gated Engineering Documentation / Memory Management Layer
**Target Architecture:** C++ FFI / Dart Deterministic Runtime

Because the `SUB_GHZ_RADIO_PROTOCOL` enforces severe bandwidth and duty-cycle limitations, traditional web-native serialization (JSON, XML, or even standard Protocol Buffers) is fundamentally incompatible with the edge node. Parsing string-heavy payloads introduces unpredictable memory allocation and garbage collection (GC) pauses.

## 1. Zero-Copy FlatBuffers Integration
Project Ebony utilizes strictly defined Google FlatBuffers for all internal state and mesh telemetry. 

* **Direct Memory Mapping:** FlatBuffers allow the C++ runtime to access serialized data directly from the physical network buffer without parsing, unpacking, or allocating new memory on the heap. 
* **Latency Guarantee:** Bypassing the parsing step eliminates GC latency spikes, guaranteeing that deserialization takes $\mathcal{O}(1)$ time (constant time) regardless of payload complexity.

## 2. Payload Compression & Bit-Packing
Every byte transmitted over the sub-GHz radio costs battery power and consumes duty-cycle time. Telemetry is aggressively bit-packed into fixed-width structs.

| Data Field | Legacy Size (JSON) | Ebony Size (FlatBuffer) | Reduction Technique |
| :--- | :--- | :--- | :--- |
| **GPS Coordinates** | ~35 bytes (String) | 8 bytes | `int32` fixed-point multiplication (1e7) |
| **Actuator State** | ~15 bytes (String) | 1 byte | Bit-field masking (`uint8_t`) |
| **Timestamp** | ~24 bytes (ISO8601) | 4 bytes | Unix epoch offset (`uint32_t`) |
| **Cryptographic Hash** | 64 bytes (Hex String) | 32 bytes | Raw binary `[32]byte` array |

## 3. Deterministic Over-the-Air (OTA) Updates
Firmware patches are split into $256 \text{-byte}$ deterministic chunks. The FlatBuffer schema includes offset pointers and a localized CRC32 checksum for each chunk, allowing the mesh nodes to slowly rebuild firmware images over several hours of background radio traffic without disrupting real-time machine control.
# FRACTURED_MESH_ROUTING: Split-Brain Healing & Node Discovery

**Classification:** Gated Engineering Documentation / Network Topology Layer
**Target Architecture:** Decentralized Directed Acyclic Graph (DAG)

When the primary telecom infrastructure drops, the fleet fractures into isolated geographic pockets. Project Ebony does not rely on a central master node for mesh routing. The network is fundamentally leaderless and highly anti-fragile.

## 1. Autonomous Node Discovery
When a node detects a macro-network failure, it immediately drops into "Hunter" mode.

* **Beaconing Protocol:** The node broadcasts a $16 \text{-byte}$ compressed FlatBuffer beacon on the sub-GHz FHSS sequence.
* **RSSI Triangulation:** Neighboring nodes receive the beacon and log the physical MAC address, RSSI, and SNR into a local routing table. 
* **Dynamic Topology:** The topology is constantly rebuilt as heavy machinery moves across the operating zone. Stale nodes are pruned from the local routing table if no beacon is received within $300 \text{ seconds}$.

## 2. Store-and-Forward Mechanics
If Node A needs to synchronize state with Node D, but they are out of physical RF range, the network utilizes automated store-and-forward gossiping.

* **Hop Bounding:** Each FlatBuffer payload is assigned a Time-To-Live (TTL) integer (max 4 hops) to prevent infinite routing loops. 
* **Asynchronous Relay:** Node B caches the encrypted payload in its local NVMe storage. When Node B physically drives within range of Node C or Node D, the payload is automatically flushed across the radio link.

## 3. Split-Brain Convergence
When two previously isolated pockets of the mesh network physically reconnect (e.g., two fleets of autonomous tractors converge in the same sector), the disparate state ledgers will conflict. 

* Execution is handed off directly to the mathematical conflict resolution logic defined in `CRDT_MERGE_MECHANIC.md`. The nodes compare their Merkle tree root hashes, exchange missing state chunks, and deterministically converge on a single version of operational truth without human intervention.
