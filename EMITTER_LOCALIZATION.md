# Emitter Localization & Signal Intersection Specification

This document details the software-defined radio processing loops used to intercept, fingerprint, and geographically map RF transmission points.

## 1. Multi-Node TDOA Intersection
* **Synchronized Clocks:** Leverages ultra-precise local hardware clocks to calculate sub-microsecond Time-Difference-of-Arrival (TDOA) variations of RF signals across distinct edge nodes.
* **Spatial Intersection Vectors:** Computes directional intersection matrices locally at the edge to map anomalous signal source positions without cloud processing dependencies.

## 2. Signal Fingerprinting
* Extracts transient phase deviations and power spectrum metrics natively to classify specific transmitter types.
