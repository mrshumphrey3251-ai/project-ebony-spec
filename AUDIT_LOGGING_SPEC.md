# Tamper-Evident Audit Logging Specification

This specification documents the cryptographically chained, append-only local event log system.

## 1. Sequential Block Chaining
* **Cryptographic Event Links:** Every local system state log, mechanical override, and hardware authorization is cryptographically linked to the previous log entry hash.
* **Hardware-Assisted Signatures:** Log entries are signed instantly by the hardware root of trust using keys held securely inside the local TPM 2.0 enclave.

## 2. Tamper Detection Loops
* Continuous hardware audit daemons compare current cryptographic state hashes against sealed boot blocks to instantly trigger localized system alerts if out-of-order logs are written.
