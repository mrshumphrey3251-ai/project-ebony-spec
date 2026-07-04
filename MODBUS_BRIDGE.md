# KINETIC_GOVERNANCE: Modbus RTU-to-TCP Protocol Bridge Specification

**Classification:** Project Ebony / Legacy SCADA Integration Layer  
**Target Architecture:** RS-485 / Modbus TCP / RT-PREEMPT / CRC-16 Validation  

This specification handles the serial packet encapsulation, frame error check corrections, and register mapping configurations for legacy industrial SCADA hardware. Bridging unprotected RS-485 serial lines to modern IP networks creates a massive attack vector. The edge node must not blindly forward serial frames; it must act as a ruthless hardware boundary, mathematically interrogating every electrical pulse, discarding corrupted signals, and safely packing the surviving telemetry into deterministic network frames.

## Nomenclature & Acronym Glossary

| Term | Definition | Context |
| :--- | :--- | :--- |
| **Coil / Register** | Modbus Memory Map | Coils represent single-bit physical states (Relay ON/OFF). Registers hold 16-bit analog values (Pressure, Temp). |
| **CRC-16** | Cyclic Redundancy Check | A 16-bit error-detecting code used to verify the integrity of the raw serial transmission. |
| **Modbus RTU** | Remote Terminal Unit | The legacy binary serial protocol operating over two-wire RS-485 copper. |
| **Modbus TCP** | IP Encapsulation | The modern adaptation of Modbus, running over standard TCP/IP port 502. |
| **RS-485** | Serial Standard | The physical electrical standard used for long-distance, electrically noisy environments. |

---

## 1. Serial-to-Ethernet Framing
A corrupted serial frame traversing a loud industrial environment can easily flip a critical bit. If that flipped bit is forwarded to the TCP stack, it could inadvertently command a 50-ton hydraulic press to cycle. 

* **CRC Validation Auditing:** Before any encapsulation occurs, the edge node intercepts the legacy RS-485 Modbus RTU frame via Direct Memory Access (DMA). The RT-PREEMPT kernel automatically verifies the frame's Cyclic Redundancy Check (CRC-16) natively. The mathematical validation utilizes the standard generator polynomial $P(x)$:

  $$P(x) = x^{16} + x^{15} + x^2 + 1$$

  Let the incoming message block be $M(x)$. The kernel calculates the remainder $R(x)$ in real-time natively on the silicon:

  $$R(x) = M(x) \cdot x^{16} \pmod{P(x)}$$

  If $R(x) \neq 0$, the electrical signal has been corrupted by electromagnetic interference (EMI) or wire-tampering. The frame is instantly discarded at the hardware boundary layer.
* **Deterministic Packet Wrapping:** If the CRC is mathematically sound, the kernel strips the serial CRC bytes (which are unnecessary in TCP) and encapsulates the raw Address, Function Code, and Data payload into a standard Modbus TCP packet, preserving the internal register sequence flawlessly.

---

## 2. Industrial Register Address Maps
Once the payload is validated, the node must translate the legacy memory map into a format that the modern sub-GHz mesh and edge AI accelerators can process.

* **Bit-Packed Serialization:** The RTU-to-TCP bridge translates the physical coil state indices (Boolean arrays) and input registers (16-bit analog integers) directly into the bit-packed FlatBuffer schemas utilized by the rest of Project Ebony. 
* **State Preservation:** By mapping the legacy $0x0000$ (Coils) and $0x30000$ (Input Registers) memory blocks natively, the edge node seamlessly integrates 30-year-old physical infrastructure into the high-speed, zero-parse sub-GHz mesh without adding application-layer overhead.

---

## 3. The Raw Code: CRC Boundary Check & Encapsulation
This is the bare-metal reality of legacy protocol bridging. The kernel pulls the raw RS-485 frame, validates the polynomial math, and packs the TCP frame natively in pure C space.

```c
#include <linux/crc16.h>
#include <linux/types.h>

// RT-PREEMPT Modbus Bridge Loop (Pure C Kernel Space)
bool bridge_rtu_to_tcp(dma_addr_t rs485_base_addr, u8* tcp_payload_buffer) {
    
    u8 rtu_frame[256];
    
    // 1. Zero-Copy Ingestion: Pull raw RS-485 frame directly from serial silicon
    size_t frame_len = read_serial_dma_block(rs485_base_addr, rtu_frame);

    if (frame_len < 4) return false; // Incomplete frame

    // 2. Hardware CRC-16 Validation (Polynomial Execution)
    // Mathematically ensures electrical integrity before TCP mapping
    u16 computed_crc = crc16(0xFFFF, rtu_frame, frame_len - 2);
    u16 received_crc = (rtu_frame[frame_len - 1] << 8) | rtu_frame[frame_len - 2];

    if (computed_crc != received
