# 🔨 Chatbot Persona — "Mandor Mimpi"

**Tempatnya ditegur, bukan dipuk-puk.**

Kerangka chatbot Streamlit + Gemini yang **karakternya bisa diganti lewat satu file**. Persona bawaannya: *Mandor Mimpi* — pelatih disiplin bergaya *tough love* untuk orang yang hobi menunda-nunda. Bukan bot yang membelai, tapi bot yang membongkar alasanmu lalu memberi satu langkah konkret untuk 15 menit ke depan.

> **Kamu:** "Belum sempat ngerjain, sibuk banget."
>
> **Mandor:** "Sibuk apa? Tadi malam berapa jam kamu scroll? Buka laptop sekarang, tulis satu paragraf pembuka. Cuma satu. Lapor lagi 15 menit."

---

## 🎭 Kenapa "Mandor"?

Sudah banyak bot yang menenangkan. Yang jarang: bot yang berani menegur. Personanya seperti mandor proyek — galak, blak-blakan, tapi tujuannya supaya kamu benar-benar jalan.

**Tapi ada rem pengamannya:** kalau kamu menunjukkan tanda depresi, burnout parah, atau sedang berduka, bot ini otomatis melepas gaya galaknya, berubah jadi hangat, dan menyarankan bicara dengan orang terdekat atau tenaga profesional. Tough love hanya untuk orang yang sedang malas — bukan untuk orang yang sedang terluka.

---

## 🛠️ Teknologi

| Bagian | Pilihan | Alasan |
|---|---|---|
| Model AI | Google Gemini (`gemini-3.5-flash-lite`) | Cepat, kuota gratis besar |
| SDK | `google-genai` (Interactions API) | Riwayat chat diurus server, tanpa framework tambahan |
| UI | Streamlit | Cepat dibangun, gratis di-deploy |

Total cuma **2 dependency**. Tanpa LangChain, tanpa vector DB, tanpa lapisan abstraksi berlebih.

---

## 📁 Struktur file

```
app.py                 → seluruh logika aplikasi (± 100 baris)
persona.py             → karakter bot & semua teks UI  ← edit di sini
requirements.txt
runtime.txt            → kunci Python 3.11
.streamlit/config.toml → tema warna
```

### Mengganti persona

Mau ubah bot ini jadi konsep lain — pelatih olahraga, teman belajar, tutor bahasa? **Cukup edit `persona.py`:**

| Yang diubah | Isinya |
|---|---|
| `SYSTEM_INSTRUCTION` | Karakter & aturan main bot |
| `JUDUL`, `SUBJUDUL`, `SAPAAN_AWAL` | Teks yang dilihat pengguna |
| `AVATAR_BOT`, `AVATAR_USER` | Emoji avatar |
| `TEKS_LOADING`, `PLACEHOLDER_INPUT` | Teks kecil di UI |
| `MODEL` | Model Gemini yang dipakai |

`app.py` tidak perlu disentuh sama sekali. Warna tema diatur terpisah di `.streamlit/config.toml`.

---

## 🚀 Menjalankan di komputer sendiri

1. **Ambil API key gratis** di [aistudio.google.com/apikey](https://aistudio.google.com/apikey) (tanpa kartu kredit).

2. **Simpan API key.** Salin `.streamlit/secrets.toml.example` menjadi `.streamlit/secrets.toml`, lalu isi:
   ```toml
   GEMINI_API_KEY = "isi_api_key_kamu"
   ```

3. **Install & jalankan:**
   ```bash
   pip install -r requirements.txt
   streamlit run app.py
   ```

---

## ☁️ Deploy ke Streamlit Community Cloud

1. Push repo ini ke GitHub.
2. Buka [share.streamlit.io](https://share.streamlit.io) → hubungkan repo → pilih `app.py`.
3. Di **Settings → Secrets**, isi:
   ```toml
   GEMINI_API_KEY = "isi_api_key_kamu"
   ```
4. Pastikan **Settings → Python version** = **3.11** (SDK `google-genai` butuh minimal Python 3.10).

---

## ⚠️ Catatan

Bot ini bukan terapis dan tidak memberi nasihat medis. Kalau kamu sedang tidak baik-baik saja, bicaralah dengan orang yang kamu percaya atau tenaga profesional.
