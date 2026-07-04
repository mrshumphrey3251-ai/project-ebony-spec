# KINETIC_GOVERNANCE: Machine Immobilization & Safe Escalation

**Classification:** Project Ebony / Kinetic Denial Layer  
**Target Architecture:** J1939 CAN / Galvanic SSR / RT-PREEMPT / Multi-Sig Quorum  

This document details the hardware-level cutoffs, emergency deceleration protocols, and physical engine immobilization overrides executed across heavy corporate or fleet assets. Immobilization is a weapon; it cannot be triggered by a single compromised cloud server or a spoofed network packet. Kinetic denial must be enforced at the silicon layer, mathematically bound to physical cryptography, and executed natively on the vehicle's internal control buses.

## Nomenclature & Acronym Glossary

| Term | Definition | Context |
| :--- | :--- | :--- |
| **CAN (J1939)** | Controller Area Network | Vehicle bus standard heavily utilized in diesel engines and industrial machinery. |
| **Galvanic Isolation** | Electrical Separation | Isolating functional sections of electrical systems to prevent current flow; severing the physical circuit. |
| **Multi-Sig** | Multiple Signature | Cryptographic requirement for multiple independent keys to authorize a critical state change. |
| **Quorum** | Validation Threshold | The mathematical minimum number of mesh nodes required to validate a kinetic override. |
| **RT-PREEMPT** | Real-Time Preemption | Strict Linux kernel patch guaranteeing microsecond scheduling determinism. |
| **SSR** | Solid-State Relay | High-speed electronic switching device for physically actuating the power cutoff. |

---

## 1. Hardware Relay Cascades
Software-level ignition kills are easily bypassed. True immobilization requires severing the physics of combustion.

* **Galvanic Fuel Cutoffs:** Upon a validated threat detection, the edge node bypasses the Engine Control Unit (ECU) entirely. It activates localized Solid-State Relays (SSRs) to instantly drop the actuation voltage to the high-pressure fuel injection pumps and the main starter solenoids. The engine is mechanically starved of thermodynamics.
* **CAN Bus Overrides:** Simply killing the engine on a 50-ton asset moving at velocity will result in a free-rolling kinetic projectile. The node must simultaneously inject high-priority J1939 control frames onto the powertrain bus. It forces the transmission into neutral and calculates the maximum safe braking force ($F_b$) based on the asset's mass ($m$), current velocity ($v$), and the mechanical friction coefficient ($\mu_k$):

  $$F_b = \mu_k \cdot m \cdot g$$

  By calculating the deceleration curve natively, the node triggers the electronic braking system independently of operator cabin inputs, safely arresting the asset's kinetic energy without causing mechanical shearing or rollover.

---

## 2. Air-Gapped Trust Boundaries
Because immobilization poses a severe kinetic risk, the authorization pathway must be entirely air-gapped from standard application layers.

* **Cryptographic Quorum:** High-privilege immobilization commands strictly reject standard IP-based authentication. Execution requires a mathematically validated physical crypto-token handshake (such as FIDO2/TPM bounding) or a localized multi-signature quorum. 
* **Mesh Consensus:** If an immobilization command is received, the edge node polls adjacent mesh vertices over sub-GHz radio. Let $n$ be the total available adjacent nodes and $k$ be the hardcoded quorum threshold. The immobilization state ($S_{kill}$) is only authorized if the sum of valid cryptographic signatures ($\sum Sig$) satisfies the quorum:

  $$S_{kill} \iff \sum_{i=1}^{n} Sig_i \ge k$$

  Without physical cryptographic consensus, the command is mathematically nullified at the kernel layer.

---

## 3. The Raw Code: Quorum Validation & J1939 Override
This is the bare-metal execution loop for autonomous kinetic denial. The kernel verifies the cryptographic quorum, calculates the safe deceleration vector, and actuates the SSR and CAN bus frames natively in pure C.

```c
#include <linux/can.h>
#include <linux/crypto.h>
#include <linux/types.h>

// RT-PREEMPT Immobilization Loop (Pure C Kernel Space)
bool execute_kinetic_immobilization(u8* token_signatures, size_t sig_count, u32 current_velocity) {
    
    // 1. Air-Gapped Trust Boundary (Multi-Sig Quorum Validation)
    // Command dies here if cryptographic consensus is not physically met
    if (!validate_mesh_quorum(token_signatures, sig_count, MIN_REQUIRED_QUORUM)) {
        trigger_hardware_fault(SECURITY_BUS_ADDR, "FATAL: IMMOBILIZATION_QUORUM_FAILED");
        return false; 
    }

    // 2. Compute Safe Kinematic Deceleration 
    // Mathematically bounds braking force to prevent mechanical shearing during E-Stop
    u32 safe_braking_force = calculate_deceleration_curve(current_velocity, ASSET_MASS, MAX_G_FORCE);

    // 3. Hardware Relay Cascade: Galvanic Fuel & Ignition Cutoff
    write_physical_register(FUEL_PUMP_SSR_ADDR, 0x00); // STARVE THERMODYNAMICS
    write_physical_register(STARTER_RELAY_ADDR, 0x00); // KILL IGNITION LATCH

    // 4. J1939 CAN Bus Override: Priority Frame Injection
    struct can_frame kill_frame;
    kill_frame.can_id  = J1939_PRIORITY_OVERRIDE | CAN_EFF_FLAG;
    kill_frame.can_dlc = 8;
    
    // Pack safe braking vector and neutral shift into the raw hex payload
    pack_j1939_brake_command(&kill_frame, safe_braking_force);
    pack_j1939_neutral_shift(&kill_frame);

    // 5. Blast priority frame directly to physical powertrain bus (Bypassing cabin inputs)
    dispatch_can_frame_direct(POWERTRAIN_CAN_IFACE, &kill_frame);

    return true; // Asset mathematically and physically neutralized
}
