# Asset Recovery & Re-Provisioning Protocol Specification

This document defines the cryptographic handshake and safe physical steps required to restore an isolated asset to active operational status.

## 1. Manual Cryptographic Handshake
* **Physical Key Invalidation:** Re-provisioning an asset requires a direct, physical hardware connection via an air-gapped technician console utilizing an authenticated master key asset.
* **TPM 2.0 State Resealing:** Generates fresh cryptographic key blocks and seals them natively inside the local Trusted Platform Module after verifying core hardware integrity.

## 2. State Convergence Verification
* The recovered asset must run a full hardware self-test routine and successfully complete a read-only telemetry sync loop with adjacent mesh nodes before it is authorized to rejoin the control network.
