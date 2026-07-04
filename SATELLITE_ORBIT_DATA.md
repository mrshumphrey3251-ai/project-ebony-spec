# KINETIC_GOVERNANCE: Satellite Orbit Tracking & Ephemeris Database

**Classification:** Project Ebony / Orbital Mechanics Layer  
**Target Architecture:** SGP4 / TLE / Topocentric Coordinate Transformation / RT-PREEMPT  

This document details the parsing parameters for Two-Line Element (TLE) sets, orbital mechanics propagation routines, and look-angle calculations for satellite communication arrays. Sovereign edge nodes operating in hostile physical theaters cannot rely on cloud APIs to determine orbital trajectories. The node must execute the Simplified General Perturbations (SGP4) physics model natively, computing exact topocentric azimuth and elevation angles to physically steer directional antennas toward passing satellites with absolute mathematical autonomy.

## Nomenclature & Acronym Glossary

| Term | Definition | Context |
| :--- | :--- | :--- |
| **Azimuth ($Az$)** | Compass Direction | The horizontal angle measured clockwise from true north to the target. |
| **Elevation ($El$)** | Vertical Angle | The vertical angle measured from the local geometric horizon up to the target. |
| **Ephemeris** | Orbital Data | A tabulated dataset giving the calculated positions of a celestial object or artificial satellite at regular intervals. |
| **SGP4** | Propagation Model | Simplified General Perturbations; the mathematical model used to calculate orbital state vectors of Earth-orbiting satellites. |
| **TLE** | Two-Line Element | A standard format encoding a list of orbital elements for a given epoch. |

---

## 1. Local Simplified General Perturbations (SGP4) Execution
A satellite does not orbit in a perfect ellipse; its trajectory is constantly perturbed by the Earth's oblateness, atmospheric drag, and lunar gravity. 

* **Offline Vector Calculations:** The RT-PREEMPT kernel natively parses locally cached TLE datasets and feeds them into an optimized SGP4 propagation block. Given the satellite's epoch and the current hardware timestamp ($t$), the SGP4 engine mathematically outputs the satellite's exact Earth-Centered Inertial (ECI) position vector ($\vec{r}_{ECI}$).
* **Look-Angle Determination:** To point a physical antenna, the ECI vector must be converted to the node's local topocentric horizon coordinate system—specifically the South-East-Zenith (SEZ) frame. Let $\vec{\rho}$ be the relative position vector of the satellite from the ground node, with components $\rho_S, \rho_E$, and $\rho_Z$. The kernel calculates the exact local Azimuth ($Az$) and Elevation ($El$) natively on the silicon:

  $$El = \arcsin\left( \frac{\rho_Z}{|\vec{\rho}|} \right)$$
  
  $$Az = \arctan2(\rho_E, -\rho_S)$$

  These absolute angles are piped directly to the servo-controllers driving the active directional antenna, ensuring the physical RF beam remains mathematically locked onto the satellite as it traverses the sky at **7.5 km/s**.

---

## 2. Ephemeris Refresh Integrity
Satellites experience orbital decay. A TLE cached three weeks ago will result in a pointing error large enough to completely miss the transmission window. The localized database must be continuously refreshed, but updating the physics engine introduces a catastrophic vulnerability if the data is spoofed.

* **Cryptographic TLE Verification:** When the node successfully establishes an uplink, the satellite blasts a compressed block of updated TLE sets back down to the node. 
* **Signature Auditing:** Before the node replaces its active localized satellite positioning matrix, the RT-PREEMPT kernel extracts the ML-DSA-85 post-quantum digital signature attached to the TLE block. If the signature math fails to align with the node's hardcoded trust anchor, the update is instantly discarded as a hostile spoofing attempt, preserving the integrity of the tracking engine.

---

## 3. The Raw Code: SGP4 Physics Engine & Look-Angle Calculus
This is the bare-metal reality of autonomous orbital mechanics. The kernel propagates the Keplerian physics, executes the topocentric trigonometric transform, and commands the mechanical antenna servos natively in pure C space.

```c
#include <linux/math64.h>
#include <linux/time.h>
#include <linux/crypto.h>

// RT-PREEMPT Orbital Tracking Loop (Pure C Kernel Space)
bool update_antenna_tracking_vector(u32 active_satellite_id) {
    
    // 1. Retrieve the localized, cryptographically verified TLE block
    tle_data_t current_tle = fetch_local_ephemeris(active_satellite_id);
    u64 current_hardware_time = get_hardware_rtc_seconds();

    // 2. Offline SGP4 Execution (Outputting ECI state vectors)
    // Mathematically propagate the satellite's physical position through time and gravity
    vector_3d_t sat_eci_pos;
    if (execute_sgp4_propagation(&current_tle, current_hardware_time, &sat_eci_pos) != SGP4_SUCCESS) {
        log_hardware_fault("WARNING: SGP4_PROPAGATION_FAILED.");
        return false;
    }

    // 3. Coordinate Transformation (ECI to SEZ Topocentric Horizon)
    vector_3d_t relative_sez_pos = transform_eci_to_sez(sat_eci_pos, LOCAL_NODE_LAT, LOCAL_NODE_LON);

    // 4. Look-Angle Determination (Azimuth & Elevation Calculus)
    float slant_range = calculate_vector_magnitude(relative_sez_pos);
    
    // El = arcsin(Z / Range) | Az = atan2(East, -South)
    float target_elevation = asinf(relative_sez_pos.z / slant_range) * (180.0f / PI);
    float target_azimuth   = atan2f(relative_sez_pos.y, -relative_sez_pos.x) * (180.0f / PI);

    // 5. Hardware Actuation: Servo Feedback Loop
    if (target_elevation > MIN_ANTENNA_ELEVATION_LIMIT) {
        
        // Command the physical stepper motors to lock onto the calculated trajectory
        write_physical_register(ANTENNA_AZIMUTH_SERVO_ADDR, convert_degrees_to_pwm(target_azimuth));
        write_physical_register(ANTENNA_ELEVATION_SERVO_ADDR, convert_degrees_to_pwm(target_elevation));
        
        return true; // Antenna physically aligned to orbital trajectory
    }

    return false; // Satellite currently below the local physical horizon
}

// 6. Ephemeris Refresh Integrity (Executed asynchronously upon data receipt)
bool ingest_ephemeris_update(u8* signed_tle_payload, size_t payload_size) {
    
    // Extract the ML-DSA-85 post-quantum signature and validate the TLE payload
    if (!verify_pq_signature(signed_tle_payload, payload_size, TRUSTED_SPACE_COMMAND_PUBKEY)) {
        log_hardware_fault("FATAL: TLE_SIGNATURE_INVALID. SPOOFING ATTEMPT DETECTED.");
        return false; // Drop corrupted orbital data immediately
    }
    
    // Mathematically safe. Commit new physics matrix to local NVMe storage.
    commit_tle_to_local_storage(signed_tle_payload);
    return true;
}
