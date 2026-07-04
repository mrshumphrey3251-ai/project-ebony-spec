# CORE_ENGINE: Sovereign Runtime & Deterministic Execution Specification

This specification defines the bare-metal execution architecture, deterministic thread scheduling, and memory isolation protocols for the Project Ebony core runtime loop operating on edge-native silicon (NVIDIA Jetson / ARM64).

## 1. Deterministic Execution Loop & Kernel Isolation
The core engine rejects standard asynchronous task scheduling. To guarantee latency bounds for physical machine control, the runtime operates on a hardened Linux 6.8 kernel patched with **RT-PREEMPT**.

* **Strict Cgroup Partitioning:** Heavy computational workloads (e.g., spatial vision inference, telemetry serialization) are sandboxed via kernel `cgroups` and pinned to specific Deep Learning Accelerator (DLA) cores. 
* **Real-Time Priority Scheduling:** Physical interface threads (J1939 CAN bus injection, Modbus RTU polling) are assigned maximum FIFO priority (`SCHED_FIFO`). The system guarantees a control-loop jitter of $< 5 \text{ ms}$ under maximum CPU load.

## 2. Zero-Copy FFI (Foreign Function Interface)
The core logic agent (compiled via Dart/Flutter ahead-of-time) does not execute hardware commands directly. It orchestrates state intentions. 

* **Native C++ Binding:** All mechanical actuations, cryptography, and sub-GHz radio modulations are executed by hardened C++ modules. The Dart runtime interfaces with these modules via strict FFI bindings utilizing zero-copy memory sharing to eliminate garbage collection (GC) latency spikes during critical physical operations.

## 3. Deadman Diagnostics & Hardware Watchdog
The core engine does not rely on software-level error catching for physical safety. 

* **State Snapshots:** The C++ runtime syncs an append-only state hash to local solid-state memory at $10 \text{ Hz}$.
* **Hardware Deadman Switch:** A discrete hardware watchdog timer monitors the primary control loop. If the core thread hangs, misses a tick, or fails a localized integrity check, the watchdog bypasses the OS entirely, severing the hydraulic pilot valves to physically immobilize the asset while triggering an immediate TPM 2.0 cryptographic seal of the operational ledger.
