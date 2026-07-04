# ANALOG_OVERRIDE: Galvanic Intercepts & Hardwired Relay Isolation

**Classification:** Gated Engineering Documentation / Analog Hardware Layer
**Target Architecture:** Solid-State Relays / Electro-Hydraulic Spools

This specification outlines the physical hardware-level cutoff and mechanical bypass logic required when digital execution loops must be completely and violently isolated. Project Ebony operates heavy kinetic machinery; because software is fundamentally fallible, all critical safety intercepts are executed via un-hackable, analog-first galvanic disconnects.

## 1. Galvanic Control Bus Intercept & Zero-Trust Isolation
The primary execution environment cannot be trusted during a catastrophic failure. Safety circuits operate entirely outside the Jetson Orin CPU's domain.

* **Solid-State Power Disconnects:** The control pathways between the C++ execution threads and the physical J1939 CAN bus are bridged via optical galvanic isolators. If analog sensors detect a physical limit breach (e.g., extreme hydraulic overpressure), local bypass switches instantly break the transmission lines, rendering the automated software node physically incapable of driving the actuators.
* **Hardwired Emergency Stop (E-Stop):** The manual safety override prioritizes a strict normally-closed (NC) analog loop. Activating the E-Stop mechanically breaks continuity. 
* **Inductive Decay Severance:** Upon breaking the E-Stop loop, the hold-voltage to the downstream electro-mechanical relays decays instantly. The current drop across the actuator solenoids is governed entirely by the inherent RL circuit physics, not software execution:
  $$I(t) = I_0 e^{-\frac{R}{L}t}$$
  The system is hardwired so the physical relays drop out and snap to their mechanical safe-states before the operating system even registers the interrupt, completely ignoring any conflicting software instruction registers.

## 2. Mechanical Fallback & Hydraulic Spool Re-routing
If the digital core is compromised, bricked via an active tamper response (as outlined in `TAMPER_RESPONSE.md`), or structurally destroyed, the physical asset must still be manageable by human operators at the site perimeter.

* **Manual Proportional Override:** Local analog adjustments physically re-route actuator path lines. The primary electro-hydraulic proportional valves are equipped with redundant mechanical spools.
* **Pilot Pressure Bleed:** By manually engaging the override pins on the manifold block, operators can bypass the disabled solid-state relays (SSRs) and directly route pilot pressure to the main cylinders. This enables human technicians to manually raise implements, release track brakes, and physically maneuver the asset without requiring a digital handshake, active power rail, or OS-level authorization.
