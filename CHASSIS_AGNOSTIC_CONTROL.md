# KINETIC GOVERNANCE: Chassis-Agnostic Kinematics

True physical autonomy cannot be hardcoded to a single chassis type. The intelligence layer must remain entirely decoupled from the physical locomotion layer.

Project Ebony utilizes a **Kinematic Translation Matrix** to allow the exact same NVIDIA Jetson edge node to govern entirely different physical machines simply by updating a JSON configuration file.

* **Ackermann Steering (Legacy Tractors):** The matrix maps the vision vector directly to a single linear actuator governing the physical steering column (e.g., an Allis Chalmers G retrofit).
* **Differential Drive (Skid-Steer Rovers):** For rovers utilizing tank-steering (independent left/right wheel drives), the matrix intercepts the vision vector and splits it using standard differential kinematics: $V_{left,right} = v \mp \frac{\omega \cdot L}{2}$.
* **Hardware Independence:** The upstream object detection and spatial mapping neural networks do not need to know *how* the machine moves. They only output the required spatial vector. The bare-metal C++ Kinematic Translator handles the physical distribution, ensuring the AI never has to recalculate basic mechanical physics.
