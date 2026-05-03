use pqcrypto_kyber::kyber768;
use pqcrypto_dilithium::dilithium3;

// Correct import of the necessary traits for the pqcrypto ecosystem
use pqcrypto_traits::kem::SharedSecret as KemSharedSecret;
use pqcrypto_traits::sign::DetachedSignature as SignDetachedSignature;

fn main() {
    println!("--- Initializing PQC Prototyping in Rust ---");

    // --- 1. ML-KEM (Kyber768) ---
    let (pk, sk) = kyber768::keypair();
    let (ss_enc, ct) = kyber768::encapsulate(&pk);
    let ss_dec = kyber768::decapsulate(&ct, &sk);
    
    // Using the imported trait with an alias to avoid ambiguities
    assert_eq!(KemSharedSecret::as_bytes(&ss_enc), KemSharedSecret::as_bytes(&ss_dec));
    println!("[OK] ML-KEM (Kyber768) successfully tested.");

    // --- 2. ML-DSA (Dilithium3) ---
    let (pk_sign, sk_sign) = dilithium3::keypair();
    let msg = b"Data for quantum-resistant signature";
    
    let sig = dilithium3::detached_sign(msg, &sk_sign);
    let result = dilithium3::verify_detached_signature(&sig, msg, &pk_sign);
    
    assert!(result.is_ok());
    println!("[OK] ML-DSA (Dilithium3) successfully tested.");
}