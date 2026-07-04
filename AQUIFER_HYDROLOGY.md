# AQUIFER_HYDROLOGY: Hydrostatic Telemetry & Subsurface Depletion Modeling

**Classification:** Gated Engineering Documentation / Environmental Telemetry Layer
**Target Architecture:** RS-485 Modbus RTU / RT-PREEMPT Kernel

This specification details the telemetry harvesting protocols for subsurface water reserves, hydrostatic pressure mapping, and localized extraction controls. Project Ebony treats critical resource management as a localized physics problem; all hydrological modeling and pump orchestration must execute natively on the edge to prevent environmental collapse caused by WAN latency or cloud API outages.

## 1. Hydrostatic Telemetry Ingestion & Piezometer Interfacing
The edge node continuously monitors subterranean fluid dynamics via direct hardwired connections, completely bypassing OEM telematics gateways.

* **Subterranean Sensor Interfaces:** The system gathers raw hydrostatic head data, volumetric flow rates, and fluid temperature metrics from deep-well piezometers and submersible pressure transducers.
* **Modbus RTU Polling:** This sensor data is ingested via an isolated RS-485 Modbus network. The native C++ execution threads poll these serial registers at a deterministic interval ($10 \text{ Hz}$), guaranteeing highly granular, real-time awareness of the localized water table.

## 2. Local Inflow Analysis & Drawdown Compute
Cloud-based models rely on historical estimation. Project Ebony computes localized replenishment metrics and depletion curves dynamically on the Jetson Orin's CPU.

* **Dynamic Drawdown Mapping:** The node tracks the localized drawdown $s(t)$, which is the difference between the static, undisturbed hydraulic head ($h_0$) and the dynamic pumping level ($h(t)$). 
* **Depletion Curve Calculation:** To prevent over-extraction, the C++ runtime calculates the rate of head change natively:
  $$\frac{ds}{dt} = \frac{d}{dt} \left( \frac{P_{static} - P_{dynamic}}{\rho g} \right)$$
  *(Where $P$ is the transducer pressure, $\rho$ is fluid density, and $g$ is gravitational acceleration).* By constantly computing this derivative, the node maps the exact localized aquifer replenishment curve in real-time, plotting extraction rates directly against the physical inflow physics.

## 3. Resource Containment & Actuator Throttling
If the localized compute model detects that extraction is outpacing the natural geological inflow, the system enforces absolute hardware containment.

* **Algorithmic Pump Throttling:** As $\frac{ds}{dt}$ approaches the predefined maximum safe drawdown limit ($s_{max}$), the PID algorithms (defined in `ACTUATOR_CONTROL.md`) step down the Variable Frequency Drives (VFDs) controlling the extraction pumps, dynamically matching the extraction rate to the physical replenishment rate.
* **Mechanical Hard-Kill Protocols:** If the drawdown curve breaches the absolute bottom-hole safety margin, or if the sensor array detects cavitation (air ingestion), the RT-PREEMPT kernel bypasses the VFDs and triggers the local SCADA relays. Extraction pumps are mechanically severed from the power rail instantly, executing a hard shutoff to protect the subterranean geology and the physical pumping hardware.
