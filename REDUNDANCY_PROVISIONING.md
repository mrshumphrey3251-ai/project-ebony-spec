# KINETIC_GOVERNANCE: Hardware Redundancy Provisioning & Failover

**Classification:** Project Ebony / Fault Tolerance Layer  
**Target Architecture:** Hot-Standby / Galvanic Matrix / RT-PREEMPT / Hardware Watchdog  

This specification outlines the hot-standby node synchronization configurations, split-brain mitigation policies, and immediate physical relay switchover tracks. In critical kinetic environments, software-based high availability (HA) clusters like Corosync or Pacemaker are too slow and inherently reliant on the TCP/IP stack. True cyber-physical failover must execute in milliseconds at the silicon level. The standby node must continuously mirror the operational state and, upon primary death, violently seize physical control of the industrial buses via hardware relays.

## Nomenclature & Acronym Glossary

| Term | Definition | Context |
| :--- | :--- | :--- |
| **Galvanic Matrix** | Hardware Relay Array | A physical array of Solid-State Relays (SSRs) used to electronically sever or connect compute nodes to mechanical buses. |
| **Hot-Standby** | 1:1 Redundancy | A secondary node that is fully powered, actively mirroring the primary's memory, and ready to take control instantly. |
| **RT-PREEMPT** | Real-Time Preemption | Strict Linux kernel patch guaranteeing microsecond scheduling determinism. |
| **Split-Brain** | Desynchronization | A catastrophic cluster failure where both nodes believe they are the Master, attempting to actuate the same physical buses simultaneously. |
| **Watchdog** | Hardware Timer | A dedicated silicon timer that must be continuously reset by the primary node; failure to do so triggers a hard interrupt. |

---

## 1. Hot-Standby State Mirroring
To achieve a seamless mechanical transition, the secondary node must maintain absolute mathematical parity with the primary node's kinematic and thermodynamic state.

* **Synchronous Telemetry Mirroring:** The primary node continuously replicates its local engine state flags, PID controller values, and spatial tracking vectors to the standby unit. This is not done over Ethernet; it is executed over an isolated, high-speed physical link (e.g., direct SPI crossover or PCIe Non-Transparent Bridging) to ensure zero-latency DMA replication.
* **Active Heartbeat Auditing:** The standby node monitors the primary node's health via direct microsecond-interval GPIO pulse lines. Let $H_n$ be the timestamp of the $n$-th heartbeat pulse, and $\tau_{critical}$ be the absolute maximum allowable processing delay of the primary node. The standby kernel natively evaluates the differential:

  $$H_n - H_{n-1} > \tau_{critical}$$

  If this threshold is breached, the primary node is mathematically classified as dead or locked in a catastrophic execution freeze.

---

## 2. Automated Switchover Execution
When the primary node dies, the standby node cannot simply start transmitting on the CAN or Modbus wires. If the primary node is merely hanging (and not electrically dead), it could wake up and transmit simultaneously, causing a split-brain collision that will mechanically shred the asset.

* **Hardware-Enforced Split-Brain Mitigation:** Before the standby node assumes control, it must physically blind the primary node. It triggers a localized electronic relay matrix to galvanically isolate the primary node's transmit (TX) pins from the shared industrial buses. 
* **Millisecond Bus Seizure:** Once the primary is physically severed from the powertrain, the standby node actuates its own TX relays, closing the circuit. The entire transition ($T_{switch}$) is strictly bounded by the heartbeat detection time ($t_{detect}$) and the relay actuation time ($t_{actuate}$):

  $$T_{switch} = t_{detect} + t_{actuate} \le 5\text{ms}$$

  This guarantees that the master physical bus control (CAN/Modbus/J1939) is cleanly shifted to the secondary unit without dropping a single mechanical control frame.

---

## 3. The Raw Code: Heartbeat Auditing & Relay Seizure
This is the bare-metal execution loop for hardware redundancy. The standby kernel audits the primary's silicon pulse, physically severs the primary upon timeout, and seizes the master buses natively in pure C.

```c
#include <linux/gpio.h>
#include <linux/time.h>
#include <linux/types.h>

// RT-PREEMPT Failover Loop (Executed natively on the Standby Node)
bool audit_primary_node_health(u64 last_heartbeat_timestamp) {
    
    u64 current_hardware_tick = get_hardware_timer_microseconds();
    
    // 1. Active Heartbeat Auditing (Microsecond Precision)
    u64 pulse_differential = current_hardware_tick - last_heartbeat_timestamp;

    if (pulse_differential > MAX_HEARTBEAT_TIMEOUT_USEC) {
        
        // FATAL: Primary node has locked, panicked, or lost physical power.
        log_hardware_fault("FATAL: PRIMARY_NODE_SILENT. INITIATING KINETIC FAILOVER.");

        // 2. Split-Brain Mitigation (Galvanic Isolation)
        // Instantly drop the SSRs connecting the Primary Node to the CAN/Modbus network
        write_physical_register(PRIMARY_CAN_TX_RELAY, 0x00);
        write_physical_register(PRIMARY_MODBUS_TX_RELAY, 0x00);

        // 3. Automated Switchover Execution
        // Actuate Standby SSRs to physically seize the mechanical control buses
        write_physical_register(STANDBY_CAN_TX_RELAY, 0x01);
        write_physical_register(STANDBY_MODBUS_TX_RELAY, 0x01);

        // 4. Elevate Standby Node to Master Status
        elevate_node_to_master_state();
        
        // Execute seamless resumption of kinetic operations
        return true; 
    }

    // Primary node heartbeat is nominal. Remain in hot-standby shadow mode.
    return true; 
}
