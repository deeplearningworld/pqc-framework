# test_pqc.py
from oqs import Signature

def test_mldsa_signature():
    # Initialize the ML-DSA-65 algorithm (corresponds to Dilithium3)
    sig = Signature("ML-DSA-65")
    
    # Generate keypair
    public_key = sig.generate_keypair()
    
    # Sign message
    message = b"Data for quantum-resistant signature"
    signature = sig.sign(message)
    
    # Verify signature
    is_valid = sig.verify(message, signature, public_key)
    
    if is_valid:
        print("[OK] ML-DSA-65 successfully verified in Python.")
    else:
        print("[ERROR] Validation failed.")

if __name__ == "__main__":
    test_mldsa_signature()