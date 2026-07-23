# HVF STAGE 2 PUBLIC ARCHITECTURAL REQUIREMENTS
**Classification:** PUBLIC DOCTRINE / VENDOR-NEUTRAL SPECIFICATION
**Mandate:** Defines vendor requirements for Sub-GHz mesh interoperability and hardware GPIO abstraction.

---

## 1. PEER MESH INTEROPERABILITY (PROTOCOL EPSILON)
External machines operating the Ebony interface standard must support decentralized, un-routed Sub-GHz packet handling. Units must be capable of receiving and relaying signed intrusion frames without relying on external cellular or satellite infrastructure.

## 2. HARDWARE ABSTRACTED INTERLOCKS
Target hardware platforms must expose hardware-level GPIO control lines or bus-disconnect contactors that can be bound directly to the Ebony kinetic interlock protocol within 10 milliseconds of intrusion detection.
