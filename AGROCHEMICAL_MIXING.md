# AGROCHEMICAL_MIXING: Fluid Telemetry & Deterministic Ratio Orchestration

**Classification:** Gated Engineering Documentation / Cyber-Physical Control Layer
**Target Architecture:** Modbus RTU (RS-485) / Proportional Valves / SCADA Relays

This specification dictates the automated telemetry, ratio compliance, and deterministic valve orchestration for fluid chemical operations. Project Ebony enforces strictly bounded, air-gapped fluid management, removing human error, network latency, and cloud-dependency from volatile agrochemical mixing cycles.

## 1. Automated Ratio Enforcement & Volumetric Compute
The system rejects time-based estimation for chemical mixing. All fluid exchanges are measured deterministically via closed-loop sensor ingestion.

* **Flow Meter Ingestion:** Real-time pulse monitoring of high-resolution digital flow sensors computes the precise volumetric exchange of liquids through dedicated manifold paths. 
* **Native Flow Processing:** The volumetric flow rate $Q$ is calculated directly on the edge silicon based on the raw sensor pulse frequency $f$ and the hardware K-factor $K$:
  $$Q = \frac{f}{K} \times 60$$
  This calculation executes continuously within the RT-PREEMPT kernel, guaranteeing real-time mass-flow awareness without polling delays.
* **Proportional Valve Modulation:** Actuators regulate fluid flow dynamically using isolated Modbus RTU (RS-485) instructions. By applying the closed-loop PID control algorithms (defined in `ACTUATOR_CONTROL.md`), the C++ runtime makes micro-adjustments to the proportional valves, maintaining strict programmatic ratio margins regardless of transient pump pressure variances.

## 2. Contamination Mitigation & Hard-Kill Flush Cascades
Physical fluid operations introduce extreme environmental and hardware risks if a control loop fails or a manifold fractures.

* **Continuous Manifold Telemetry:** Local pressure transducers and inline telemetry sensors monitor the physical integrity of the chemical pathways at $100 \text{ Hz}$.
* **Automated Flush Cascades:** If the telemetry indicates an unexpected manifold pressure drop (suggesting a physical leak), an unauthorized ratio deviation, or a cryptographic cycle abort, the system triggers an immediate unmaskable interrupt.
* **Relay Isolation:** Dedicated secondary solid-state SCADA relays fire instantaneously, executing automated chemical line isolation protocols. The system bypasses the primary software loop, severing active pumping circuits and shifting mechanical valves to a secure, closed-loop flush state to prevent hazardous cross-contamination or unregulated environmental discharge.
