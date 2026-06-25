# Disaster Recovery & System Re-Initialization Specification

This specification handles the localized cold-restore sequences, backup snapshot mount rules, and bare-metal recovery handshakes.

## 1. Localized Bare-Metal Restores
* **Air-Gapped Recovery Media:** Authorizes full system re-flashes directly from authenticated local hardware storage keys after local biometric token validation is achieved.
* **LUKS2 Backup Re-Mounting:** Decrypts and restores local operational configurations securely using keys stored inside the node's dedicated physical TPM 2.0 block.

## 2. Peer-Driven State Sync
* Upon successful re-initialization, the recovered node queries adjacent mesh vertices over sub-GHz channels to download and verify the current consensus network state map.
