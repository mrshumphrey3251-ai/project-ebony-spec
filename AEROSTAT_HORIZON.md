# AEROSTAT_HORIZON: High-Altitude Mesh Relay & Antenna Stabilization

**Classification:** Gated Engineering Documentation / Network Topology Layer
**Target Architecture:** Tethered LTA Platforms / 900 MHz FHSS Transceivers

This specification covers the high-altitude telemetry relay and sightline optimization protocols for persistent elevation nodes (aerostats). When terrain geometry or dense industrial infrastructure severely attenuates ground-level sub-GHz mesh links, the localized fleet deploys aerial relays to guarantee deterministic store-and-forward routing across fractured ground clusters.

## 1. Line-of-Sight (LoS) Data Relays & Asymmetric Bridging
The aerostat node acts as the apex router in the decentralized Directed Acyclic Graph (DAG) topology (as defined in `FRACTURED_MESH_ROUTING.md`).

* **Fresnel Zone Clearance:** By elevating the transceiver, the node physically clears the primary Fresnel zone of ground obstacles. The absolute RF line-of-sight horizon distance $d$ (in kilometers) is maximized based on the physical elevation of the aerial ($h_1$) and ground ($h_2$) antennas (in meters):
  $$d \approx 3.57 \left( \sqrt{h_1} + \sqrt{h_2} \right)$$
* **Telemetry Aggregation:** The aerial node ingests low-power, high-spread-factor LoRa beacons from isolated field relays. It repackages these fragmented payloads into strictly bit-packed FlatBuffer schemas (`FLATBUFFER_SERIALIZATION.md`), caching them in localized solid-state storage before executing high-throughput FSK down-link bursts to connected sectors.

## 2. Environmental Stabilization & IMU Compensation
High-altitude nodes are subject to severe environmental turbulence and wind shear, which can misalign high-gain directional antennas and abruptly sever the physical RF link.

* **Yaw/Pitch/Roll Monitoring:** A dedicated 9-axis Inertial Measurement Unit (IMU) continuously monitors the physical posture of the aerial platform.
* **Closed-Loop Gimbal Actuation:** Native C++ stabilization modules ingest the IMU telemetry at $200 \text{ Hz}$. If the platform deviates from its target vector, the RT-PREEMPT kernel calculates the required counter-rotations and injects synchronized PWM signals into the payload gimbals. This closed-loop compensation guarantees the directional antenna arrays remain precisely locked onto the ground-fleet's azimuth, regardless of atmospheric volatility.
