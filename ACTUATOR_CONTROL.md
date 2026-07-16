# 🔒 RESTRICTED: Phase 2 Hardware Integration

The contents of this specification have been moved to the **Private Deployment Repository** in accordance with the Project Ebony Open-Core security model.

This file contained exact bare-metal integration scripts, physical wiring schematics, or active hardware deployment keys. 
# KINETIC GOVERNANCE: Bare-Metal Actuator Control (The Final Physical Mile)

When translating software intelligence into heavy physical motion, high-level languages (like Python or Node.js) present a catastrophic risk. Garbage collection pauses and runtime overhead can cause a multi-ton machine to miss its braking window by fatal milliseconds. 

Project Ebony strictly isolates all physical actuation logic to the lowest possible software layer. 

### The Final Physical Mile
* **Direct Kernel Access (`sysfs`):** We completely bypass commercial soft-robotics libraries. The motor control logic is written in strict, memory-safe C++ that writes electrical voltage instructions directly to the Linux kernel's `sysfs` hardware registers.
* **Hardcoded Safety Governors:** The C++ actuation logic contains immutable mathematical ceilings for Duty Cycle and RPM. Even if the upstream Llama-3 AI or the Rust execution daemon hallucinates and requests a hyper-aggressive speed, the C++ hardware interface will reject the command, capping the kinetic output to prevent machine self-destruction.
* **Zero Garbage Collection:** Because this layer uses bare-metal C++, there are no unpredictable memory clearing pauses. When the edge node commands a hydraulic valve to close, the execution latency is strictly bounded and deterministic.
To request access to the unabridged hardware specifications, refer to the **Access Protocols** in the main `README.md`.
