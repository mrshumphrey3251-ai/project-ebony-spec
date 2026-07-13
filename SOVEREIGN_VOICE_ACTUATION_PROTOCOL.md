# Project Ebony: Sovereign Edge NLP & ADA-Compliant Actuation

## 1. Architectural Philosophy: The Right to Sovereign Execution
Modern enterprise machinery and aerial assets rely on corporate-controlled, cloud-dependent "walled gardens" for advanced features like voice actuation. This creates an institutional vulnerability and violates the fundamental Right to Repair and Operator Sovereignty. Project Ebony bypasses this dependency by migrating Natural Language Processing (NLP) entirely to the air-gapped edge.

## 2. Air-Gapped Voice Control (Zero-Cloud NLP)
To ensure 100% operational uptime and zero cloud latency, all voice commands are processed locally on bare-metal edge compute (e.g., NVIDIA Jetson architecture).
* **The Mesh:** Operators utilize an isolated, local-only network to transmit audio from a wearable node to the central compute node.
* **The Translation:** The edge node translates audio waves to text offline, mapping them to pre-compiled deterministic Rust actuation commands.

## 3. Decoupling Authentication from Actuation (The Two-Stage Gate)
To prevent autonomous physical hazards in heavy industrial or agricultural environments, voice control operates under a strict, mathematically verifiable safety gate:
* **Stage 1 (Connection):** The hardware handshake is secured, but actuators remain physically isolated from the power bus.
* **Stage 2 (Push-To-Talk Override):** Voice commands are ignored by the edge compute unless accompanied by a simultaneous, physical Push-To-Talk (PTT) hardware interrupt from the operator. 

## 4. Aerial Node Macro Triggers (Bypassing Proprietary Latency)
Direct, real-time voice joystick control of 3D aerial assets introduces unacceptable kinetic latency. Therefore, aerial deployment via voice is restricted to **Macro Triggers**. 
* The edge node translates the voice command and injects a single execution trigger to the isolated flight controller.
* The flight controller launches a mathematically pre-defined autonomous mission (e.g., perimeter sweep), maintaining absolute safety while completely bypassing the manufacturer's cloud APIs.
