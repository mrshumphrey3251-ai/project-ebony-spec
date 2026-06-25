# CBRN Sensing Matrix Specification

This specification handles the continuous ingestion, baseline normalization, and threshold tracking of ambient radiological, particulate, and electrochemical air quality monitors.

## 1. Radiation & Ionization Sensing
* **Geiger-Müller Interface:** Ingests raw pulse counts from localized radiation sensing components over isolated hardware interfaces to track real-time microsievert variations.
* **Gas-Phase Chromatography Mocks:** Parses telemetry arrays from ambient air quality sensors to spot volatile toxic compounds or chemical agent signatures.

## 2. Baseline Normalization Dynamics
* Computes running environmental telemetry averages locally at the edge node to identify immediate structural changes while avoiding false alarms from natural variations.
