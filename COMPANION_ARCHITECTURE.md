# Project Ebony: Companion Architecture & Human-Asset Synchronization

This document outlines the decentralized specifications for **The Companion**—the local, interactive interface layer of Project Ebony running natively on edge silicon (NVIDIA Jetson platform). This architecture enforces zero-trust physical safety through immersive training and un-bypassable hardware lockdowns.

---

## 1. LOTO-by-Training (Lockout/Tagout Verification)

Traditional industrial Lockout/Tagout (LOTO) protocols rely on passive, analog mechanisms (physical padlocks and paper tags). Project Ebony replaces these vulnerable, human-error-prone practices with a hardware-enforced, cryptographic gate tied directly to operator competency verification.

### Core Mechanism:
* **The Silicon Lock:** The local control rail and PLC override mechanisms are maintained in a hardened, un-bootable state by default. 
* **Dynamic Safety Credentialing:** The physical asset refuses to pass ignition voltages or open SCADA control paths until the local edge chip processes an authorization handshake from the local Companion interface.
* **The Requirement:** Authorization is only granted if the unique, bio-sensed operator has successfully logged a verified passing score in the specific, scenario-required synthetic training sandbox within the mandatory validation window.

---

## 2. Immersive AR/VR Synthetic Sandbox

To eliminate accidents caused by untrained personnel or unexpected field anomalies, operators are required to interface with the asset digitally before executing physical manipulation.
