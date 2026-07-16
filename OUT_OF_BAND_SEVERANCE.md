# KINETIC GOVERNANCE: Out-of-Band (OOB) Sub-GHz Severance

In heavy physical autonomy, software-based Emergency Stops are an illusion of safety. If an E-Stop relies on the primary operating system, a local Wi-Fi mesh, or a tablet application, it introduces multiple points of catastrophic failure. If the tablet dies, the operator cannot stop the machine.

Project Ebony utilizes an **Out-of-Band (OOB) Sub-GHz Severance** architecture.

* **Complete CPU Bypass:** The kill-switch logic does not run on the primary NVIDIA Jetson. It is executed by an isolated microcontroller wired directly to the main physical power contactors governing the hydraulics and drive motors.
* **Sub-GHz Radio Dominance:** The system listens on a dedicated 915MHz LoRa frequency. This low-frequency band punches through dense agricultural canopies, steel industrial structures, and bad weather far better than standard 2.4GHz Wi-Fi.
* **The Cryptographic Heartbeat:** The operator's handheld radio transmits a cryptographic pulse every 500 milliseconds. If the machine loses this heartbeat for more than 1 second (due to radio failure, range limits, or the operator dropping the transmitter), the microcontroller drops the power relays. The iron fails to a safe, dead state instantly.
