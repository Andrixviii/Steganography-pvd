# Steganography-pvd

[![Live Demo](https://img.shields.io/badge/Live-Demo-green)](https://steganography-pvd.vercel.app)

Aplikasi web interaktif untuk menyisipkan (embed) dan mengekstrak (extract) pesan rahasia ke dalam citra digital menggunakan metode **Pixel Value Differencing (PVD) Steganography**.

## 📌 Teknologi & Algoritma

<<<<<<< HEAD
- **Backend:** Python, Flask, Pillow (PIL).
- **Frontend:** HTML/CSS/JS, Lucide Icons.
- **Algoritma:** [Pixel Value Differencing (PVD)](https://en.wikipedia.org/wiki/Steganography#Pixel_value_differencing).
=======
- **Backend:** Python, Flask, Pillow (PIL)
- **Frontend:** HTML/CSS/JS, Lucide Icons
- **Algoritma:** [Pixel Value Differencing (PVD)](https://en.wikipedia.org/wiki/Steganography#Pixel_value_differencing)
>>>>>>> 9a4bc9dbae40bdead124877f06490c094d97658e

### 📖 Penjelasan Singkat PVD
PVD membagi gambar menjadi pasangan piksel. Perbedaan nilai antara setiap pasangan digunakan untuk menyisipkan sejumlah bit pesan, tergantung rentang perbedaan tersebut. Semakin besar perbedaan, semakin banyak bit yang bisa disisipkan tanpa membuat perubahan visual yang mencolok.

## 🎯 Fitur Utama

- **Sisipkan Pesan Rahasia ke Gambar**  
  Membunyikan pesan teks ke dalam gambar (PNG, JPG, JPEG, BMP) dengan teknologi PVD yang menjaga kualitas visual gambar.
- **Ekstraksi Pesan dari Gambar Stego**  
  Mengambil kembali pesan rahasia yang telah disisipkan dari gambar steganografi.
- **Antarmuka Modern & Interaktif**  
  UI responsif, mudah digunakan, dengan fitur preview hasil penyisipan maupun ekstraksi.
- **Tanpa Penyimpanan File di Server**  
  Semua proses embedding dan ekstraksi berjalan langsung di server tanpa menyimpan file pengguna secara permanen.

## 🚀 Demo

Coba langsung aplikasi ini di:  
👉 https://steganography-pvd.vercel.app

## 🛠️ Cara Instalasi Lokal

1. **Clone repository ini**
    ```bash
    git clone https://github.com/Andrixviii/Steganography-pvd.git
    cd Steganography-pvd
    ```

2. **Buat virtual environment & install dependencies**
    ```bash
    python -m venv venv
    source venv/bin/activate  # atau venv\Scripts\activate di Windows
    pip install -r requirements.txt
    ```

3. **Jalankan aplikasi**
    ```bash
    python app.py
    ```
    Akses aplikasi di `http://localhost:5000`.

## 📌 Panduan Penggunaan

### 1. 🔒 Embed (Sisipkan) Pesan
- Pilih gambar (PNG/JPG/JPEG/BMP).
- Masukkan pesan rahasia.
- Klik **Embed Message**.
- Unduh gambar hasil stego.

### 2. 🔍 Extract (Ekstrak) Pesan
- Pilih gambar stego (yang sudah berisi pesan).
- Klik **Extract Message**.
- Pesan rahasia akan ditampilkan jika ditemukan.

## 📂 Struktur Direktori

```
.
├── app.py                # Aplikasi Flask utama
├── pvd_core.py           # Implementasi algoritma PVD
├── templates/
│   └── index.html        # Template halaman web
├── static/
│   └── css/
│       └── style.css     # Style untuk antarmuka
├── requirements.txt      # Daftar dependensi Python
```

