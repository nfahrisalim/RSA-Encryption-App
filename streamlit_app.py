import streamlit as st
import math
import random
import pandas as pd
import io

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

# Generate bilangan prima acak
def generate_random_prime(min_val=10, max_val=100):
    primes = [n for n in range(min_val, max_val) if is_prime(n)]
    if primes:
        return random.choice(primes)
    return 7

# Enkripsi teks dengan support untuk semua karakter
def encrypt_text(text, e, n, support_all_chars=False):
    cipher_numbers = []
    cipher_letters = []
    encryption_data = []
    
    for ch in text:
        ascii_val = ord(ch)
        cipher_num = mod_exp(ascii_val, e, n)
        cipher_letter = angka_ke_huruf(cipher_num)
        
        encryption_data.append({
            'Karakter': ch if ch != ' ' else '␣',
            'ASCII (m)': ascii_val,
            f'm^{e} mod {n}': cipher_num,
            'Cipher Huruf': cipher_letter
        })
        
        cipher_numbers.append(cipher_num)
        cipher_letters.append(cipher_letter)
    
    return cipher_numbers, cipher_letters, encryption_data

# Dekripsi teks
def decrypt_text(cipher_numbers, d, n):
    decrypted_numbers = []
    decrypted_letters = []
    decryption_data = []
    
    for cipher_num in cipher_numbers:
        decrypted_num = mod_exp(cipher_num, d, n)
        decrypted_letter = chr(decrypted_num)
        
        decryption_data.append({
            'Cipher (c)': cipher_num,
            f'c^{d} mod {n}': decrypted_num,
            'ASCII ke Karakter': decrypted_letter if decrypted_letter != ' ' else '␣'
        })
        
        decrypted_numbers.append(decrypted_num)
        decrypted_letters.append(decrypted_letter)
    
    return decrypted_numbers, decrypted_letters, decryption_data

