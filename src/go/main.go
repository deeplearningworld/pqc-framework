package main

import (
	"crypto/rand"
	"fmt"
	"log"

	"github.com/cloudflare/circl/kem/kyber/kyber768"
	"github.com/cloudflare/circl/sign/mldsa/mldsa65"
)

func main() {
	fmt.Println("--- Initializing PQC Prototyping in Go (ML-DSA / FIPS 204) ---")

	// --- 1. ML-KEM ---
	scheme := kyber768.Scheme()
	pk, sk, _ := scheme.GenerateKeyPair()
	ct, ssEnc, _ := scheme.Encapsulate(pk)
	ssDec, _ := scheme.Decapsulate(sk, ct)

	if string(ssEnc) == string(ssDec) {
		fmt.Println("[OK] ML-KEM (Kyber768) tested.")
	}

	// --- 2. ML-DSA-65 (FIPS 204) ---
	pkSign, skSign, err := mldsa65.GenerateKey(rand.Reader)
	if err != nil {
		log.Fatalf("KeyGen Error: %v", err)
	}

	msg := []byte("Data for quantum-resistant signature")
	ctx := []byte("") // Empty context as per FIPS 204

	// Creating a buffer for the signature (fixed size per schema)
	sig := make([]byte, 3309) // ML-DSA-65 signature size

	err = mldsa65.SignTo(skSign, msg, ctx, true, sig)
	if err != nil {
		log.Fatalf("Signing error: %v", err)
	}

	if mldsa65.Verify(pkSign, msg, ctx, sig) {
		fmt.Println("[OK] ML-DSA-65 (FIPS 204) successfully tested.")
	} else {
		log.Fatal("Signature verification failed!")
	}
}
