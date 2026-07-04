# BIOSECURITY_TRIAGE: Automated Zone Isolation & Atmospheric Containment

**Classification:** Gated Engineering Documentation / Threat Mitigation Layer
**Target Architecture:** HVAC SCADA Relays / Modbus RTU / Sub-GHz Mesh

This specification outlines the localized containment protocols, airlock state tracking, and environmental sealing cascades for agricultural or site biological anomalies. Project Ebony operates under the assumption that wide-area network (WAN) latency is unacceptable during a biosecurity event. The edge node must calculate and enforce atmospheric and fluid containment natively to prevent pathogen or contaminant propagation.

## 1. Automated Zone Isolation & Negative Pressure Modulation
The physical node interfaces directly with localized HVAC and environmental control infrastructure via isolated SCADA relays to enforce strict atmospheric quarantine zones.

* **Airlock Pressure Modulation:** To maintain a biologically secure negative pressure environment, the C++ runtime dynamically calculates the required volumetric airflow extraction rate ($Q$) based on the targeted pressure differential ($\Delta P$) and the structural leakage area ($A$). The node computes this continuously:
  $$Q = C_d A \sqrt{\frac{2 \Delta P}{\rho}}$$
  *(Where $C_d$ is the discharge coefficient and $\rho$ is the ambient air density).* * **VFD Actuation:** The resulting calculation is fed into the closed-loop PID algorithms (`ACTUATOR_CONTROL.md`) to dynamically modulate the Variable Frequency Drives (VFDs) on exhaust fans. This mathematically guarantees the structural containment space remains at a persistent negative pressure state (e.g., $\le -25 \text{ Pa}$), regardless of external wind shear or door actuations.

## 2. M2M Containment Cascades
Biosecurity threats are highly mobile. A single isolated zone is insufficient if adjacent machinery continues to exchange biological or environmental material.

* **Mesh-Distributed Lockdown:** If a localized biological anomaly flag is verified (via integrated environmental sensors or a manual E-Stop override), the node instantly generates a high-priority `0x00` FlatBuffer containment directive.
* **Autonomous Handoff:** This payload is blasted across the 900 MHz FHSS DAG mesh. Adjacent nodes receive the directive and immediately drop into a synchronized lockdown state, ceasing all fluid exchanges, lowering implements, and mechanically locking all local airlock or payload bay doors to establish a site-wide quarantine perimeter.

## 3. Waste Path Mitigation & Thermal Sterilization
Liquid run-off and ventilation exhaust are primary vectors for cross-contamination. 

* **Galvanic Fluid Severance:** The system utilizes isolated Modbus RTU instructions to instantly actuate high-torque pneumatic isolation valves, hermetically sealing localized water channels, fluid drainage manifolds, and exhaust vectors.
* **Automated Thermal Flash:** For high-risk waste paths, the localized SCADA relays actuate high-temperature heating elements within the isolation spools. The node monitors internal RTD sensors to ensure the trapped fluid matrix exceeds strict sterilization parameters natively (e.g., $T \ge 121^\circ \text{C}$ for a sustained $t \ge 15 \text{ mins}$), neutralizing biological threats within the manifold before safe mechanical venting is permitted.
