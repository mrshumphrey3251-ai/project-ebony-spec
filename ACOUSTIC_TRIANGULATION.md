# ACOUSTIC_TRIANGULATION: GPS-Denied TDOA Localization & DSP Matrix

**Classification:** Gated Engineering Documentation / Sensor Fusion Layer
**Target Architecture:** I2S MEMS Arrays / RT-PREEMPT Kernel

This specification defines the bare-metal, passive acoustic event localization matrix. In GPS-denied or highly spoofed environments, Project Ebony nodes utilize decentralized hardware microphone arrays and strictly local digital signal processing (DSP) to triangulate kinetic events, mechanical fractures, and structural compromises without external reference beacons.

## 1. Hardware Ingestion & DMA PDM/I2S Streams
Standard USB audio interfaces introduce unacceptable bus polling jitter. Acoustic ingestion for kinetic localization must be deterministic.

* **Direct Memory Access (DMA):** Multi-channel MEMS microphone arrays are wired directly to the Jetson Orin’s I2S hardware buses. The audio payload bypasses the CPU via DMA, writing directly to pre-allocated zero-copy ring buffers.
* **Priority Execution:** Native ALSA (Advanced Linux Sound Architecture) drivers are bound to the `SCHED_FIFO` real-time pool (see `SECURE_BOOT.md`). This guarantees that high-frequency acoustic sample rates ($48 \text{ kHz}$ to $96 \text{ kHz}$) are captured synchronously without a single dropped frame, even under maximum Deep Learning Accelerator (DLA) load.

## 2. DSP & Time-Difference-of-Arrival (TDOA) Mechanics
To localize a sound source in physical space, the system relies on exact arrival time deltas across spatially distributed nodes.

* **Cross-Correlation Matrix:** The localized DSP pipeline isolates target acoustic signatures (e.g., a high-pressure hydraulic line rupture or structural impact) via aggressive bandpass filtering. To find the time delay $\tau$ between two nodes, the system calculates the discrete cross-correlation natively on the edge-silicon:
  $$R_{xy}[n] = \sum_{m=-\infty}^{\infty} x[m] y[m+n]$$
* **Hyperbolic Intersection:** The peak of $R_{xy}[n]$ yields the exact Time-Difference-of-Arrival (TDOA). The physical distance difference is calculated as $\Delta d = c \cdot \tau$ (where $c$ is the speed of sound, adjusted dynamically via local ambient temperature and barometric sensors). Grid coordinates are computed by solving the mathematical intersection of the resulting hyperbolas.

## 3. Mesh-Distributed Localization
A single node cannot triangulate an event in 3D space alone. The localization matrix is fundamentally decentralized across the physical fleet.

* **Micro-Second Synchronization:** Accurate TDOA requires absolute time synchronization across fractured fleets. Nodes sync their internal hardware clocks via sub-GHz mesh gossiping, achieving $< 10 \text{ \mu s}$ variance.
* **FlatBuffer Telemetry:** Instead of transmitting heavy raw audio files, a node simply broadcasts the compressed acoustic signature hash and its exact microsecond timestamp via fixed-width payloads (see `FLATBUFFER_SERIALIZATION.md`). Adjacent nodes cross-reference this timestamp with their own internal captures to complete the hyperbolic geometry offline.

## 4. Adaptive Ego-Noise Cancellation
Heavy industrial machinery generates massive localized acoustic interference. The RT-PREEMPT kernel pipes raw RPM, hydraulic pressure, and track-speed telemetry directly from the J1939 CAN bus into an adaptive noise cancellation filter. The node dynamically subtracts its own mechanical baseline from the I2S stream in real-time, preventing its own actuator noise from blinding the TDOA matrix.
