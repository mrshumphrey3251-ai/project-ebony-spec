# ASYMMETRIC_COMMUNICATION: Burst Transmission & Backpressure Queues

**Classification:** Gated Engineering Documentation / Network Topology Layer
**Target Architecture:** Sub-GHz FHSS Transceivers / RT-PREEMPT Network Stack

This specification details the unidirectional data parsing, burst-transmission arrays, and priority-tiered backpressure loops required for low-bandwidth mesh clusters. Project Ebony nodes operate in environments where physical telemetry ingestion massively outpaces sub-GHz transmission capabilities ($\lambda_{in} \gg \mu_{out}$). The network stack must mathematically guarantee that critical hardware alerts survive extreme network congestion.

## 1. Burst Telemetry Serialization & Asymmetric Duty Cycles
To comply with hardware-enforced duty cycles (see `SUB_GHZ_RADIO_PROTOCOL.md`) and minimize RF signature profiles, nodes spend the vast majority of their operational cycles in a passive, zero-emission listening state.

* **Bit-Packed Framing:** System metrics are aggressively compressed into zero-parse FlatBuffers. This strict binary payload eliminates memory allocation overhead and maximizes the data-to-airtime ratio.
* **Randomized Slotted Transmission:** When a state change requires transmission, the node executes a high-speed burst on a randomized FHSS interval. To mitigate packet collisions across a dense local cluster, the system utilizes a slotted transmission protocol where the probability of a successful, collision-free burst is maximized by dynamically adjusting the transmission probability $p$ based on the estimated number of active neighboring nodes $N$:
  $$P_{success} = Np(1-p)^{N-1}$$
  The C++ runtime dynamically tunes $p$ to maintain optimal channel utilization without saturating the spectrum.

## 2. Priority-Tiered Queueing & Inbound Stream Backpressure
During a split-brain mesh convergence or a mass hardware event, the influx of inbound telemetry can overwhelm local processing queues, leading to Out-Of-Memory (OOM) kernel panics if left unmanaged.

* **Encrypted Ephemeral Caching:** Standard, low-priority telemetry (e.g., ambient temperature shifts, routine GPS waypoints) is cached dynamically into the LUKS2 encrypted NVMe blocks, completely bypassing RAM.
* **Algorithmic Backpressure (RED):** To prevent buffer bloat on the sub-GHz radio interface, the network stack implements a hardware-optimized Random Early Detection (RED) algorithm. As the transmission queue length $Q$ grows, the probability of silently dropping low-priority packets scales deterministically:
  $$P_{drop}(Q) = \begin{cases} 
  0 & \text{if } Q < Q_{min} \\ 
  \frac{Q - Q_{min}}{Q_{max} - Q_{min}} & \text{if } Q_{min} \le Q \le Q_{max} \\ 
  1 & \text{if } Q > Q_{max} 
  \end{cases}$$
  This forces non-critical data to be culled natively at the MAC layer before consuming CPU cycles.

## 3. Hardware Alert Preemption
Critical telemetry cannot be subjected to standard backpressure drops. 

* **OOB (Out-of-Band) Intercepts:** High-priority mechanical alerts (e.g., E-Stop engagements, cryptographic tamper alerts, hydraulic pressure losses) are flagged with a strict `0x00` priority header.
* **Queue Preemption:** The RT-PREEMPT kernel instantly intercepts these flags, freezing the processing of the standard RED queue. The critical payload is immediately pushed to the physical radio transceiver, preempting all other traffic and guaranteeing sub-50ms latency for kinetic safety events.
