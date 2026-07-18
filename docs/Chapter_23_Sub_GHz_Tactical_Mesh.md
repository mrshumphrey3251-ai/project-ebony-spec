# Chapter 23: The Sub-GHz Tactical Mesh – Cryptographic Anti-Spoofing

**Architect:** Jeffery Humphrey | CEO, Humphrey Virtual Farms  
**System:** Project Ebony (Evont)  
**Status:** Executable Logic, Cloud Deficient  

## The Vulnerability of Standard ADA Robotics
Current agricultural and ADA platforms rely on unencrypted radio frequencies (RF) or basic Wi-Fi for proximity and perimeter detection. This presents a catastrophic vulnerability. A bad actor equipped with a cheap Software-Defined Radio (SDR) can record a "stop" or "veto" signal and replay it indefinitely, triggering a remote Denial of Service (DoS) attack that effectively paralyses the machine in the field. 

## The Ebony Sovereign Mesh
Project Ebony treats all external radio traffic as a zero-trust environment. To prevent spoofing and replay attacks, the Evont architecture employs a **Cryptographically Signed Sub-GHz Tactical Mesh**.

Before a proximity alert from a personnel tag or rover is ingested by the Kinetic Guillotine, the mesh node processes an HMAC-SHA256 signature calculation. 

```python
# Project Ebony: Mesh Authentication Logic (Redacted)
def listen_and_verify():
    # Extracts the payload and the incoming signature
    raw_payload, received_signature = packet.split('|')
    
    # Generates a deterministic hash using the air-gapped sovereign key
    expected_signature = generate_signature(raw_payload)
    
    # Constant-time cryptographic comparison
    if hmac.compare_digest(expected_signature, received_signature):
        return raw_payload # Packet Authenticated. Proceed to Guillotine.
    else:
        return None # Spoof detected. Packet instantly dropped.
