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
## 6. Environmental Hardening & Kinetic Survivability
Deploying bare-metal compute (NVIDIA Jetson) into heavy agricultural environments requires rigorous physical protection that does not compromise the RF air-gap or thermal limits.
* **Faraday Mitigation:** Edge compute housed in metallic enclosures must utilize decoupled, exterior-mounted antennas to preserve the isolated local Wi-Fi mesh. 
* **Kinetic Isolation:** To survive unsprung kinetic shock from off-road operation, all silicon and inverter hardware must be mechanically decoupled from the chassis using internal elastomeric shock-mounts.
* **The Bulkhead Principle:** Environmental enclosures must be physically segregated. A sealed, thermally managed "Clean Room" for compute operations is strictly divided via a physical bulkhead from any mechanical utility or analog payload space to prevent moisture or conductive debris contamination.
## 7. Chronological Execution & State Management
To ensure the edge compute node operates with absolute determinism, the sovereign software stack runs on a strict, chronological execution loop built in memory-safe Rust. The software states are sequenced as follows:
* **State 0 (Boot & Lockdown):** Upon receiving power, the execution loop instantly defaults all digital GPIO output pins to a "Low" (Normally Closed) state, mathematically ensuring the mechanical relay cascade remains physically locked to manual control.
* **State 1 (The Handshake):** The master loop halts and listens exclusively for the offline cryptographic/biometric payload from the localized interface node. 
* **State 2 (The Sensory Loop):** Only after the biometric firewall is cleared does the system advance into the infinite sensory loop, simultaneously opening the audio mesh and listening for the physical Push-To-Talk (PTT) interrupt required for NLP translation. 
* **Failure State:** If authentication fails or the NLP service crashes, the execution loop immediately terminates, dropping GPIO voltage and instantly returning the heavy iron to its mechanical manual override defaults.
## 8. Network Topology Trade-Offs for Air-Gapped Authentication
Securing the biometric handshake across a localized, dead-router mesh presents two distinct topological paths:
* **Browser-Based (HTTP/REST):** Offers universal device accessibility and rapid deployment, but introduces severe friction with modern browser sandboxing (WebAuthn requires HTTPS, complicating offline PKI infrastructure).
* **Native Application (TCP Sockets):** Requires managing dual codebases (Compute Node + Interface Node) but provides unfettered, native access to hardware biometric scanners and localized wearable mesh networks without requiring external certificate validation.
