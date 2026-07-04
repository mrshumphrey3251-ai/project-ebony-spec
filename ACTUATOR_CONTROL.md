# ACTUATOR_CONTROL: J1939 CAN Bus, Modbus RTU & Closed-Loop Modulation

**Classification:** Gated Engineering Documentation / Cyber-Physical Control Layer
**Target Architecture:** Electro-Hydraulic Pilot Valves / Solid-State SCADA Relays

This specification handles the deterministic translation of edge-intelligence directives into physical electromechanical work. Project Ebony bypasses abstracted, cloud-dependent machine controllers to interface natively with the primary hardware buses, guaranteeing absolute operational sovereignty.

## 1. Physical Bus Interfacing & Deterministic Limits
The runtime does not rely on high-level APIs to move machinery. It constructs and injects raw hexadecimal frames directly into the physical infrastructure.

* **Supported Topologies:** * **J1939 CAN Bus (ISO 11898):** Primary interface for engine control units (ECUs) and hydraulic manifold controllers.
  * **Modbus RTU (RS-485):** Secondary interface for legacy industrial sensors and heavy-duty serial telemetry.
  * **Solid-State SCADA Relays:** Direct GPIO manipulation for localized unmaskable interrupts and hard-kill switches.
* **Execution Jitter Constraints:** Core control loops execute inside highly prioritized real-time boundaries. By pinning the C++ injection threads to the `SCHED_FIFO` policy on the RT-PREEMPT Linux kernel, the system guarantees a scheduling jitter of $< 1 \text{ ms}$, ensuring perfectly synchronized physical movements.

## 2. Active Mechanical Posture & PID Loop Processing
To maintain fluid, precise mechanical actuations under heavy dynamic loads (e.g., changing soil densities, hydraulic pressure drops), the node utilizes local closed-loop modulation.

* **Native C++ Processing:** Hardened C++ modules ingest local pressure, temperature, and fluid telemetry straight off the bus. 
* **The PID Algorithm:** Micro-adjustments are calculated natively at $100 \text{ Hz}$ using a continuous-time Proportional-Integral-Derivative (PID) control algorithm to minimize actuator error:
  $$u(t) = K_p e(t) + K_i \int_0^t e(\tau) d\tau + K_d \frac{de(t)}{dt}$$
  *(Where $u(t)$ is the control signal sent to the pilot valve, and $e(t)$ is the calculated error between the targeted spatial coordinate and the current physical state).*

## 3. Hardware Watchdogs & Mechanical Fail-Safes
Physical safety strictly supersedes software instruction. If the cryptographic perimeter is breached, or the active mechanical posture fails sanity checks:

* **Hardware Heartbeats:** Independent, localized hardware watchdogs continuously listen for system heartbeats from the primary execution thread. 
* **Spring-Return Severance:** If the primary software loop encounters a segmentation fault, misses a $< 1 \text{ ms}$ deadline, or triggers an exception, the watchdog instantly drops voltage to the solid-state relays. Actuators automatically snap back to their hardcoded, spring-return mechanical safe-states (locking tracks and dropping implements) without requiring software intervention.
