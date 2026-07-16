# KINETIC GOVERNANCE: Bare-Metal Inter-Process Communication (IPC)

When a localized DLA vision model identifies a target vector, that data must be routed to the physical actuators. Standard architectures accomplish this by running internal web servers (HTTP/REST) or generic network loops (TCP/IP). In heavy industry, network stack overhead introduces unacceptable latency spikes.

Project Ebony bypasses the networking layer entirely. 

* **UNIX Domain Sockets (UDS):** The vision intelligence node and the physical execution node communicate exclusively via raw UNIX Domain Sockets. The data never hits a virtual network interface; it passes directly through the operating system's kernel memory space.
* **Sub-Millisecond Execution:** Because the IPC bridge is written in bare-metal C++ and stripped of TCP/IP headers, routing, and checksum overhead, the latency between "seeing" a row crop and "moving" the physical linkage is effectively reduced to the speed of the Jetson's internal bus.
* **Absolute Isolation:** A UDS socket operates as a local file (`/tmp/ebony_kinetic.sock`). It is mathematically impossible for an external network payload to inject malicious steering commands into this socket without breaking the local file permissions of the Linux kernel.
