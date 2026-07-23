#!/usr/bin/env python3
"""
HVF OPERATOR TERMINAL - PUBLIC VENDOR INTERFACE SPECIFICATION
Classification: PUBLIC DOCTRINE / VENDOR-NEUTRAL ARCHITECTURAL SPEC
Mandate: Defines command-plane interaction boundaries for external hardware vendors.
"""

from cage_router_interface_spec import PublicSubstrateInterface

class PublicOperatorTerminal:
    def __init__(self, interface_instance):
        self.interface = interface_instance
        self.terminal_status = "ACTIVE_PUBLIC_BOUNDARY"

    def request_vendor_access(self, register_addr, vendor_id):
        print(f"\n[PUBLIC_TERMINAL] Vendor {vendor_id} requesting access to {hex(register_addr)}...")
        try:
            res = self.interface.request_access(register_addr, vendor_id)
            print(f"[PUBLIC_TERMINAL] Access Granted: {res}")
            return res
        except PermissionError as e:
            print(f"[PUBLIC_TERMINAL] ACCESS DENIED: {e}")
            return {"status": "SEVERED", "error": str(e)}

if __name__ == "__main__":
    print("--> Initializing Public Vendor Terminal Interface...")
    pub_interface = PublicSubstrateInterface()
    pub_term = PublicOperatorTerminal(pub_interface)
    pub_term.request_vendor_access(0x1000, "CERTIFIED_VENDOR_01")
    pub_term.request_vendor_access(0x4000, "UNAUTHENTICATED_VENDOR_99")
    print("\n--> Public interface test complete. Zero-trust boundaries enforced.")
