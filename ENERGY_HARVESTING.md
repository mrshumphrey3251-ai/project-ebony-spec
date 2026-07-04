# ENERGY_HARVESTING: Microgrid Ingestion & MPPT Conditioning

**Classification:** Gated Engineering Documentation / Power-State Management Layer
**Target Architecture:** Multi-Source DC Bus / Jetson Power Bounding / RT-PREEMPT

This specification handles the multi-source energy ingestion, Maximum Power Point Tracking (MPPT), and dynamic power routing layers for off-grid edge hardware. Project Ebony nodes are expected to operate in fully decentralized, zero-logistics environments. The system must autonomously harvest, condition, and route heterogeneous energy sources natively, mathematically guaranteeing the survival of the primary RT-PREEMPT compute loop under extreme environmental starvation.

## 1. Heterogeneous Energy Harvesting & MPPT Compute
Ambient energy sources are highly volatile and non-linear. The local node must ingest these varying voltage curves and force them into a unified, clean distribution rail.

* **Multi-Input Microgrid Ingestion:** The architecture interconnects solar photovoltaic arrays, micro-hydro turbines, and Thermoelectric Generators (TEGs) into a unified, galvanically isolated DC distribution layer. Each energy source is bound to a dedicated hardware buck-boost converter.
* **Local MPPT Modulation Compute:** To maximize energy extraction, the local C++ runtime executes high-frequency perturb-and-observe MPPT algorithms natively. The system tracks the instantaneous power ($P(v) = v \cdot i$) of the incoming array and continuously calculates the exact power derivative against the voltage change:
  $$\frac{dP}{dv} = i + v \frac{di}{dv}$$
* **PWM Execution Loop:** When $\frac{dP}{dv} \neq 0$, the RT-PREEMPT kernel dynamically adjusts the duty cycle ($D$) of the hardware Pulse-Width Modulation (PWM) controllers to force the equation to zero (the absolute maximum power point). For a localized buck converter routing solar power to the main rail, the output voltage ($V_{out}$) is deterministically held stable despite cloud cover or shading:
  $$V_{out} = D \cdot V_{in}(t)$$
  This loop runs at $10 \text{ kHz}$, instantly adjusting the physical energy extraction curves without requiring cloud telemetry analysis.

## 2. Dynamic Power Partition Routing
During severe low-harvest intervals (e.g., prolonged darkness or kinetic structural damage), the energy ingested will fail to meet the total system draw. The node must autonomously cannibalize its own auxiliary functions to keep the core OS alive.

* **Deterministic Load Shedding:** The local node models its internal power consumption as a linear optimization problem. The system automatically routes energy directly to essential computation blocks (Jetson CPU/IOMMU) and critical environmental survival layers (CBRN filtration or battery thermal blankets).
* **Objective Function Bounding:** The node dynamically cuts off auxiliary loads (e.g., optical training matrices or high-torque mechanical actuators) by maximizing the survival time ($T_{survival}$) based on the current available power ($P_{avail}$):
  $$\text{Maximize} \quad T_{survival} = \frac{E_{battery}}{\sum_{j \in \mathbb{C}} P_j - P_{avail}}$$
  *(Where $E_{battery}$ is the localized reserve capacity calculated in `BATTERY_MONITORING.md`, and $\mathbb{C}$ is the strict set of critical survival systems).* If $P_{avail}$ drops below the baseline, the hardware watchdogs instantly sever the power rails to non-essential loads, mathematically preventing a localized brownout and preserving the cryptographic ledgers.
