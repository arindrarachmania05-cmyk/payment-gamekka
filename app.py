import random
import streamlit as st

# Konfigurasi Halaman
st.set_page_config(page_title="Payment Detective Game", layout="centered")

# Inisialisasi State Permainan
if "game_state" not in st.session_state:
  st.session_state.game_state = "START"  # START, LEVEL_1, LEVEL_2, LEVEL_3, GAME_OVER, WIN
if "current_soal_l1" not in st.session_state:
  st.session_state.current_soal_l1 = None
if "score" not in st.session_state:
  st.session_state.score = 0

# --- STOK SOAL LEVEL 1 (Pilihan Ganda / Eliminasi Awal) ---
SOAL_LEVEL_1_POOL = [
    {
        "id": 1,
        "soal": (
            "Jatuh tempo pembayaran adalah 10 November. Nasabah menerima gaji"
            " 20 November dan tidak memiliki uang yang cukup sebelum tanggal"
            " 10. Apa penyebab paling tepat?"
        ),
        "opsi": [
            "A. Lupa tanggal jatuh tempo",
            "B. Gajian setelah jatuh tempo",
            "C. Tidak ada pengingat",
            "D. Mendapat bonus setelah jatuh tempo",
        ],
        "jawaban": "B. Gajian setelah jatuh tempo",
    },
    {
        "id": 2,
        "soal": (
            "Jatuh tempo 10 Desember, tanggal gajian 5 Desember, tetapi nasabah"
            " baru membayar 15 Desember karena lupa tanggal pembayaran. Apa"
            " penyebab utamanya?"
        ),
        "opsi": [
            "A. Gajian setelah jatuh tempo",
            "B. Saldo tidak mencukupi",
            "C. Lupa tanggal jatuh tempo",
            "D. Tidak menerima gaji",
        ],
        "jawaban": "C. Lupa tanggal jatuh tempo",
    },
    {
        "id": 3,
        "soal": (
            "Jatuh tempo 20 Januari. Nasabah menerima gaji 10 Januari, tetapi"
            " tidak mengaktifkan notifikasi dan akhirnya lupa membayar sampai"
            " tanggal 25 Januari. Penyebab yang paling tepat adalah..."
        ),
        "opsi": [
            "A. Gajian terlambat",
            "B. Tidak ada pengingat",
            "C. Saldo tidak mencukupi",
            "D. Jatuh tempo terlalu cepat",
        ],
        "jawaban": "B. Tidak ada pengingat",
    },
    {
        "id": 4,
        "soal": (
            "Iuran bulanan Rp150.000. Jatuh tempo 5 Februari, sedangkan saldo"
            " nasabah pada tanggal tersebut hanya Rp100.000. Tanggal gajian"
            " adalah 10 Februari. Apa penyebab keterlambatan?"
        ),
        "opsi": [
            "A. Lupa tanggal jatuh tempo",
            "B. Tidak ada pengingat",
            "C. Saldo tidak mencukupi",
            "D. Gaji diterima sebelum jatuh tempo",
        ],
        "jawaban": "C. Saldo tidak mencukupi",
    },
]

# --- JUDUL UTAMA ---
st.title("🕵️ PAYMENT DETECTIVE - GAME SISTEM GUGUR")
st.write(
    "Aturan: Jika Anda salah menjawab atau memilih kartu BOOM, Anda akan langsung"
    " **GUGUR (Game Over)**!"
)
st.markdown("---")

# --- HALAMAN UTAMA / START ---
if st.session_state.game_state == "START":
  st.subheader("Selamat Datang di Detektif Pembayaran!")
  st.write(
      "Uji kemampuananalisis kasus keuangan Anda. Selesaikan 3 Level untuk"
      " menang."
  )
  if st.button("Mulai Game"):
    # Ambil soal acak untuk Level 1 dari stok
    st.session_state.current_soal_l1 = random.choice(SOAL_LEVEL_1_POOL)
    st.session_state.game_state = "LEVEL_1"
    st.rerun()

# --- LEVEL 1: PILIHAN GANDA (SISTEM GUGUR) ---
elif st.session_state.game_state == "LEVEL_1":
  st.header("📌 Level 1: Analisis Kasus Awal")
  soal_data = st.session_state.current_soal_l1

  st.write(f"**Soal:** {soal_data['soal']}")

  pilihan = st.radio("Pilih jawaban yang paling tepat:", soal_data["opsi"])

  if st.button("Jawab Level 1"):
    if pilihan == soal_data["jawaban"]:
      st.success("Benar! Anda Lanjut ke Level 2.")
      st.session_state.game_state = "LEVEL_2"
      st.rerun()
    else:
      st.error(
          f"❌ SALAH! Jawaban yang benar adalah: {soal_data['jawaban']}"
      )
      st.session_state.game_state = "GAME_OVER"
      st.rerun()

