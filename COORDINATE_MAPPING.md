# CONSOLE_ALERTS: Priority Mitigation & Zero-Heap Rendering

**Classification:** Gated Engineering Documentation / Human-Machine Interface (HMI) Layer
**Target Architecture:** Wearable Display Terminals / RT-PREEMPT / Zero-Allocation Ring Buffers

This specification handles the categorization, UI rendering layers, and localized dispatching of high-priority hardware alerts. Project Ebony operators must receive instantaneous, deterministic notification of fatal mechanical faults, biometric breaches, or environmental hazards. The system must render these alerts natively, completely bypassing high-level operating system delays, and mathematically demand physical operator verification before muting kinetic alarm states.

## 1. Priority Categorization Engine & Deterministic Interrupts
Not all telemetry anomalies carry the same kinetic weight. The localized edge node must instantly categorize inbound metrics and preempt lower-level OS threads to prioritize fatal alerts.

* **Critical Path Interrupts:** The C++ runtime dynamically ingests system metrics and categorizes them into strict severity tiers. The system calculates the absolute Priority Index ($P_{index}$) natively for any incoming fault vector ($\vec{f}$):
  $$P_{index} = \max\left( \omega_1 f_{kinetic}, \omega_2 f_{bio}, \omega_3 f_{env} \right)$$
  *(Where $\omega$ represents the hardcoded severity weights for kinetic, biometric, and environmental fault states).* If $P_{index}$ breaches the fatal threshold, the RT-PREEMPT kernel maps the alert directly to a Non-Maskable Interrupt (NMI), instantly suspending background ML training (`EDGE_RETRAINING.md`) or standard mesh routing tasks.
* **Low-Latency Rendering Loops (Zero-Heap):** To guarantee the alert reaches the operator's Wearable Arm Device instantly, the system utilizes a strict zero-heap memory architecture. Dynamic memory allocation (`malloc()`) is mathematically forbidden in the alert path to prevent non-deterministic garbage collection latency. 
* **$O(1)$ Ring Buffer Execution:** Alerts are written directly to pre-allocated, fixed-size memory ring buffers. The display terminal's render loop reads from this buffer with $O(1)$ time complexity, guaranteeing a motion-to-photon render latency bounded perfectly to the hardware refresh cycle:
  $$t_{render} \le \frac{1}{f_{refresh}}$$
  This ensures the operator is visually notified of a catastrophic fault state in under 16 milliseconds, independent of total system load.

## 2. Local Operator Acknowledgment & Cryptographic Handshakes
A critical alarm on a heavy industrial asset cannot simply be "swiped away" like a standard mobile notification. Muting an active mechanical alarm state requires mathematical proof of authorized human presence.

* **Explicit Localized Confirmation:** To acknowledge and dismiss a $P_{index}$ fatal alert, the UI requires localized confirmation metrics (e.g., unique PIN entry or a biometric validation token routed from the TrustZone enclave).
* **HMAC Verification Handshake:** The wearable console generates a cryptographic payload binding the operator's input ($M_{token}$), the specific alert ID ($A_{id}$), and a strict temporal timestamp ($T_{stamp}$). The console computes a Hash-based Message Authentication Code (HMAC) using the session key ($K_{session}$) established during initial LOTO boot:
  $$V_{auth} = \text{HMAC}(K_{session}, M_{token} \parallel A_{id} \parallel T_{stamp})$$
* **Galvanic Alarm Severance:** This payload is blasted over the secure local sub-GHz link back to the primary edge node. If and only if the edge node mathematically verifies $V_{auth}$ and confirms $T_{stamp}$ falls within a strict 3-second replay-prevention window, the kernel drops the alarm state ($A_{state} \to 0$) and physically disengages the SCADA warning sirens via the localized relays.
