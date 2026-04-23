Azmi Novi Athaya (2301020001)  
Ezzy Auriel Syach Lie (2301020011)

# Tugas Pengolahan Citra Digital - Konvolusi & Mask Processing

Repositori ini berisi serangkaian program Python yang dibuat untuk memenuhi tugas mata kuliah **Pengolahan Citra Digital**. Tujuan utama dari proyek ini adalah untuk memahami dan mengimplementasi operasi peningkatan mutu citra (Image Enhancement) menggunakan teknik **Konvolusi Spasial (Mask Processing)**.

---

##  Daftar File Program

Terdapat 3 versi program utama yang disertakan dalam repositori ini, masing-masing memiliki tujuan dan standar yang berbeda:

### 1. `konvolusi_citra.py` (Proses Matematika Konvolusi Manual)
File ini mendemonstrasikan bagaimana konvolusi bekerja secara mentah (dari *scratch*).
- **Rumus yang digunakan**: $h(x,y) = f(x,y) \otimes g(x,y)$.
- **Metrik Padding**: Menerapkan metode *Zero Padding* sehingga semua piksel pinggir tetap terkonvolusi.
- Algoritma pemrosesan menggunakan optimasi *Numpy Slicing* (alternatif efisien dari perulangan manual/Nested Loop).
- Menerapkan iterasi manual tanpa bantuan fungsi instan seperti `filter2D` untuk tujuan edukasi yang fundamental.

### 2. `konvolusi_filter2d.py` (Menggunakan Pustaka Praktis Open CV)
File ini menjawab permintaan pembuatan konvolusi yang memanfaatkan secara penuh fungsi *built-in* dari library eksternal.
- Dirancang menggunakan fungsi `cv2.filter2D()`.
- Secara default akan menerapkan dan menampilkan *Image Sharpening* (Peningkatan Kontras Tepi) serta algoritma *Edge Detection* (Deteksi Tepi Ekstrim/Laplacian).

### 3. `gui_konvolusi.py` (Aplikasi Antarmuka Pengguna Interaktif / GUI)
Program interaktif (Berbasis `Tkinter`) untuk mempermudah eksekusi dan demonstrasi algoritma di atas!
- Tema *Dark Mode* modern yang elegan.
- **Fitur Tambahan**: 
  - Memilih foto bebas langsung dari *File Explorer* pengguna.
  - Opsi *Dropdown* instan untuk menukar berbagai variasi Kernel Mask (Sharpening, Smoothing, Emboss, Sobel X & Y, Motion Blur) tanpa perlu me-restart script.
  - Tombol **Simpan Hasil** untuk mengekstrak foto yang telah di-filter!

---

## 🧮 Daftar Mask / Filter Kernel yang Digunakan

Program ini menanamkan serangkaian *Mask Array* 3x3 berikut:

1. **Sharpening (Penajaman Citra)**:  
   Meningkatkan keterangan/kontras tepian objek.  
   ```math
   [ 0,  -1,   0 ]
   [-1,   5,  -1 ]
   [ 0,  -1,   0 ]
   ```
2. **Smoothing (Box Filter)**:  
   Menghaluskan / me-ngeblur citra secara parsial (Low-pass) menggunakan perhitungan rata-rata.
3. **Edge Detection (Tepi Laplacian)**:  
   Mempertahankan area deteksi sudut dan memadamkan rentang piksel statis/solid.
   ```math
   [-1, -1, -1 ]
   [-1,  8, -1 ]
   [-1, -1, -1 ]
   ```
4. **Emboss Effect**:  
   Menghasilkan bayangan semu yang memberi efek pahatan/ukiran 3D (Timbul).
5. **Sobel X & Sobel Y**:  
   Operator edge eksklusif untuk mengekstrak hanya tekstur vertikal/horizontal dari citra.

---

## 🛠️ Prasyarat (Requirements)

Sebelum menjalankan program, pastikan Anda telah memasang dependensi (Library) Python berikut:

```bash
pip install opencv-python numpy matplotlib pillow
```

---

## 🎯 Cara Menjalankan (How to Run)

1. *Clone* repositori ini ke komputer Anda:
   ```bash
   git clone https://github.com/SyachLie/TugasPengolahanCitra.git
   ```
2. Buka folder lewat Terminal / CMD.
3. Untuk menjalankan **Versi GUI** interaktif:
   ```bash
   python gui_konvolusi.py
   ```
4. Untuk menjalankan **Versi Skrip Normal** (pastikan sudah menyiapkan folder `dataset_bunga` dan memasukkan foto di dalamnya):
   ```bash
   python konvolusi_citra.py
   # ATAU
   python konvolusi_filter2d.py
   ```
