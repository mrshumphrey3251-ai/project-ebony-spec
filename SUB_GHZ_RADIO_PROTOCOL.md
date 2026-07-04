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
