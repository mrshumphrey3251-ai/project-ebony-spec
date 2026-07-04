# KINETIC_GOVERNANCE: PUF-Backed Post-Quantum Roots of Trust

**Classification:** Project Ebony / Physical Cryptography Layer  
**Target Architecture:** SRAM PUF / ML-KEM-1024 / Tamper-Evident Capacitance / no_std Rust  

This specification replaces fragile optical Quantum Key Distribution (QKD) with solid-state Physical Unclonable Functions (PUFs). Tactical edge nodes operate under brutal Size, Weight, and Power (SWaP) constraints, rendering delicate photon-alignment impossible. Instead of relying on the quantum state of traveling photons, the node utilizes the quantum-level manufacturing variations inherent in its own silicon gates. By measuring these microscopic imperfections, the hardware derives an un-forgeable cryptographic seed natively at boot, ensuring absolute Post-Quantum security without a single moving part or optical lens.

## Nomenclature & Acronym Glossary

| Term | Definition | Context |
| :--- | :--- | :--- |
| **ML-KEM-1024** | Post-Quantum Standard | The highest security tier of the NIST-approved lattice-based key encapsulation mechanism. |
| **PUF** | Physical Unclonable Function | A physical object that, for a given input (challenge), provides a practically unpredictable output (response) due to microscopic manufacturing flaws. |
| **SRAM PUF** | Static RAM PUF | Utilizing the unpredictable startup state of uninitialized SRAM memory cells to generate entropy. |
| **SWaP** | Size, Weight, and Power | The physical engineering constraints placed on tactical and mobile hardware. |

---

## 1. Silicon Entropy & Post-Quantum Key Derivation
The keys to the kinetic asset are not stored in memory. Stored keys can be extracted by an adversary using an electron microscope. Instead, the keys are *derived* from the physical metal every time the node boots.

* **SRAM Entropy Extraction:** When power is applied to the node, the uninitialized SRAM cells settle into a random state of 1s and 0s based on deep-submicron threshold voltage variations. This generates the raw PUF response ($R_{PUF}$). 
* **Cryptographic Seed Derivation:** The RT-PREEMPT kernel reads this raw response, passes it through a localized Error Correction Code (ECC) to eliminate thermal noise, and fuses it with the TPM 2.0 hardware key ($K_{TPM}$). The absolute Post-Quantum Seed ($Seed_{PQ}$) is generated via a secure hashing function ($\mathcal{H}$):

  $$Seed_{PQ} = \mathcal{H}(R_{PUF} \oplus K_{TPM})$$

  Because $Seed_{PQ}$ is dynamically calculated and only exists in volatile memory during active execution, an adversary powering down the node to steal the drive mathematically guarantees the destruction of the key.

---

## 2. Tamper-Evident Vaporization
If an adversary physically captures the Project Ebony node, their first objective will be decapsulation—using acid to strip the silicon packaging and read the active gates. 

* **Capacitance Collapse:** A PUF is hyper-sensitive to its physical environment. The exact parasitic capacitance ($C_{parasitic}$) of the silicon traces dictates the PUF response. If an adversary attempts to probe the chip or remove the packaging, $C_{parasitic}$ instantly shifts.
* **Mathematical Zeroization:** When the capacitance changes, the SRAM cells settle differently. The new response ($R_{tampered}$) will fail the mathematical derivation:

  $$\mathcal{H}(R_{tampered} \oplus K_{TPM}) \neq Seed_{PQ}$$

  The node mathematically locks itself out. The encrypted partitions remain sealed forever. The hardware defends its own integrity simply by existing.

---

## 3. The Raw Code: Memory-Safe PUF Key Derivation
We maintain our strict transition to memory-safe execution. This is the bare-metal logic for extracting the silicon entropy and deriving the Post-Quantum seed, written in `no_std` Rust to eliminate buffer overflow vectors during cryptographic initialization.

```rust
#![no_std]

use ebony_hal::crypto::{SramPuf, ErrorCorrection, Hash, MlKem1024};
use ebony_hal::tpm::TpmInterface;

// RT-PREEMPT Cryptographic Initialization (Pure no_std Rust)
pub fn derive_post_quantum_root_of_trust(tpm: &mut TpmInterface) -> Option<[u8; 32]> {
    
    // 1. Extract the raw microscopic variations from the uninitialized SRAM
    let raw_puf_response = SramPuf::read_uninitialized_block();

    // 2. Apply Error Correction to stabilize thermal and voltage noise
    let stable_puf_response = ErrorCorrection::decode(&raw_puf_response);

    if stable_puf_response.is_err() {
        // FATAL: The silicon capacitance has shifted significantly. 
        // This indicates physical tampering, extreme temperature variance, or decapsulation.
        return None; 
    }

    // 3. Retrieve the localized hardware secret from the TPM
    let tpm_key = tpm.read_hardware_secret();

    // 4. Derive the Post-Quantum Seed (Seed = Hash(PUF XOR TPM))
    let mut fused_entropy = [0u8; 64];
    for i in 0..64 {
        fused_entropy[i] = stable_puf_response.unwrap()[i] ^ tpm_key[i];
    }

    let pq_seed = Hash::sha3_256(&fused_entropy);

    // 5. Initialize the Lattice-Based ML-KEM-1024 Engine
    if MlKem1024::initialize_from_seed(&pq_seed).is_ok() {
        // Zeroize intermediate entropy buffers immediately
        fused_entropy.fill(0);
        return Some(pq_seed);
    }

    None // Cryptographic derivation mathematically failed
}
