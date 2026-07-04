# KINETIC_GOVERNANCE: Infrared Surveillance & Thermal Processing

**Classification:** Project Ebony / Spatial Awareness Layer  
**Target Architecture:** LWIR / MIPI CSI-2 / RT-PREEMPT / Sub-GHz Mesh  

This document outlines the low-latency ingestion of Long-Wave Infrared (LWIR) camera matrices, localized threshold slicing, and cold-body tracking under zero-light conditions. Thermal anomaly detection cannot wait for network buffering or cloud-based video inference. To guarantee perimeter supremacy, the edge node must bypass standard software encoding, ingest raw thermal matrices natively at the hardware level, and distribute coordinate vectors across localized radio meshes without ever touching TCP/IP.

## Nomenclature & Acronym Glossary

| Term | Definition | Context |
| :--- | :--- | :--- |
| **DMA** | Direct Memory Access | Silicon-level data ingestion bypassing CPU overhead. |
| **LWIR** | Long-Wave Infrared | Thermal imaging spectrum capable of detecting human/mechanical heat signatures in total darkness. |
| **MIPI CSI-2** | Camera Serial Interface | High-speed, bare-metal bus protocol for directly piping camera sensor data to the processor. |
| **RT-PREEMPT** | Real-Time Preemption | Strict Linux kernel patch guaranteeing microsecond scheduling determinism. |
| **Sub-GHz Mesh** | Low-Frequency Radio | Resilient, localized RF communication (e.g., LoRa, FSK) operating below 1 GHz for long-range, non-IP telemetry. |

---

## 1. Edge-Native Thermal Ingestion
Standard IP cameras introduce fatal latency by compressing video into software streams. Project Ebony physically routes thermal data straight into the silicon.

* **MIPI CSI Bus Alignment:** Raw, uncompressed thermal camera streams are piped directly into local hardware video processing units via the MIPI CSI-2 bus. Using Direct Memory Access (DMA), the system maps the thermal frame buffers directly into zero-copy kernel memory, entirely bypassing the CPU's standard networking and application layers.
* **Localized Intensity Slicing:** To isolate a human or mechanical heat signature from ambient thermal noise, the node executes high-speed mathematical threshold checks natively on the pixel arrays. Letting the intensity of a given pixel be $I_{(x,y)}$ and the dynamic background noise threshold be $T_{bg}$, the kernel isolates the target matrix ($S_{target}$) using a localized standard deviation ($\sigma$):

  $$T_{bg} = \mu_{ambient} + (k \cdot \sigma_{ambient})$$
  $$S_{target} = \{ I_{(x,y)} \mid I_{(x,y)} > T_{bg} \}$$

  If a pixel cluster mathematically breaches the ambient threshold $T_{bg}$, it is instantly classified as a kinetic entity.

---

## 2. Spatial Direction Mapping
Once a thermal target is acquired, the node does not send a JSON payload to a central server. It relies on decentralized, bare-metal radio propagation.

* **Bit-Packed Telemetry:** The identified heat signatures and their vector trajectories are stripped of all software bloat and compiled into ultra-dense, bit-packed coordinate messages (typically 4 to 8 bytes in total length). 
* **Sub-GHz Propagation:** These raw coordinates are instantly blasted over localized sub-GHz radio frequencies to adjacent mesh nodes. This ensures that even if the primary Ethernet or cellular network is jammed or severed, the physical perimeter grid maintains absolute spatial awareness of the target's trajectory.

---

## 3. The Raw Code: Thermal Slicing & Mesh Propagation
This is the bare-metal execution loop for thermal tracking. It ingests the raw MIPI CSI arrays, computes the thermal threshold, packs the bits, and fires the telemetry across the SPI radio interface in pure C.

```c
#include <linux/dma-mapping.h>
#include <linux/spi/spi.h>
#include <linux/types.h>

// RT-PREEMPT Thermal evaluation loop (Pure C Kernel Space)
bool process_thermal_matrix(dma_addr_t mipi_csi_base, struct spi_device *subghz_radio) {
    u8 thermal_frame[LWIR_FRAME_SIZE];
    
    // 1. Zero-Copy Ingestion: Pull raw LWIR pixel array via MIPI CSI DMA
    read_physical_block(mipi_csi_base, thermal_frame, sizeof(thermal_frame));
    
    u16 target_x, target_y;
    
    // 2. Localized Intensity Slicing (Threshold Math)
    // Mathematically separates localized heat signatures from ambient noise
    bool target_acquired = execute_intensity_slice(thermal_frame, AMBIENT_NOISE_FLOOR, &target_x, &target_y);
    
    if (target_acquired) {
        
        // 3. Spatial Direction Mapping: Bit-pack coordinates (X, Y, Hostile Flag)
        u32 packed_telemetry = (target_x << 16) | (target_y << 8) | KINETIC_FLAG_HOSTILE;
        
        // 4. Distribute to adjacent nodes via Sub-GHz SPI Radio (No TCP/IP overhead)
        if (spi_write(subghz_radio, (u8*)&packed_telemetry, sizeof(packed_telemetry)) != 0) {
            trigger_hardware_fault(subghz_radio->chip_select, "FATAL: MESH_RADIO_FAILURE");
            return false;
        }
        
        // Target acquired and successfully gossiped to the mesh
        return true; 
    }

    return true; // Sector clear, ambient temperatures nominal
}