# --- LEVEL 2: PILIH KARTU PENYEBAB & BOOM ---
elif st.session_state.game_state == "LEVEL_2":
  st.header("🃏 Level 2: Pilih Kartu Faktor Penyebab (1 BOOM)")
  st.write(
      "Pilih **4 Faktor Penyebab yang Benar** dan hindari **1 Kartu BOOM"
      " (Jebakan)**."
  )

  # Checkbox untuk kartu-kartu
  k_a = st.checkbox(
      "Kartu A — Gajian Setelah Jatuh Tempo (Terima gaji tgl 20, jatuh tempo"
      " tgl 10)"
  )
  k_b = st.checkbox(
      "Kartu B — Saldo Tidak Mencukupi (Dana sebelum tgl 10 tidak cukup)"
  )
  k_c = st.checkbox(
      "Kartu C — Kendala Keuangan (Keterbatasan dana sebelum terima gaji)"
  )
  k_d = st.checkbox(
      "Kartu D — Lupa Tanggal Jatuh Tempo (Tidak membayar sebelum tanggal"
      " ditentukan)"
  )
  k_e = st.checkbox(
      "Kartu E — Gaji Sebelum Jatuh Tempo (Nasabah menerima gaji sebelum tgl"
      " 10)"
  )

  if st.button("Submit Pilihan Kartu"):
    # Kunci benar: A, B, C, D. BOOM: E (tidak boleh dicentang atau jika E dicentang = gugur)
    pilihan_user = {
        "A": k_a,
        "B": k_b,
        "C": k_c,
        "D": k_d,
        "E": k_e,
    }

    # Syarat menang: A, B, C, D True, E False
    if (
        pilihan_user["A"]
        and pilihan_user["B"]
        and pilihan_user["C"]
        and pilihan_user["D"]
        and not pilihan_user["E"]
    ):
      st.success("Luar Biasa! Anda berhasil melewati Level 2.")
      st.session_state.game_state = "LEVEL_3"
      st.rerun()
    else:
      st.error(
          "💥 BOOM! Pilihan kartu Anda salah atau mengenai kartu jebakan (BOOM)."
          " Anda GUGUR!"
      )
      st.session_state.game_state = "GAME_OVER"
      st.rerun()

# --- LEVEL 3: SOLUSI & TINDAKAN ---
elif st.session_state.game_state == "LEVEL_3":
  st.header("💡 Level 3: Solusi dan Tindakan Terbaik")
  st.write(
      "Pilih tindakan pencegahan/solusi yang **BENAR**. Hati-hati dengan pilihan"
      " BOOM!"
  )

  s_a = st.checkbox("A. Sisihkan dana dari pemasukan sebelumnya.")
  s_b = st.checkbox("B. Atur anggaran agar tagihan diprioritaskan.")
  s_c = st.checkbox("C. Ajukan bantuan/solusi pembayaran kepada pihak bank.")
  s_d = st.checkbox("D. Pasang pengingat beberapa hari sebelum jatuh tempo.")
  s_e = st.checkbox("E. Bayar setelah gaji masuk tanggal 20.")
  s_f = st.checkbox(
      "F. Gunakan dana yang tersedia untuk pembayaran terlebih dahulu."
  )

  if st.button("Submit Solusi"):
    # Kunci benar: A, B, C, D, F | BOOM: E
    if s_a and s_b and s_c and s_d and s_f and not s_e:
      st.balloons()
      st.success(
          "🎉 SELAMAT! Anda berhasil menyelesaikan semua level Payment"
          " Detective!"
      )
      st.session_state.game_state = "WIN"
      st.rerun()
    else:
      st.error(
          "💥 BOOM! Anda memilih solusi yang salah atau memilih opsi BOOM."
          " Anda GUGUR di ujung level!"
      )
      st.session_state.game_state = "GAME_OVER"
      st.rerun()

# --- GAME OVER (GUGUR) ---
elif st.session_state.game_state == "GAME_OVER":
  st.error("💀 GAME OVER - ANDA GUGUR!")
  st.write("Jangan menyerah, silakan coba lagi dengan soal yang diacak ulang.")
  if st.button("Main Lagi Dari Awal"):
    st.session_state.game_state = "START"
    st.rerun()

# --- MENANG (WIN) ---
elif st.session_state.game_state == "WIN":
  st.balloons()
  st.success("🏆 ANDA MENANG SEBAGAI MASTER PAYMENT DETECTIVE!")
  if st.button("Main Lagi"):
    st.session_state.game_state = "START"
    st.rerun()