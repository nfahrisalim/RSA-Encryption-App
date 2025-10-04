import streamlit as st
import math

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

# Fungsi untuk mengecek bilangan prima
def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    st.title("🔐 RSA Encryption/Decryption Calculator")
    st.markdown("---")
    
    # Sidebar untuk parameter RSA
    st.sidebar.header("RSA Parameters")
    
    # Input untuk bilangan prima p dan q
    p = st.sidebar.number_input("Masukkan bilangan prima p:", min_value=2, value=7, step=1)
    q = st.sidebar.number_input("Masukkan bilangan prima q:", min_value=2, value=11, step=1)
    
    # Validasi bilangan prima
    p_is_prime = is_prime(p)
    q_is_prime = is_prime(q)
    
    if not p_is_prime:
        st.sidebar.error(f"❌ {p} bukan bilangan prima!")
    else:
        st.sidebar.success(f"✅ {p} adalah bilangan prima")
    
    if not q_is_prime:
        st.sidebar.error(f"❌ {q} bukan bilangan prima!")
    else:
        st.sidebar.success(f"✅ {q} adalah bilangan prima")
    
    # Jika p dan q valid, lanjutkan
    if p_is_prime and q_is_prime and p != q:
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # Input untuk e
        e = st.sidebar.number_input(f"Masukkan nilai e (1 < e < {phi}, relatif prima dengan φ):", 
                                   min_value=2, max_value=phi-1, value=min(65537, phi-1), step=1)
        
        # Validasi e
        if gcd(e, phi) == 1:
            st.sidebar.success(f"✅ e = {e} relatif prima dengan φ = {phi}")
            
            # Hitung d
            try:
                d = mod_inverse(e, phi)
                
                # Tampilkan hasil kunci
                st.header("🔑 Kunci RSA yang Dihasilkan")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Parameter Dasar")
                    st.write(f"**p =** {p}")
                    st.write(f"**q =** {q}")
                    st.write(f"**n = p × q =** {n}")
                    st.write(f"**φ(n) = (p-1) × (q-1) =** {phi}")
                
                with col2:
                    st.subheader("Kunci")
                    st.write(f"**Kunci Publik (e, n) =** ({e}, {n})")
                    st.write(f"**Kunci Privat (d, n) =** ({d}, {n})")
                    st.write(f"**Verifikasi: e × d mod φ =** {(e * d) % phi}")
                
                st.markdown("---")
                
                # Input pesan
                st.header("💬 Enkripsi dan Dekripsi Pesan")
                pesan = st.text_input("Masukkan pesan (huruf kapital A-Z):", value="HELLO").upper()
                
                # Filter hanya huruf A-Z
                pesan_filtered = ''.join([ch for ch in pesan if ch.isalpha() and ch.isupper()])
                
                if pesan_filtered != pesan and pesan:
                    st.warning(f"Pesan difilter menjadi: {pesan_filtered}")
                    pesan = pesan_filtered
                
                if pesan:
                    st.subheader("🔒 Proses Enkripsi")
                    
                    # Tampilkan tabel enkripsi
                    st.write("**Langkah 1: Konversi huruf ke ASCII**")
                    ascii_values = [ord(ch) for ch in pesan]
                    
                    # Buat DataFrame untuk menampilkan proses
                    import pandas as pd
                    
                    encryption_data = []
                    cipher_numbers = []
                    cipher_letters = []
                    
                    for i, ch in enumerate(pesan):
                        ascii_val = ord(ch)
                        # Enkripsi: c = m^e mod n
                        cipher_num = mod_exp(ascii_val, e, n)
                        cipher_letter = angka_ke_huruf(cipher_num)
                        
                        encryption_data.append({
                            'Huruf': ch,
                            'ASCII (m)': ascii_val,
                            f'm^{e} mod {n}': cipher_num,
                            'Cipher Huruf': cipher_letter
                        })
                        
                        cipher_numbers.append(cipher_num)
                        cipher_letters.append(cipher_letter)
                    
                    df_encryption = pd.DataFrame(encryption_data)
                    st.dataframe(df_encryption, use_container_width=True)
                    
                    st.write("**Hasil Enkripsi:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Ciphertext (angka):** {cipher_numbers}")
                    with col2:
                        st.write(f"**Ciphertext (huruf):** {''.join(cipher_letters)}")
                    
                    st.markdown("---")
                    
                    # Proses Dekripsi
                    st.subheader("🔓 Proses Dekripsi")
                    
                    decryption_data = []
                    decrypted_numbers = []
                    decrypted_letters = []
                    
                    for i, cipher_num in enumerate(cipher_numbers):
                        # Dekripsi: m = c^d mod n
                        decrypted_num = mod_exp(cipher_num, d, n)
                        decrypted_letter = chr(decrypted_num)
                        
                        decryption_data.append({
                            'Cipher (c)': cipher_num,
                            f'c^{d} mod {n}': decrypted_num,
                            'ASCII ke Huruf': decrypted_letter
                        })
                        
                        decrypted_numbers.append(decrypted_num)
                        decrypted_letters.append(decrypted_letter)
                    
                    df_decryption = pd.DataFrame(decryption_data)
                    st.dataframe(df_decryption, use_container_width=True)
                    
                    st.write("**Hasil Dekripsi:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Plaintext (ASCII):** {decrypted_numbers}")
                    with col2:
                        st.write(f"**Plaintext (huruf):** {''.join(decrypted_letters)}")
                    
                    # Verifikasi
                    if pesan == ''.join(decrypted_letters):
                        st.success("✅ Dekripsi berhasil! Pesan asli berhasil dipulihkan.")
                    else:
                        st.error("❌ Terjadi kesalahan dalam proses enkripsi/dekripsi.")
                    
                    # Penjelasan matematis
                    st.markdown("---")
                    st.subheader("📚 Penjelasan Matematis")
                    st.write(f"""
                    **Enkripsi:** c ≡ m^e (mod n) = m^{e} (mod {n})
                    
                    **Dekripsi:** m ≡ c^d (mod n) = c^{d} (mod {n})
                    
                    **Kunci:** 
                    - Public Key: (e={e}, n={n})
                    - Private Key: (d={d}, n={n})
                    - e × d ≡ 1 (mod φ(n)) → {e} × {d} ≡ 1 (mod {phi})
                    """)
                    
            except Exception as ex:
                st.sidebar.error(f"Error menghitung private key: {str(ex)}")
                
        else:
            st.sidebar.error(f"❌ e = {e} tidak relatif prima dengan φ = {phi} (GCD = {gcd(e, phi)})")
    
    elif p == q:
        st.sidebar.error("❌ p dan q tidak boleh sama!")
    
    # Informasi tambahan
    st.sidebar.markdown("---")
    st.sidebar.info("""
    **Tips:**
    - Pilih bilangan prima p dan q yang berbeda
    - e harus relatif prima dengan φ(n)
    - Nilai e yang umum: 3, 17, 257, 65537
    - Untuk keamanan nyata, gunakan bilangan prima yang lebih besar
    """)

if __name__ == "__main__":
    main()