def main():
    st.title("RSA Encryption/Decryption Calculator")
    st.markdown("---")
    
    # RSA Parameters in main area
    st.header("RSA Parameters")
    
    # Generator bilangan prima
    st.subheader("Generator Bilangan Prima")
    if st.button("Buat angka prima acak", help="Klik untuk membuat bilangan prima p dan q secara acak"):
        st.session_state.random_p = generate_random_prime(10, 100)
        st.session_state.random_q = generate_random_prime(10, 100)
        while st.session_state.random_q == st.session_state.random_p:
            st.session_state.random_q = generate_random_prime(10, 100)
        st.success(f"✨ Generated: p={st.session_state.random_p}, q={st.session_state.random_q}")
    
    # Input untuk bilangan prima p dan q
    default_p = st.session_state.get('random_p', 7)
    default_q = st.session_state.get('random_q', 11)
    
    st.subheader("Input Bilangan Prima")
    col1, col2 = st.columns(2)
    
    with col1:
        p = st.number_input("Masukkan bilangan prima p:", min_value=2, value=default_p, step=1, 
                           help="Bilangan prima pertama untuk RSA. Contoh: 7, 11, 13, 17, 19, 23")
    with col2:
        q = st.number_input("Masukkan bilangan prima q:", min_value=2, value=default_q, step=1,
                           help="Bilangan prima kedua untuk RSA. Harus berbeda dari p")
    
    # Validasi bilangan prima
    p_is_prime = is_prime(p)
    q_is_prime = is_prime(q)
    
    col1, col2 = st.columns(2)
    with col1:
        if not p_is_prime:
            st.error(f"❌ {p} bukan bilangan prima!")
        else:
            st.success(f"✅ {p} adalah bilangan prima")
    
    with col2:
        if not q_is_prime:
            st.error(f"❌ {q} bukan bilangan prima!")
        else:
            st.success(f"✅ {q} adalah bilangan prima")
    
    # Jika p dan q valid, lanjutkan
    if p_is_prime and q_is_prime and p != q:
        n = p * q
        phi = (p - 1) * (q - 1)
        
        # Input untuk e
        st.subheader("Eksponen Publik")
        e = st.number_input(f"Masukkan nilai e (1 < e < {phi}, relatif prima dengan φ):", 
                           min_value=2, max_value=phi-1, value=min(65537, phi-1) if phi > 65537 else min(17, phi-1), step=1,
                           help="Eksponen enkripsi publik. Nilai umum: 3, 17, 257, 65537")
        
        # Validasi e
        if gcd(e, phi) == 1:
            st.success(f"✅ e = {e} relatif prima dengan φ = {phi}")
            
            # Hitung d
            try:
                d = mod_inverse(e, phi)
                
                # Tampilkan hasil kunci
                st.header("Kunci RSA yang Dihasilkan")
                
                with st.expander("Apa itu kunci RSA?", expanded=False):
                    st.write("""
                    **RSA** adalah algoritma enkripsi asimetris yang menggunakan sepasang kunci:
                    - **Kunci Publik (e, n)**: Digunakan untuk mengenkripsi pesan. Bisa dibagikan ke publik.
                    - **Kunci Privat (d, n)**: Digunakan untuk mendekripsi pesan. Harus dirahasiakan.
                    
                    **Cara Kerja:**
                    1. Pilih dua bilangan prima p dan q
                    2. Hitung n = p × q (modulus)
                    3. Hitung φ(n) = (p-1) × (q-1) (Euler's totient)
                    4. Pilih e yang relatif prima dengan φ(n)
                    5. Hitung d sebagai modular inverse dari e mod φ(n)
                    """)
                
                # Opsi pengaturan tampilan parameter
                col_settings1, col_settings2, col_settings3 = st.columns([2, 1, 1])
                with col_settings2:
                    show_calculations = st.checkbox("Tampilkan Perhitungan Detail", value=False, 
                                                   help="Tampilkan langkah-langkah perhitungan untuk setiap parameter")
                with col_settings3:
                    edit_mode = st.checkbox("Edit Parameter", value=False,
                                           help="Aktifkan untuk mengedit nilai p, q, dan e")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Parameter Dasar")
                    
                    if edit_mode:
                        # Mode edit - bisa input langsung
                        st.write("**Edit bilangan prima:**")
                        
                        # Input p
                        new_p = st.number_input("**p** (bilangan prima):", 
                                               min_value=2, value=p, step=1, 
                                               key="edit_p",
                                               help="Masukkan bilangan prima pertama")
                        if new_p != p:
                            if is_prime(new_p):
                                st.success(f"✅ {new_p} adalah bilangan prima")
                                st.session_state.random_p = new_p
                                st.rerun()
                            else:
                                st.error(f"❌ {new_p} bukan bilangan prima!")
                        
                        # Input q
                        new_q = st.number_input("**q** (bilangan prima):", 
                                               min_value=2, value=q, step=1,
                                               key="edit_q",
                                               help="Masukkan bilangan prima kedua (harus berbeda dari p)")
                        if new_q != q:
                            if is_prime(new_q):
                                if new_q != new_p:
                                    st.success(f"✅ {new_q} adalah bilangan prima")
                                    st.session_state.random_q = new_q
                                    st.rerun()
                                else:
                                    st.error(f"❌ q tidak boleh sama dengan p!")
                            else:
                                st.error(f"❌ {new_q} bukan bilangan prima!")
                        
                        st.info("Gunakan sidebar atau klik 'Generate Random Primes' untuk nilai acak")
                    else:
                        # Mode view - hanya tampilan
                        # p dengan tooltip
                        st.write(f"**p =** {p}")
                        if show_calculations:
                            st.caption(f"Bilangan prima pertama yang dipilih")
                        
                        # q dengan tooltip
                        st.write(f"**q =** {q}")
                        if show_calculations:
                            st.caption(f"Bilangan prima kedua yang dipilih")
                    
                    # n dengan perhitungan (selalu tampil)
                    st.write(f"**n = p × q =** {n}")
                    if show_calculations:
                        st.caption(f"Perhitungan: {p} × {q} = {n}")
                        st.caption(f"n adalah modulus untuk enkripsi dan dekripsi")
                    
                    # phi dengan perhitungan (selalu tampil)
                    st.write(f"**φ(n) = (p-1) × (q-1) =** {phi}")
                    if show_calculations:
                        st.caption(f"Perhitungan: ({p}-1) × ({q}-1) = {p-1} × {q-1} = {phi}")
                        st.caption(f"φ(n) adalah Euler's totient function")
                    
                    # Tambahan detail parameter dasar
                    if show_calculations:
                        with st.expander("➕ Informasi Tambahan Parameter"):
                            st.write(f"**Faktorisasi n:** {p} × {q} = {n}")
                            st.write(f"**p - 1 =** {p-1}")
                            st.write(f"**q - 1 =** {q-1}")
                            st.write(f"**φ(n) =** {phi}")
                            st.write(f"**GCD(e, φ) =** {gcd(e, phi)}")
                
                with col2:
                    st.subheader("Kunci")
                    
                    if edit_mode:
                        # Mode edit - bisa input e langsung
                        st.write("**Edit eksponen publik e:**")
                        
                        new_e = st.number_input(f"**e** (relatif prima dengan φ={phi}):", 
                                               min_value=2, max_value=phi-1, value=e, step=1,
                                               key="edit_e",
                                               help="Eksponen enkripsi publik. Nilai umum: 3, 17, 257, 65537")
                        
                        if new_e != e:
                            if gcd(new_e, phi) == 1:
                                st.success(f"✅ e = {new_e} relatif prima dengan φ = {phi}")
                                st.info("⚠️ Silakan ubah nilai e di sidebar untuk menerapkan perubahan")
                            else:
                                st.error(f"❌ e = {new_e} tidak relatif prima dengan φ = {phi} (GCD = {gcd(new_e, phi)})")
                        
                        st.info("Ubah nilai e di sidebar untuk menerapkan perubahan")
                    
                    # Kunci Publik (selalu tampil)
                    st.write(f"**Kunci Publik (e, n) =** ({e}, {n})")
                    if show_calculations:
                        st.caption(f"e = {e} (eksponen enkripsi)")
                        st.caption(f"n = {n} (modulus)")
                    
                    # Kunci Privat
                    st.write(f"**Kunci Privat (d, n) =** ({d}, {n})")
                    if show_calculations:
                        st.caption(f"d = {d} (eksponen dekripsi)")
                        st.caption(f"d adalah modular inverse dari e mod φ(n)")
                    
                    # Verifikasi
                    verification = (e * d) % phi
                    st.write(f"**Verifikasi: e × d mod φ =** {verification}")
                    if show_calculations:
                        st.caption(f"Perhitungan: ({e} × {d}) mod {phi}")
                        st.caption(f"= {e * d} mod {phi} = {verification}")
                        if verification == 1:
                            st.caption("✅ Kunci valid (hasil = 1)")
                        else:
                            st.caption("❌ Error: hasil harus = 1")
                    
                    # Tambahan detail kunci
                    if show_calculations:
                        with st.expander("➕ Informasi Tambahan Kunci"):
                            st.write("**Properti Kunci:**")
                            st.write(f"- e × d ≡ 1 (mod φ(n))")
                            st.write(f"- {e} × {d} ≡ 1 (mod {phi})")
                            st.write(f"- {e} × {d} = {e*d}")
                            st.write(f"- Dapat dibagikan: Public Key (e, n)")
                            st.write(f"- Harus dirahasiakan: Private Key (d, n)")
                
                st.markdown("---")
                
                # Input pesan dengan opsi mode
                st.header("Enkripsi dan Dekripsi Pesan")
                
                # Mode input
                input_mode = st.radio("Mode Input:", ["Text Input", "File Upload"], horizontal=True,
                                     help="Pilih apakah ingin mengetik teks langsung atau upload file")
                
                pesan = ""
                
                if input_mode == "Text Input":
                    # Opsi untuk support semua karakter
                    support_all_chars = st.checkbox("Support lowercase & karakter spesial", value=False,
                                                   help="Centang untuk mendukung huruf kecil, spasi, dan karakter khusus")
                    
                    if support_all_chars:
                        pesan = st.text_area("Masukkan pesan (semua karakter):", value="Hello World!", height=100)
                    else:
                        pesan_input = st.text_input("Masukkan pesan (huruf kapital A-Z):", value="HELLO")
                        pesan = pesan_input.upper()
                        # Filter hanya huruf A-Z
                        pesan_filtered = ''.join([ch for ch in pesan if ch.isalpha() and ch.isupper()])
                        if pesan_filtered != pesan and pesan:
                            st.warning(f"Pesan difilter menjadi: {pesan_filtered}")
                            pesan = pesan_filtered
                else:
                    # File upload
                    uploaded_file = st.file_uploader("Upload file teks:", type=['txt'], 
                                                     help="Upload file .txt untuk dienkripsi")
                    if uploaded_file is not None:
                        pesan = uploaded_file.read().decode('utf-8')
                        st.info(f"File loaded: {len(pesan)} karakter")
                        with st.expander("Preview pesan dari file"):
                            st.text(pesan[:500] + ('...' if len(pesan) > 500 else ''))
                    support_all_chars = True
                
                if pesan:
                    # Enkripsi
                    st.subheader("Proses Enkripsi")
                    
                    with st.expander("Bagaimana enkripsi bekerja?", expanded=False):
                        st.write("""
                        **Proses Enkripsi:**
                        1. Setiap karakter dikonversi ke nilai ASCII
                        2. Nilai ASCII dipangkatkan dengan eksponen e
                        3. Hasil dipangkatan di-mod dengan n untuk mendapat ciphertext
                        4. Formula: **c ≡ m^e (mod n)**
                        
                        Ciphertext yang dihasilkan aman karena sangat sulit menghitung akar pangkat e mod n tanpa mengetahui kunci privat d.
                        """)
                    
                    cipher_numbers, cipher_letters, encryption_data = encrypt_text(pesan, e, n, support_all_chars)
                    
                    # Tampilkan tabel enkripsi
                    if len(pesan) <= 50:
                        st.write("**Langkah per Karakter:**")
                        df_encryption = pd.DataFrame(encryption_data)
                        st.dataframe(df_encryption, width=800)
                    else:
                        st.info(f"Pesan terlalu panjang ({len(pesan)} karakter) untuk ditampilkan dalam tabel detail.")
                        with st.expander("Lihat detail enkripsi"):
                            df_encryption = pd.DataFrame(encryption_data)
                            st.dataframe(df_encryption, width=800)
                    
                    st.write("**Hasil Enkripsi:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Ciphertext (angka):**")
                        st.code(str(cipher_numbers), language=None)
                    with col2:
                        st.write(f"**Ciphertext (huruf):**")
                        cipher_text = ''.join(cipher_letters)
                        st.code(cipher_text, language=None)
                    
                    # Download hasil enkripsi
                    col1, col2 = st.columns(2)
                    with col1:
                        cipher_text_file = '\n'.join([
                            "=== RSA Encrypted Message ===",
                            f"Ciphertext (numbers): {cipher_numbers}",
                            f"Ciphertext (letters): {cipher_text}",
                            f"Public Key (e, n): ({e}, {n})",
                            ""
                        ])
                        st.download_button(
                            label="📥 Download Ciphertext",
                            data=cipher_text_file,
                            file_name="encrypted.txt",
                            mime="text/plain"
                        )
                    
                    # Proses Dekripsi
                    st.subheader("Proses Dekripsi")
                    
                    with st.expander("Bagaimana dekripsi bekerja?", expanded=False):
                        st.write("""
                        **Proses Dekripsi:**
                        1. Ciphertext dipangkatkan dengan eksponen privat d
                        2. Hasil dipangkatan di-mod dengan n
                        3. Nilai yang didapat adalah nilai ASCII asli
                        4. Nilai ASCII dikonversi kembali ke karakter
                        5. Formula: **m ≡ c^d (mod n)**
                        
                        Hanya pemilik kunci privat d yang dapat mendekripsi pesan dengan benar.
                        """)
                    
                    decrypted_numbers, decrypted_letters, decryption_data = decrypt_text(cipher_numbers, d, n)
                    
                    if len(pesan) <= 50:
                        st.write("**Langkah per Karakter:**")
                        df_decryption = pd.DataFrame(decryption_data)
                        st.dataframe(df_decryption, width=800)
                    else:
                        st.info(f"Pesan terlalu panjang ({len(pesan)} karakter) untuk ditampilkan dalam tabel detail.")
                        with st.expander("Lihat detail dekripsi"):
                            df_decryption = pd.DataFrame(decryption_data)
                            st.dataframe(df_decryption, width=800)
                    
                    st.write("**Hasil Dekripsi:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Plaintext (ASCII):**")
                        st.code(str(decrypted_numbers), language=None)
                    with col2:
                        st.write(f"**Plaintext (teks):**")
                        decrypted_text = ''.join(decrypted_letters)
                        st.code(decrypted_text, language=None)
                    
                    # Download hasil dekripsi
                    with col2:
                        st.download_button(
                            label="📥 Download Plaintext",
                            data=decrypted_text,
                            file_name="decrypted.txt",
                            mime="text/plain"
                        )
                    
                    # Verifikasi
                    if pesan == decrypted_text:
                        st.success("✅ Dekripsi berhasil! Pesan asli berhasil dipulihkan.")
                    else:
                        st.error("❌ Terjadi kesalahan dalam proses enkripsi/dekripsi.")
                    
                    # Penjelasan matematis
                    st.markdown("---")
                    st.subheader("Penjelasan Matematis")
                    
                    with st.expander("Lihat Detail Formula", expanded=False):
                        st.latex(r"c \equiv m^e \pmod{n}")
                        st.write(f"**Enkripsi:** c ≡ m^{e} (mod {n})")
                        st.write("")
                        
                        st.latex(r"m \equiv c^d \pmod{n}")
                        st.write(f"**Dekripsi:** m ≡ c^{d} (mod {n})")
                        st.write("")
                        
                        st.write("**Kunci:**")
                        st.write(f"- Public Key: (e={e}, n={n})")
                        st.write(f"- Private Key: (d={d}, n={n})")
                        
                        st.latex(r"e \times d \equiv 1 \pmod{\phi(n)}")
                        st.write(f"- Verifikasi: {e} × {d} ≡ 1 (mod {phi})")
                        st.write(f"- Hasil: {e} × {d} = {e*d}, {e*d} mod {phi} = {(e*d) % phi}")
                    
            except Exception as ex:
                st.error(f"Error menghitung private key: {str(ex)}")
                
        else:
            st.error(f"❌ e = {e} tidak relatif prima dengan φ = {phi} (GCD = {gcd(e, phi)})")
    
    elif p == q:
        st.error("❌ p dan q tidak boleh sama!")
    
    # Informasi tambahan
    st.markdown("---")
    st.info("""
    **💡 Tips:**
    - Pilih bilangan prima p dan q yang berbeda
    - e harus relatif prima dengan φ(n)
    - Nilai e yang umum: 3, 17, 257, 65537
    - Untuk keamanan nyata, gunakan bilangan prima yang lebih besar
    - Gunakan generator untuk coba berbagai kombinasi
    """)

if __name__ == "__main__":
    main()
