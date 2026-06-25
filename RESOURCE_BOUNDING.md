# Resource Bounding & Deterministic CPU Scheduling Specification

This specification handles the hard real-time thread task configurations, Linux cgroup memory allocations, and hardwired watchdog bounds.

## 1. Hard Real-Time Thread Allocation
* **SCHED_FIFO Priority Isolation:** Binds safety-critical physical control and sensory parsing tasks to dedicated high-priority real-time kernel scheduling domains.
* **Static Memory Locking:** Locks all active process memory into physical RAM blocks (`mlockall`), preventing system page faults from disrupting time-sensitive execution paths.

## 2. Linux Cgroup Resource Restraints
* Constrains background data compression and analytics tasks inside rigid resource walls to guarantee they can never exhaust memory or compute cycles required by primary control loops.
