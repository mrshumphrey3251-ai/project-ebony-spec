# Actuator Control & Closed-Loop Modulation Specification

This specification handles the deterministic translation of edge-intelligence directives into physical electromechanical work.

## 1. Physical Bus Interfacing
* **Buses Supported:** Isolated CAN bus (ISO 11898), Modbus RTU (RS-485), and solid-state SCADA relays.
* **Deterministic Limits:** Core control loops execute inside highly prioritized real-time constraints (<1ms scheduling jitter via RT-PREEMPT).

## 2. Active Mechanical Posture
* **PID Loop Processing:** Native C++ modules ingest local pressure, temperature, and fluid telemetry to calculate micro-adjustments via closed-loop PID algorithms.
* **Fail-Safe Fallbacks:** Independent hardware watchdogs listen for system heartbeats. If the primary software loop encounters an exception, actuators automatically drop back to hardcoded mechanical safe-states.
