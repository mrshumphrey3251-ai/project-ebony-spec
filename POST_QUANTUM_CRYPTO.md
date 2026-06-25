# Post-Quantum Cryptography & Key Encapsulation Specification

This document outlines the implementation parameters for ML-KEM (FIPS 203) and ML-DSA (FIPS 204) algorithms protecting air-gapped node communications.

## 1. Lattice-Based Key Encapsulation
* **ML-KEM-1024 Parameter Sets:** Enforces the highest security category for asymmetric key exchange, safeguarding local mesh session setup against future quantum computing decryption capabilities.
* **Ephemeral Session Ratcheting:** Generates fresh lattice-based key pairs for every discrete burst-transmission block, ensuring forward secrecy across contested spectrum lines.

## 2. Post-Quantum Digital Signatures
* Authenticates firmware updates and high-privilege configuration overrides using ML-DSA-85 signed tokens verified locally inside secure execution layers.
