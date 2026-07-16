# KINETIC GOVERNANCE: Bare-Metal PID Physics Engine

Retrofitting legacy agricultural iron (e.g., an 80-year-old Allis Chalmers G) with autonomous capability requires extreme mechanical empathy. You cannot apply binary voltage (100% ON or OFF) to decades-old steering linkages; it will snap the metal.

Project Ebony utilizes a locally executed Proportional-Integral-Derivative (PID) matrix written in C++ to act as a physical shock-absorber.

* **The Mathematical Governor:** The algorithm continuously calculates the error $e(t)$ between the machine's current trajectory and the target vector provided by the DLA vision node. The physical voltage output $u(t)$ is calculated natively in microseconds:
  $$u(t) = K_p e(t) + K_i \int_{0}^{t} e(t) d\tau + K_d \frac{de(t)}{dt}$$
* **Dynamic Modularity:** The tuning variables ($K_p$, $K_i$, $K_d$) are not hardcoded. They are ingested from a localized JSON ledger, allowing operators to add entirely new types of machinery to the fleet without rewriting the C++ execution logic.
* **Anti-Windup Constraints:** The system employs strict mathematical bounds on the Integral term. If a linear actuator becomes physically stuck in deep soil, the system will not blindly escalate voltage until the battery shorts or the iron breaks.
