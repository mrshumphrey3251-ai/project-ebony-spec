# FIBER_PERIMETER_SECURITY: Distributed Acoustic Sensing & Threat Matrix

**Classification:** Gated Engineering Documentation / Physical Perimeter Layer
**Target Architecture:** DAS Interrogator / Jetson Edge DSP / Single-Mode Fiber

This document details the optical interferometry parsing loops and structural tracking protocols for buried fiber-optic sensor arrays. Project Ebony assets are often deployed in highly volatile, expansive environments. The physical perimeter must act as a continuous, un-spoofable sensor matrix, capable of detecting and classifying physical intrusions instantly at the edge without wide-area network dependencies.

## 1. Optical Interferometry Analysis & DAS Ingestion
The buried single-mode fiber array functions as a massive, continuous microphone. The node injects coherent laser pulses and analyzes the microscopic Rayleigh backscatter to detect kinetic ground disturbances.

* **Phase Modulation Tracking:** When an intruder breaches the perimeter, the acoustic vibration induces a microscopic strain ($\epsilon$) on the fiber core. The native DSP pipeline measures the sub-nanometer optical phase shift ($\Delta \phi$) of the backscattered light natively:
  $$\Delta \phi(z,t) = \frac{4\pi n}{\lambda} \epsilon(z,t) L$$
  *(Where $n$ is the refractive index of the fiber, $\lambda$ is the interrogation laser wavelength, and $L$ is the spatial gauge length).* This allows the edge node to track minute environmental acoustic vibrations securely.
* **Localization Mapping (OTDR Compute):** The system does not merely detect an intrusion; it mathematically pinpoints it. The local edge node computes the transient pulse velocity delay ($\Delta t$) of the returning scattered photons using continuous Optical Time-Domain Reflectometry (OTDR). The exact physical distance ($z$) of the boundary intrusion is mapped natively:
  $$z = \frac{c \cdot \Delta t}{2 n_g}$$
  *(Where $c$ is the speed of light in a vacuum and $n_g$ is the group refractive index of the fiber).* This spatial computation is executed completely offline, guaranteeing zero-latency localization without wide-area network queries.

## 2. Threat Classification Matrix & DSP Filtering
A perimeter sensor that alarms for every falling branch or passing deer is operationally useless. The edge node must mathematically isolate hostile vectors from standard environmental background noise.

* **Deterministic Cross-Correlation:** The raw acoustic waterfall matrix is piped into the Jetson Deep Learning Accelerators (DLA). To minimize false alarm triggers across the physical perimeter, the node filters out typical environmental noise patterns (such as heavy wind or wildlife movement) by computing the cross-correlation ($R_{xy}$) of the ingested acoustic signal ($x(t)$) against a frozen, localized library of verified hostile kinetic signatures ($T(t)$):
  $$R_{xy}(\tau) = \int_{-\infty}^{\infty} x(t) T(t-\tau) dt$$
* **Kinetic Alarm Gating:** The RT-PREEMPT kernel evaluates the correlation peak against a dynamically tuned environmental threshold ($\tau_{alarm}$). If $R_{xy}(\tau)$ mathematically breaches $\tau_{alarm}$, the system confirms a hostile intrusion, logs the precise spatial coordinates to the encrypted ledger, and instantly dispatches the anomaly to the `CONSOLE_ALERTS.md` escalation path.
