# CBRN_SENSING_MATRIX: Ambient Ionization & Volatile Telemetry Fusion

**Classification:** Gated Engineering Documentation / Environmental Sensor Layer
**Target Architecture:** Geiger-Müller Arrays / PID Sensors / I2C / RT-PREEMPT

This specification handles the continuous ingestion, baseline normalization, and deterministic threshold tracking of ambient radiological, particulate, and electrochemical air quality monitors. Project Ebony nodes operate in unpredictable kinetic environments where hostile actors or industrial failures may introduce lethal airborne agents. The localized edge node must definitively detect and classify these threats natively to trigger the `CBRN_FILTRATION_CONTROL.md` containment loops without remote API dependencies.

## 1. Radiation & Ionization Sensing
Radiological detection requires sub-second latency. The system ingests raw pulse telemetry directly via isolated hardware interrupts, bypassing standard polling delays.

* **Geiger-Müller Interface:** High-voltage Geiger-Müller (GM) tubes are wired directly to the Jetson Orin's GPIO pins configured for hardware-level edge detection. 
* **Native Dose Rate Compute:** The C++ runtime counts the raw ionizing pulses (Counts Per Minute, or CPM) over a discrete hardware timer interval. It dynamically calculates the absolute ambient dose equivalent rate $H(t)$ (in $\mu\text{Sv/hr}$) natively on the silicon:
  $$H(t) = C_f \left( \frac{dN}{dt} \right) + H_{bg}$$
  *(Where $C_f$ is the specific GM tube calibration factor, $\frac{dN}{dt}$ is the instantaneous pulse rate, and $H_{bg}$ is the hardware-calibrated cosmic background noise).*
* **Deterministic Thresholding:** If $H(t)$ violently breaches the operational safety limits, the RT-PREEMPT kernel immediately preempts all active computational threads to execute the mechanical sealing cascades.

## 2. Electrochemical & Gas-Phase Chromatography Arrays
Detecting Chemical Warfare Agents (CWAs) or volatile toxic compounds (VOCs) requires high-resolution analog ingestion and complex matrix parsing.

* **PID & Electrochemical Ingestion:** The node utilizes localized Photoionization Detectors (PIDs) and solid-state electrochemical sensors connected via isolated I2C and high-speed 16-bit ADCs.
* **Spectral Matrix Parsing:** The telemetry arrays are processed via INT8-quantized edge models running on the DLA cores. The system evaluates the voltage transients across the multi-gas array to identify specific chemical agent signatures (e.g., organophosphates or blister agents), isolating the hazardous compounds from standard industrial diesel exhaust or agricultural methane.

## 3. Baseline Normalization Dynamics & Anomaly Detection
Ambient environmental telemetry fluctuates naturally based on barometric pressure, humidity, and operational altitude. A rigid, hardcoded threshold will result in false positives, triggering unneeded filtration and wasting battery reserves.

* **Dynamic EWMA Baselines:** The node computes a running environmental baseline locally using an Exponentially Weighted Moving Average (EWMA). For any given sensor input $x_t$, the dynamic mean $\mu_t$ and variance $\sigma_t^2$ are continuously updated:
  $$\mu_t = \alpha x_t + (1 - \alpha) \mu_{t-1}$$
  $$\sigma_t^2 = \alpha (x_t - \mu_t)^2 + (1 - \alpha) \sigma_{t-1}^2$$
  *(Where $\alpha$ is the decay factor determining the memory length of the physical environment).*
* **Z-Score Trigger Activation:** To distinguish a legitimate chemical or radiological spike from natural drift, the system calculates the real-time Z-score:
  $$Z_t = \frac{|x_t - \mu_t|}{\sqrt{\sigma_t^2}}$$
  If $Z_t$ exceeds the predefined critical statistical boundary ($Z_{critical}$), the telemetry is flagged as a mathematically verified anomaly, instantly initiating the SCADA isolation relays.
