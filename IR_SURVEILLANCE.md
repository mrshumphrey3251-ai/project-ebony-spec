# Infrared Surveillance & Thermal Processing Specification

This file outlines the low-latency ingestion of long-wave infrared (LWIR) camera matrices, localized threshold slicing, and cold-body tracking under zero-light conditions.

## 1. Edge-Native Thermal Ingestion
* **MIPI CSI Bus Alignment:** Pipes raw, uncompressed thermal camera streams straight into local hardware video processing units to minimize frame parsing latencies.
* **Localized Intensity Slicing:** Executes high-speed mathematical threshold checks on pixel arrays to isolate human or mechanical heat signatures from background ambient thermal noise.

## 2. Spatial Direction Mapping
* Compiles identified heat signatures into bit-packed coordinate messages to distribute tracking paths to adjacent mesh nodes over sub-GHz radio frequencies.
