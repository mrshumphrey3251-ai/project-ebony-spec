# Secure Tunneling & Point-to-Point Layer Specification

This document details the low-overhead cryptographic encapsulation, packet whitening protocols, and point-to-point network tunneling layers for local mesh links.

## 1. Low-Overhead Cryptographic Encapsulation
* **ChaCha20-Poly1305 Stream Ciphers:** Encapsulates local mesh traffic inside lightweight, authenticated streaming envelopes optimized for processing on low-power edge compute silicon.
* **Packet Identity Whitening:** Modifies packet headers and prepends pseudo-random padding bytes to obfuscate traffic length signatures and prevent pattern analysis by external listeners.

## 2. Dynamic Point-to-Point Session Rekeying
* Rotates symmetric session keys automatically using ephemeral Diffie-Hellman handshakes after a strict time or packet-count limit is breached, maintaining forward secrecy.
