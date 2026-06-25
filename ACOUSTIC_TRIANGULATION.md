# Acoustic Triangulation Module Specification

This module defines the mathematical and hardware-in-the-loop processing specifications for local passive acoustic event localization.

## 1. Hardware Microphone Array Profiles
* **Interface Protocol:** Low-latency I2S / ALSA native hardware streams.
* **Sampling Matrix:** Multi-channel synchronous high-frequency capture with real-time analog noise filtering.

## 2. DSP & Time-Difference-of-Arrival (TDOA) Logic
* **Signal Isolation:** Local DSP algorithms perform bandpass filtering to isolate specific sound signatures (e.g., mechanical failures, high-impact structural compromises).
* **Localization Vectors:** Cross-correlation matrices map sub-millisecond arrival differences across geographically spaced micro-nodes to calculate real-time grid coordinates without external GPS dependencies.
