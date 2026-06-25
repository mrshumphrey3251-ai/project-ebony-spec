# Telemetry Streaming & Serialization Specification

This document details the serialization formats, packet compression parameters, and network transmission queues for sending real-time state metrics across the node network.

## 1. Low-Overhead Binary Serialization
* **FlatBuffer Schema Enforcement:** Compiles all internal state metrics into strict, zero-copy binary layouts that eliminate parse overhead during ingestion loops.
* **Delta-Encoded Payload Maps:** Transmits only modified values relative to the last known state vector to preserve raw bandwidth limits over sub-GHz mesh lines.

## 2. Prioritized Transmission Queuing
* Sorts outgoing telemetry frames into discrete priority lanes, guaranteeing that safety-critical alarms bypass background performance metrics.
