import os
import pytest
from src.python.manifest_signer import sign_manifest

def test_full_signing_flow(tmp_path):
    # Setup: Create a dummy model file
    model_file = tmp_path / "test_model.bin"
    model_file.write_bytes(b"model_weights_data")
    
    # Execute: Run the signer
    sign_manifest(str(model_file))
    
    # Verify: Check if the .manifest file was created
    manifest_path = model_file.with_suffix(".bin.manifest")
    assert manifest_path.exists()