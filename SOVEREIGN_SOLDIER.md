# KINETIC_GOVERNANCE: Sovereign Flight Perimeter & Avionics Isolation

**Classification:** Project Ebony / Aerospace Sovereign Layer  
**Target Architecture:** ARINC 429 / AFDX (ARINC 664) / DO-178C RT-PREEMPT / Zero-Trust Uplink  

This specification handles the physical isolation, deterministic bus policing, and mathematical state verification for commercial and tactical avionics arrays. An aircraft cannot rely on ground-based IP infrastructure to maintain its flight envelope. The edge node (the Sovereign Flight Computer) must physically bridge the gap between legacy federated avionics (ARINC 429) and modern integrated modular avionics (AFDX). It must mathematically guarantee that malicious cloud uplinks or spoofed ACARS telemetry can never cross the hardware gap to manipulate the fly-by-wire actuators or engine controllers.

## Nomenclature & Acronym Glossary

| Term | Definition | Context |
| :--- | :--- | :--- |
| **ACARS** | Aircraft Communications Addressing and Reporting System | A digital datalink system for transmission of short messages between aircraft and ground stations; historically unencrypted. |
| **AFDX** | Avionics Full-Duplex Switched Ethernet | Standardized as ARINC 664 Part 7. A deterministic, highly reliable Ethernet protocol used in modern aircraft (e.g., A380, B787). |
| **ARINC 429** | Legacy Avionics Bus | A two-wire, point-to-point data bus standard heavily utilized for critical sensors (Pitot tubes, Gyros). Transmits in 32-bit words. |
| **BAG** | Bandwidth Allocation Gap | The minimum mathematical time interval allowed between two consecutive AFDX frames on a Virtual Link. |
| **VL** | Virtual Link | A logical unidirectional connection over the AFDX physical network, isolating different traffic types. |

---

## 1. ARINC 429 Galvanic Isolation & Deterministic Parsing
Critical flight data—like airspeed from the Pitot-static system and attitude from the Inertial Reference Units (IRU)—arrives over simplex, twisted-pair ARINC 429 lines. Because these lines are physically unroutable, they are inherently secure from remote IP attacks, but they are vulnerable to electromagnetic interference (EMI) or sensor degradation.

* **Hardware Parity Auditing:** ARINC 429 transmits exactly 32 bits per word. The 32nd bit is the parity bit. The RT-PREEMPT kernel intercepts the word via DMA and mathematically verifies odd parity on the silicon before the data ever reaches the flight envelope protection logic. Let $b_i$ represent the $i$-th bit of the 32-bit word. The hardware computes the parity sum ($P$):

  $$P = \left( \sum_{i=1}^{31} b_i \right) \pmod 2$$

  If $b_{32} \neq \neg P$ (for odd parity), the physical copper wire has suffered electromagnetic corruption. The word is instantaneously dropped at the boundary.
* **Sign/Status Matrix (SSM) Bounding:** Bits 30 and 31 contain the SSM, dictating the operational state of the transmitting sensor (Normal, No Computed Data, Functional Test, Failure Warning). The hardware strictly enforces a lockout on any word that does not carry the exact binary signature for "Normal Operation," mathematically blinding the flight computer to degraded sensor hallucination.

---

## 2. AFDX Virtual Link (VL) Fencing & Anti-Spoofing
Modern aircraft use AFDX to route heavy telemetry. Because AFDX is based on standard Ethernet (IEEE 802.3), it is a prime target for adversarial packet flooding if the ground-to-air gateway is compromised. The aircraft must mathematically restrict bandwidth.

* **BAG Timer Calculus:** To prevent network saturation, AFDX relies on Virtual Links (VLs), each assigned a strict Bandwidth Allocation Gap (BAG) ranging from 1 to 128 milliseconds. Let $S_{max}$ be the maximum allowed frame size (in bytes), and let the transmission speed be constant. The absolute maximum bandwidth allocated to a specific flight subsystem ($BW_{VL}$) is strictly enforced by the physical switch fabric:

  $$BW_{VL} = \frac{S_{max}}{BAG}$$

