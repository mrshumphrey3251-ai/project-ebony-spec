# PROJECT EBONY: KINETIC RAMPING & VARIABLE SPEED LOGIC
**Classification:** PRIVATE / INTERNAL ARCHITECTURE  
**Platform:** NVIDIA Jetson Orin (Rust Bare-Metal NLP to PWM)  
**Mandate:** Prevent Mechanical Shock, Enforce Deterministic Braking

---

## 1. NLP VARIABLE EXTRACTION
*Rule: Voice intents must parse both Vector (Direction) and Velocity (Speed). Default to safe parameters if Velocity is null.*

* **Input String:** `"ebony execute forward drive speed fifty"`
* **Parsing Logic:**
  * `Vector` = Forward (Positive Y-Axis threshold)
  * `Velocity` = 50%
* **Safety Null:** If command is `"ebony execute forward drive"`, `Velocity` defaults to 10% (Creep Mode).

## 2. THE PWM TO ANALOG CONVERSION MATH
*Rule: Jetson Orin digital pins use Pulse Width Modulation (PWM) bridged through a Low-Pass RC Filter to spoof analog joystick voltage ($V_{out}$).*

The baseline formula for calculating the filtered output voltage from the duty cycle ($D$) and the logic high voltage ($V_{cc}$, typically 5V) is:
$$V_{out} = D \times V_{cc}$$

**The Hardcoded Voltage Map:**
* **Deadzone (Zero Kinetic):** 50% Duty Cycle $\rightarrow$ `2.5V Output`
* **10% Speed (Creep):** 54% Duty Cycle $\rightarrow$ `2.7V Output`
* **50% Forward Speed:** 70% Duty Cycle $\rightarrow$ `3.5V Output`
* **100% Forward Speed:** 90% Duty Cycle $\rightarrow$ `4.5V Output`
* **100% Reverse Speed:** 10% Duty Cycle $\rightarrow$ `0.5V Output`

## 3. THE KINETIC RAMPING PROTOCOL (SLEW RATE)
*Rule: Never instantly jump from 2.5V to target voltage. A software slew rate loop must be utilized to simulate physical joystick throw and protect the 24V gearboxes.*

* **Execution:** Rust `for` loop stepping the PWM duty cycle over time ($\Delta t$).
* **Parameters:** * `Step Size:` +0.1V increments.
  * `Delay Interval:` 50 milliseconds per step.
* **Result:** Reaching 100% speed (4.5V) from Deadzone (2.5V) takes approximately 1.0 second, eliminating torque shock to the differential drive payload.

## 4. EMERGENCY OVERRIDE (ZERO SLEW)
*Rule: Deceleration during an operator interrupt must bypass all ramping parameters.*

* **Trigger:** Push-To-Talk (PTT) GPIO pin goes `LOW` OR voice command `"ebony halt"` is parsed.
* **Execution:** Slew rate loop is instantly terminated. PWM Duty Cycle reverts to exactly 50% (2.5V) in $<5$ milliseconds. Factory motor controller registers a zero-input and engages electromagnetic chassis brakes.
