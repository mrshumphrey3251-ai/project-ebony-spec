# Project Ebony: Sovereign Edge NLP & ADA-Compliant Actuation

## 1. Architectural Philosophy: The Right to Sovereign Execution
Modern enterprise machinery and aerial assets rely on corporate-controlled, cloud-dependent "walled gardens" for advanced features like voice actuation. This creates an institutional vulnerability and violates the fundamental Right to Repair and Operator Sovereignty. Project Ebony bypasses this dependency by migrating Natural Language Processing (NLP) entirely to the air-gapped edge.

## 2. Air-Gapped Voice Control (Zero-Cloud NLP)
To ensure 100% operational uptime and zero cloud latency, all voice commands are processed locally on bare-metal edge compute (e.g., NVIDIA Jetson architecture).
* **The Mesh:** Operators utilize an isolated, local-only network to transmit audio from a wearable node to the central compute node.
* **The Translation:** The edge node translates audio waves to text offline, mapping them to pre-compiled deterministic Rust actuation commands.

## 3. The "Evil Maid" Defense: Edge-Level MFA & Cryptographic Deadlock
Relying on "Security Through Obscurity" (hiding physical kill switches) is a compromised defense. Project Ebony secures heavy iron using a bare-metal Multi-Factor Authentication (MFA) cascade:
* **Factor 1 (Physical Token):** An exposed, physical ignition key controls power to the localized compute node (the brain).
* **Factor 2 (Biometric Cryptography):** The compute node will not route power to the high-amperage drivetrain (the brawn) until the operator passes a localized, offline biometric scan (fingerprint).
* **The Deadlock:** If the physical key is hot-wired, the biometric firewall holds. If the digital system is somehow bypassed, the physical key removes the electrical bridge. The hardware is mathematically bricked to unauthorized operators.

## 4. True Drive-by-Wire (The Hardware Air-Gap)
Software cannot physically stop voltage. To achieve true, unhackable drive-by-wire capability, the edge compute node operates a physical cascade of electromagnetic relays. In the event of a total compute failure, the relays default to a "Normally Closed" mechanical state, instantly returning full manual control to the operator.

## 5. Aerial Node Macro Triggers (Bypassing Proprietary Latency)
Direct, real-time voice joystick control of 3D aerial assets introduces unacceptable kinetic latency. Therefore, aerial deployment via voice is restricted to **Macro Triggers**. 
* The edge node translates the voice command and injects a single execution trigger to the isolated flight controller.
* The flight controller launches a mathematically pre-defined autonomous mission (e.g., perimeter sweep), maintaining absolute safety while completely bypassing the manufacturer's cloud APIs.