* **Silicon Traffic Policing:** The Sovereign Edge Node actively polices the VL handling external ground comms. Let $T_n$ be the arrival timestamp of the current frame, and $T_{n-1}$ be the timestamp of the previous frame. The kernel evaluates the arrival delta against the defined BAG:

  $$T_n - T_{n-1} < BAG - \tau_{jitter}$$

  *(Where $\tau_{jitter}$ is the allowable hardware jitter).* If a compromised SATCOM gateway attempts to flood the internal avionics network, the mathematical inequality triggers immediately. The AFDX switch natively drops the offending frames, severing the ground-link and isolating the flight controls.

---

## 3. The Raw Code: ARINC 429 Ingestion & AFDX Boundary Enforcement
This is the bare-metal reality of a sovereign flight deck. The kernel evaluates the legacy parity math, polices the modern Ethernet gaps, and cuts the cloud link instantly if the constraints are violated in pure C space.

```c
#include <linux/types.h>
#include <linux/time.h>

// RT-PREEMPT Aerospace Isolation Loop (Pure C Kernel Space)

// 1. ARINC 429 Parity & SSM Validation
bool ingest_arinc429_word(u32 raw_arinc_word, float* extracted_telemetry) {
    
    // Mathematically evaluate Odd Parity (Bit 32)
    u32 parity_bit = (raw_arinc_word >> 31) & 0x01;
    u32 computed_parity = calculate_hardware_parity(raw_arinc_word & 0x7FFFFFFF);
    
    if (parity_bit == computed_parity) {
        log_hardware_fault("WARNING: ARINC429_PARITY_FAILURE. EMI DETECTED.");
        return false;
    }

    // Evaluate the Sign/Status Matrix (Bits 30-31)
    u32 ssm = (raw_arinc_word >> 29) & 0x03;
    if (ssm != ARINC_SSM_NORMAL_OPERATION) {
        log_hardware_fault("WARNING: SENSOR_DEGRADATION_FLAGGED. IGNORING DATA.");
        return false;
    }

    // Word is mathematically sound. Extract the 19-bit payload (Bits 11-29).
    *extracted_telemetry = decode_bvr_to_float(raw_arinc_word);
    return true;
}

// 2. AFDX Virtual Link Fencing (BAG Policing)
bool police_afdx_virtual_link(u16 virtual_link_id, u64 current_frame_timestamp_ns) {
    
    u64 last_timestamp_ns = get_vl_previous_timestamp(virtual_link_id);
    u64 time_delta_ns = current_frame_timestamp_ns - last_timestamp_ns;
    
    u64 assigned_bag_ns = lookup_vl_bag_allocation(virtual_link_id);

    // Evaluate frame arrival against the deterministic Bandwidth Allocation Gap
    if (time_delta_ns < (assigned_bag_ns - AFDX_ALLOWED_JITTER_NS)) {
        
        // FATAL: The data rate has mathematically exceeded the hardware allocation.
        // A potential packet-flooding attack or network loop is occurring.
        log_hardware_fault("FATAL: AFDX_BAG_VIOLATION. SATURATION ATTACK DETECTED.");
        
        // 3. Autonomous Uplink Severance
        // If the violating link is the SATCOM/Ground gateway, sever it completely.
        if (virtual_link_id == VL_EXTERNAL_GATEWAY) {
            write_physical_register(SATCOM_UPLINK_RELAY_ADDR, 0x00); // DROP CLOUD CONNECTION
            log_hardware_fault("AIRCRAFT HAS ENTERED FULL SOVEREIGN ISOLATION.");
        }
        
        return false; // Drop the malicious frame at the silicon switch level
    }

    // Frame arrival is valid and deterministic. Update hardware tracker.
    update_vl_timestamp(virtual_link_id, current_frame_timestamp_ns);
    return true;
}
