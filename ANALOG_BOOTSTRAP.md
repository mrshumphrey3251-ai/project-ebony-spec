# ANALOG_BOOTSTRAP: Cold-Start Initialization & Hardware Sequencing

**Classification:** Gated Engineering Documentation / Analog Hardware Layer
**Target Architecture:** Low-Power MCU / Power-On Reset (POR) Circuitry

This specification details the cold-start hardware initialization and physical fallback configuration sequences. Project Ebony assumes the primary compute module (Jetson Orin) is fundamentally untrusted at $T=0$. The system relies on a strictly isolated, low-power analog bootstrap sequence to verify electrical integrity before the primary CPU is permitted to draw power.

## 1. Zero-State Power-On & Analog Isolation
When physical power is applied to the chassis, the primary compute architecture remains mechanically isolated from the power rails.

* **Isolated Boot Strapping:** A dedicated, low-power physical microcontroller (MCU) initializes directly from immutable, hardware-level ROM. This MCU operates completely independently of the primary Jetson processor.
* **Power-On Reset (POR) Delay:** To defend against voltage-glitching and fault-injection attacks, the analog circuitry enforces a strict, un-bypassable hardware delay to guarantee power rail stability. The threshold voltage rise time is mathematically bounded by the RC time constant of the isolation circuit:
  $$V(t) = V_{DD} \left(1 - e^{-\frac{t}{RC}}\right)$$
  The MCU will not begin execution until $V(t)$ stabilizes strictly within a $1\%$ tolerance of the target logic voltage for a continuous $50 \text{ ms}$ window.

## 2. Hardware Self-Test (POST) & Clock Verification
Before the primary compute node is allowed to wake, the MCU must establish absolute physical state values.

* **Peripheral Impedance Checks:** The MCU natively checks local peripheral voltages, CAN bus termination resistor impedance, and hydraulic manifold sensor continuity.
* **Oscillator Lock Verification:** The system verifies the primary quartz oscillators have achieved Phase-Locked Loop (PLL) stability, ensuring the primary CPU cannot be booted into an overclocked or underclocked state that could disrupt the deterministic execution limits defined in `CORE_ENGINE.md`.

## 3. Boot Security Anchoring & Handoff
Once the electrical baseline is mathematically proven, the MCU prepares to wake the primary architecture.

* **Hardware-Fused Anchoring:** The MCU validates its own first-stage boot image cryptographic signatures locally against hardware-fused public keys held inside its discrete secure element.
* **Compute Wake Sequence:** If, and only if, the analog telemetry and cryptographic hashes pass, the MCU asserts the hardware `SYS_RESET_N` pin, delivering power to the Jetson Orin to begin the UEFI boot sequence and TPM 2.0 handshake (as detailed in `SECURE_BOOT.md`). If the analog bootstrap fails, the system triggers the mechanical tamper response, severing all solid-state relays.
