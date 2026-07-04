# EMITTER_LOCALIZATION: Spatial TDOA Intersection & RF Fingerprinting

**Classification:** Gated Engineering Documentation / SIGINT & Localization Layer
**Target Architecture:** Wideband SDR / Hardware Oscillators / DLA Cores

This document details the software-defined radio processing loops used to intercept, fingerprint, and geographically map hostile or anomalous RF transmission points. Project Ebony assumes the operational environment contains unauthorized actors or active electronic warfare (EW) nodes. The localized mesh must act as a distributed sensor matrix, autonomously triangulating emitter locations and classifying their hardware signatures purely on the edge.

## 1. Multi-Node TDOA Intersection & Hyperbolic Compute
Geolocating an emitter without directional antennas requires computing the microscopic delay of the signal as it hits physically separated mesh nodes. 

* **Microsecond Clock Synchronization:** The local nodes maintain synchronized time domains using hardware-timestamped Precision Time Protocol (IEEE 1588v2 PTP) passing over the sub-GHz mesh, backed by local high-stability oscillators.
* **TDOA Calculation:** When an anomalous signal is detected, a node records the exact time of arrival ($t_i$). It shares this timestamp with an adjacent peer node ($j$). The native C++ runtime calculates the exact Time-Difference-of-Arrival ($\Delta t_{ij}$):
  $$\Delta t_{ij} = t_i - t_j$$
* **Spatial Intersection Vectors:** The time delta is converted to a physical distance delta using the speed of light ($c$). The edge node mathematically maps the hyperbolic intersection curve between the two nodes natively on the Orin CPU:
  $$\sqrt{(x - x_i)^2 + (y - y_i)^2} - \sqrt{(x - x_j)^2 + (y - y_j)^2} = c \Delta t_{ij}$$
  *(Where $(x,y)$ is the unknown emitter location, and $(x_i, y_i)$ and $(x_j, y_j)$ are the physical coordinates of the intercepting nodes).* By fusing the data from three or more nodes, the system runs a non-linear least squares optimization to instantly plot the precise $(x,y)$ coordinates of the hostile emitter without cloud processing dependencies.

## 2. Signal Fingerprinting & Hardware Identification
Simply locating a signal is insufficient; the node must mathematically classify the transmitter type to determine if it is a standard commercial radio, a military-grade jammer, or a spoofed control signal.

* **I/Q Baseband Ingestion:** The onboard SDR hardware captures the raw In-Phase ($I$) and Quadrature ($Q$) data streams of the intercepted burst.
* **Transient Phase Extraction:** No two physical RF amplifiers are perfectly identical. The system analyzes the microscopic, transient turn-on characteristics of the transmitter. The C++ DSP pipeline calculates the instantaneous phase $\phi(t)$ natively:
  $$\phi(t) = \arctan\left(\frac{Q(t)}{I(t)}\right)$$
* **DLA Classification:** The phase deviation variance and localized Power Spectral Density metrics are fed into the Jetson Deep Learning Accelerators (DLA). The INT8-quantized edge model analyzes this "RF DNA" against known hardware profiles, classifying the specific transmitter type and generating an un-spoofable mathematical fingerprint.
