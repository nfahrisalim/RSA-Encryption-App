# Fungsi cari gcd
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Extended Euclidean Algorithm untuk cari invers modulo
def mod_inverse(e, phi):
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
    g, x, y = egcd(e, phi)
    if g != 1:
        raise Exception('Tidak ada invers modular')
    else:
        return x % phi

# Fast modular exponentiation
def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp //= 2
        base = (base * base) % mod
    return result

# Konversi angka ke huruf A-Z (mod 26)
def angka_ke_huruf(num):
    return chr((num % 26) + 65)

# Main RSA
if __name__ == "__main__":
    print("=== Penggunaan RSA Dalam pyhon ===")
    
    # Input kunci dari user
    p = int(input("Masukkan bilangan prima p: "))
    q = int(input("Masukkan bilangan prima q: "))
    e = int(input("Masukkan nilai e (relatif prima dengan phi): "))

    n = p * q
    phi = (p - 1) * (q - 1)

    # Validasi gcd
    if gcd(e, phi) != 1:
        raise Exception("e tidak relatif prima dengan phi")

    # Cari d
    d = mod_inverse(e, phi)

    print(f"\n=== Kunci yang dihasilkan ===")
    print(f"p = {p}, q = {q}")
    print(f"n (modulus) = {n}")
    print(f"phi(n) = {phi}")
    print("Kunci Publik  (e, n) =", (e, n))
    print("Kunci Privat (d, n) =", (d, n))
    print()

    # Input pesan
    pesan = input("Masukkan pesan (huruf kapital A-Z): ")

    # Enkripsi: pakai kunci publik (e, n)
    cipher = [mod_exp(ord(ch), e, n) for ch in pesan]
    cipher_huruf = ''.join([angka_ke_huruf(c) for c in cipher])

    print("\n=== Enkripsi ===")
    print("Plaintext ASCII:", [ord(ch) for ch in pesan])
    print("Ciphertext (angka):", cipher)
    print("Ciphertext (huruf A-Z):", cipher_huruf)

    # Dekripsi: pakai kunci privat (d, n)
    decrypted_num = [mod_exp(c, d, n) for c in cipher]
    plain = ''.join([chr(num) for num in decrypted_num])

    print("\n=== Dekripsi ===")
    print("Hasil ASCII:", decrypted_num)
    print("Pesan setelah dekripsi:", plain)
