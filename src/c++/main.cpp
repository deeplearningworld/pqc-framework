#include <iostream>
#include <vector>
#include <cstring>
#include <oqs/oqs.h>

extern "C" {
    // We use a fixed keypair for this demo; in production, 
    // load your secret key from a secure vault.
    int sign_data(const char* data, size_t len, char* sig_out) {
        
        // 1. Initialize OQS and Algorithm
        OQS_SIG *sig = OQS_SIG_new(OQS_SIG_alg_ml_dsa_65);
        if (sig == NULL) return 0; // Error

        // 2. Generate Keypair (In production, replace with loading a persistent key)
        uint8_t *public_key = (uint8_t *)malloc(sig->length_public_key);
        uint8_t *secret_key = (uint8_t *)malloc(sig->length_secret_key);
        if (OQS_SIG_keypair(sig, public_key, secret_key) != OQS_SUCCESS) {
            OQS_SIG_free(sig);
            return 0;
        }

        // 3. Perform Signing
        size_t signature_len;
        uint8_t *signature = (uint8_t *)malloc(sig->length_signature);
        
        if (OQS_SIG_sign(sig, signature, &signature_len, 
                         (const uint8_t*)data, len, secret_key) != OQS_SUCCESS) {
            free(signature);
            free(public_key);
            free(secret_key);
            OQS_SIG_free(sig);
            return 0;
        }

        // 4. Copy signature to the buffer provided by Python
        memcpy(sig_out, signature, signature_len);

        // 5. Cleanup
        free(signature);
        free(public_key);
        free(secret_key);
        OQS_SIG_free(sig);

        return 1; // Success
    }
}
