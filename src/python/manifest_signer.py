import hashlib
import json
import ctypes
import argparse
import os
from pathlib import Path

# 1. Dynamic Pathing: Locate libpqccore relative to this script
BASE_DIR = Path(__file__).resolve().parent.parent
LIB_PATH = BASE_DIR / "libpqccore.so"

# Load library
try:
    lib = ctypes.CDLL(str(LIB_PATH))
except OSError as e:
    print(f"[ERROR] Could not load library at {LIB_PATH}: {e}")
    exit(1)

# 2. Define Argument Types for C++ ABI compatibility
# Expecting: int sign_data(const uint8_t* data, size_t len, uint8_t* sig_out)
lib.sign_data.argtypes = [ctypes.c_char_p, ctypes.c_size_t, ctypes.POINTER(ctypes.c_char)]
lib.sign_data.restype = ctypes.c_int

def hash_file(file_path: Path):
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def sign_manifest(model_path: str):
    file_path = Path(model_path)
    if not file_path.exists():
        print(f"Error: {model_path} not found.")
        return

    manifest = {
        "model_file": file_path.name,
        "hash": hash_file(file_path),
        "algorithm": "ML-DSA-65"
    }
    
    manifest_bytes = json.dumps(manifest).encode('utf-8')
    
    # 3. Buffer allocation: Prepare a buffer for the C++ signature
    # Assuming ML-DSA-65 signature size is 3309 bytes (FIPS 204 standard)
    sig_buffer = ctypes.create_string_buffer(3309)
    
    print(f"[INFO] Signing manifest for: {file_path.name}")
    
    # Call the adjusted C++ function
    result = lib.sign_data(manifest_bytes, len(manifest_bytes), sig_buffer)
    
    if result == 1:
        # Save manifest with the signature included
        manifest['signature'] = sig_buffer.raw.hex()
        with open(f"{file_path.name}.manifest", "w") as f:
            json.dump(manifest, f, indent=4)
        print("[OK] Manifest and signature saved.")
    else:
        print("[ERROR] Signing failed inside C++ core.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Supply Chain Signer")
    parser.add_argument("model", help="Path to the model file")
    args = parser.parse_args()
    sign_manifest(args.model)