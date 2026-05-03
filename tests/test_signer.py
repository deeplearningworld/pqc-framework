import pytest
from unittest.mock import MagicMock, patch
from src.python.manifest_signer import hash_file, sign_manifest

# Test the hashing logic (does not require C++)
def test_hash_file(tmp_path):
    d = tmp_path / "test.txt"
    d.write_text("Hello World")
    h = hash_file(d)
    assert len(h) == 64  # SHA-256 hash length

# Test the manifest logic using a Mock for the C++ library
@patch('src.python.manifest_signer.lib')
def test_sign_manifest_success(mock_lib, tmp_path):
    mock_lib.sign_data.return_value = 1 # Simulate C++ success
    d = tmp_path / "model.bin"
    d.write_bytes(b"dummy_weights")
    
    # Run the function
    sign_manifest(str(d))
    
    # Assert the C++ function was called
    mock_lib.sign_data.assert_called_once()