# PQC Interoperability & Validation (FIPS 204)

## Executive Summary
This repository provides a production-grade framework for implementing and validating Post-Quantum Cryptographic (PQC) digital signatures, specifically ML-DSA-65 (FIPS 204). Designed for heterogeneous environments, this project demonstrates how to maintain cryptographic uniformity across C++, Rust, Go, and Python, ensuring secure, interoperable, and quantum-resistant infrastructure.

## Technical Architecture
We utilize the liboqs (Open Quantum Safe) engine as the primary cryptographic provider, with language-specific wrappers and native implementations:

* **C++ (Core):** High-performance implementation focusing on low-level memory management and direct integration with liboqs.
* **Rust (Safety):** Implementation utilizing Rust’s type safety and memory-safety guarantees for secure cryptographic operations.
* **Go (Infrastructure):** Utilization of Go for concurrent service architecture and network-level cryptographic tasks.
* **Python (Orchestration):** Development of automated test suites and MLOps integration to streamline validation pipelines.

## Prerequisites
Ensure your build environment is configured with the following:

* **liboqs:** Built with `CMAKE_INSTALL_PREFIX`.
* **OpenSSL 3.x:** Required for AES-acceleration support.
* **Compilers/Runtimes:** `gcc` (12+), `rustc/cargo` (2021 edition), `go` (1.20+), `python` (3.10+).

## Implementation & Build Guide

| Language | Build Command | Use Case |
| :--- | :--- | :--- |
| **C++** | `g++ -I./include -L./lib main.cpp -o test-loqs` | Performance-critical core |
| **Rust** | `cargo run` | Memory-safe implementation |
| **Go** | `go run main.go` | Concurrent service integration |
| **Python** | `pip install liboqs && pytest` | Validation & Test Automation |

## Key Design Principles
* **Security Uniformity:** By centralizing the cryptographic core (liboqs), we ensure that ML-DSA-65 behaves consistently across the entire system.
* **Memory Robustness:** The project contrasts manual memory management (C++) with safe-abstraction models (Rust), allowing for fine-grained security auditing.
* **Standard Compliance:** All implementations follow NIST FIPS 204 guidelines, preparing the architecture for the transition to post-quantum standards.
* **Language Heterogeneity:** We leverage the specific strengths of each language to build a resilient, multi-layered security stack.

## Usage
1. **Initialize the Environment:** Ensure liboqs is compiled with `CMAKE_INSTALL_PREFIX` and configured according to the platform-specific instructions in the `scripts/` folder.
2. **Compile & Run:** Utilize the provided build scripts for each language to ensure the correct dynamic libraries are linked via `LD_LIBRARY_PATH` or `DYLD_LIBRARY_PATH`.

## Engineering Note
This repository is designed for production-readiness in environments requiring cryptographic agility. It serves as a benchmark for interoperability, proving that security standards can be maintained effectively even when distributed across polyglot microservices.

## License & Contributing
This project is licensed under the Apache-2.0. Contributions are welcome; please refer to the `CONTRIBUTING.md` file for code style guidelines and pull request procedures.
