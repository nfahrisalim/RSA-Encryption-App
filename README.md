# 🔐 RSA Encryption/Decryption Web Application

A comprehensive RSA cryptography web application built with Streamlit that provides an interactive interface for understanding and implementing RSA encryption and decryption algorithms.

## 🌟 Features

- **Interactive RSA Key Generation**: Generate RSA key pairs with customizable prime numbers
- **Real-time Encryption/Decryption**: Encrypt and decrypt text messages with detailed step-by-step calculations
- **Educational Interface**: Comprehensive explanations of RSA mathematics and cryptographic processes
- **Multiple Input Modes**: Support for both text input and file upload
- **Character Set Flexibility**: Options for uppercase letters only or full ASCII character support
- **Mathematical Visualization**: Display encryption/decryption formulas and calculations
- **Data Export**: Download encrypted and decrypted results
- **Prime Number Generator**: Random prime number generation for testing
- **Parameter Validation**: Real-time validation of prime numbers and key parameters

## 🎯 Educational Value

This application is designed for educational purposes to help students and professionals understand:
- RSA algorithm fundamentals
- Public and private key cryptography
- Modular arithmetic and number theory
- Euler's totient function
- Extended Euclidean algorithm
- Fast modular exponentiation

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- pip or uv package manager

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nfahrisalim/RSA-Encryption-App.git
   cd RSA-Encryption-App
   ```

2. **Install dependencies using uv (recommended):**
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install streamlit pandas
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to `http://localhost:5000`

## 📋 Usage Guide

### 1. Setting Up RSA Parameters

- **Generate Random Primes**: Use the "Generate Random Primes" button for automatic prime generation
- **Manual Input**: Enter your own prime numbers p and q in the sidebar
- **Public Exponent**: Choose an appropriate value for e (common values: 3, 17, 257, 65537)

### 2. Key Generation Process

The application automatically calculates:
- **n = p × q** (modulus)
- **φ(n) = (p-1) × (q-1)** (Euler's totient function)
- **d** (private exponent, modular inverse of e mod φ(n))

### 3. Encryption and Decryption

- **Text Input**: Type your message directly or upload a text file
- **Character Support**: Choose between uppercase letters only or full ASCII support
- **Step-by-Step View**: See detailed calculations for each character
- **Export Results**: Download encrypted and decrypted files

### 4. Understanding the Mathematics

The application displays:
- **Encryption Formula**: c ≡ m^e (mod n)
- **Decryption Formula**: m ≡ c^d (mod n)
- **Key Verification**: e × d ≡ 1 (mod φ(n))

## 🔧 Technical Details

### Core Functions

- `gcd(a, b)`: Calculate greatest common divisor
- `mod_inverse(e, phi)`: Extended Euclidean algorithm for modular inverse
- `mod_exp(base, exp, mod)`: Fast modular exponentiation
- `is_prime(n)`: Prime number validation
- `encrypt_text()`: Text encryption with detailed logging
- `decrypt_text()`: Text decryption with detailed logging

### Security Features

- Input validation for prime numbers
- Automatic verification of key parameters
- Support for various text encodings
- Error handling for invalid inputs

## 📊 File Structure

```
RSA-Encryption-App/
├── app.py              # Main Streamlit application
├── pyproject.toml      # Project dependencies and metadata
├── uv.lock            # Dependency lock file
└── README.md          # Project documentation
```

## 🎨 User Interface

The application features:
- **Sidebar**: Parameter configuration and key generation
- **Main Panel**: Encryption/decryption interface with detailed explanations
- **Expandable Sections**: Mathematical details and process explanations
- **Data Tables**: Step-by-step calculation displays
- **Download Buttons**: Export functionality for results

## 🔗 References

- [RSA Algorithm - Wikipedia](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
- [Introduction to Modern Cryptography](https://www.cs.umd.edu/~jkatz/imc.html)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 📧 Contact

For questions or suggestions, please open an issue on GitHub or contact the repository owner.

---

**Note**: This application is for educational purposes. Please use established cryptographic libraries for production applications.