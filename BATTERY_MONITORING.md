# BATTERY_MONITORING: Coulomb Tracking & Deterministic SoH Telemetry

**Classification:** Gated Engineering Documentation / Power-State Management Layer
**Target Architecture:** 24-Bit ADC Current Shunts / RT-PREEMPT Kernel

This specification handles the continuous telemetry logging of voltage, current, State of Charge (SoC), and State of Health (SoH) metrics. Project Ebony assets operate autonomously in isolated environments where a sudden power loss during a kinetic operation is a catastrophic failure. Power reserves are calculated deterministically on the edge silicon, rejecting estimated voltage-curve approximations.

## 1. High-Precision State of Charge (SoC) & Coulomb Counting
Heavy electromechanical workloads introduce severe voltage sag, rendering standard voltage-based capacity readings dangerously inaccurate. The system tracks absolute energy flow via hardware shunts.

* **Hardware Shunt Ingestion:** A dedicated 24-bit Analog-to-Digital Converter (ADC) polls the primary DC bus current shunt at $1000 \text{ Hz}$. 
* **Native Integral Calculus:** The RT-PREEMPT kernel calculates the exact State of Charge natively by continuously integrating the instantaneous current draw $I(\tau)$ over time:
  $$SoC(t) = SoC(0) - \frac{1}{C_{max}} \int_{0}^{t} I(\tau) d\tau$$
  *(Where $C_{max}$ is the absolute maximum Ah capacity of the array, and $I(\tau)$ is negative during discharge and positive during regenerative states).* This guarantees a mathematically perfect local SoC map regardless of transient load spikes.

## 2. Transient Impedance & State of Health (SoH)
Lithium arrays degrade physically over time. The node autonomously tracks its own hardware degradation to prevent deploying on a mission it lacks the internal chemistry to complete.

* **Cell Impedance Calculations:** During peak actuator loads (e.g., dead-starting a hydraulic pump), the C++ runtime captures the exact microsecond voltage drop ($\Delta V$) against the current spike ($\Delta I$).
* **Continuous SoH Mapping:** The internal cell resistance $R_{int}$ is calculated continuously:
  $$R_{int} = \frac{\Delta V}{\Delta I}$$
  As $R_{int}$ increases over the asset's lifecycle, the system dynamically updates its internal State of Health (SoH) metrics, actively reducing its maximum authorized operational range to compensate for chemical aging.

## 3. Low-Voltage Fault Protection & Cryptographic Safe-Shutdown
If the localized energy reserve breaches the point of no return, the system prioritizes cryptographic and mechanical integrity over continued operation.

* **Reserve Margin Thresholds:** When the continuously calculated $SoC(t)$ drops below the localized "Return-to-Base" margin, the node drops non-essential workloads (see `BATTERY_MITIGATION.md`).
* **Mesh Alerting & Clean Severance:** If the SoC breaches the absolute critical threshold, the node broadcasts a high-priority `0x00` FlatBuffer alert across the sub-GHz DAG mesh. The OS then instantly executes a `sync` command to flush all telemetry out of volatile RAM, aggressively unmounts the primary LUKS2 NVMe partitions, and drops the TPM 2.0 PCR keys before the analog power rails physically brown out.
