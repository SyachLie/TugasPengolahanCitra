import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def konvolusi_2d(image, kernel):
    """
    Fungsi untuk melakukan operasi konvolusi spasial 2D (grayscale).
    Menerapkan rumus: h(x,y) = f(x,y) ⊗ g(x,y)
    
    Argumen:
    - image: Masukan citra 2D (array matriks pixel)
    - kernel: Matrix mask/filter 
    """
    # Menentukan rentang/lebar padding berdasarkan dimensi kernel (biasanya ukuran ganjil spt 3x3)
    pad_h = kernel.shape[0] // 2
    pad_w = kernel.shape[1] // 2
    
    # 1. PENANGANAN PIKSEL PINGGIR
    # Solusi: Menggunakan teknik PADDING dengan menambahkan nilai 0 (Zero Padding) 
    # di sekeliling gambar batas, sehingga semua pixel akan ikut terkonvolusi dengan dimensi hasil yang sama.
    padded_img = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    
    h, w = image.shape
    hasil = np.zeros((h, w), dtype=np.float32)
    
    # 2. OPERASI KONVOLUSI
    # Algoritma iterasi disederhanakan dengan Numpy Slicing untuk komputasi cepat.
    # Secara logika ekuivalen dengan rumus per piksel: 
    # untuk setiap pixel image (x, y), kalikan region sekitarnya dengan matrik kernel.
    # 
    # Bentuk asli / konvensional (Nested-Loop):
    # for y in range(h):
    #     for x in range(w):
    #         for ky in range(kernel.shape[0]):
    #             for kx in range(kernel.shape[1]):
    #                 hasil[y, x] += padded_img[y+ky, x+kx] * kernel[ky, kx]
    
    for i in range(kernel.shape[0]):
        for j in range(kernel.shape[1]):
            # Menjumlahkan dan mengalikan mask dengan area matriks ketetanggaan pixel
            hasil += padded_img[i:i+h, j:j+w] * kernel[i, j]
            
    return hasil

def proses_konvolusi_warna(image, kernel):
    """
    Fungsi bantu untuk menangani konvolusi pada citra berwarna (3 channel: R, G, B).
    """
    # Pisahkan warna menjadi channel tunggal terlebih dahulu
    if len(image.shape) == 3:
        kanal = cv2.split(image)
        hasil_kanal = []
        for ch in kanal:
            # Konvolusi untuk tiap rentang warna
            res = konvolusi_2d(ch, kernel)
            hasil_kanal.append(res)
            
        # Gabungkan kembali 3 channel yang sudah dikonvolusi
        hasil_akhir = cv2.merge(hasil_kanal)
        # Pastikan format nilai pixel berada pada batas 0 - 255 (format standar uint8)
        return np.clip(hasil_akhir, 0, 255).astype(np.uint8)
    else:
        # Pengecekan aman jika gambar aslinya sudah grayscale
        hasil_akhir = konvolusi_2d(image, kernel)
        return np.clip(hasil_akhir, 0, 255).astype(np.uint8)

def proses_sharpening(image, kernel_laplacian):
    """
    Proses Sharpening dengan Filter Tinggi (High-pass).
    Berdasarkan teori, kernel Laplacian menghasilkan Citra Tepi (Edges).
    Untuk "menajamkan" citra, Citra Asli dikurangi (-) Gambar Tepi jika nilai tengah kernel negatif.
    """
    if len(image.shape) == 3:
        kanal = cv2.split(image)
        hasil_kanal = []
        for ch in kanal:
            # Cari tepinya menggunakan fungsi konvolusi tadi dengan laplacian mask
            laplacian = konvolusi_2d(ch, kernel_laplacian)
            # Hasil Tajam = Asli - (Laplacian dikalikan faktor)
            # Kita bisa mengalikan hasil laplacian (misal x 1.5) untuk membuat efek penajam lebih ekstrim
            faktor_intensitas = 1.5
            sharpened = ch.astype(np.float32) - (laplacian * faktor_intensitas)
            hasil_kanal.append(sharpened)
            
        hasil_akhir = cv2.merge(hasil_kanal)
        return np.clip(hasil_akhir, 0, 255).astype(np.uint8)
    else:
        laplacian = konvolusi_2d(image, kernel_laplacian)
        faktor_intensitas = 1.5
        sharpened = image.astype(np.float32) - (laplacian * faktor_intensitas)
        return np.clip(sharpened, 0, 255).astype(np.uint8)

def main():
    # Folder tempat meletakkan file gambar input .jpg / .png
    folder_dataset = 'dataset_bunga'
    
    # Otomatis membuat folder jika user belum membuatnya
    if not os.path.exists(folder_dataset):
        os.makedirs(folder_dataset)
        print(f"Folder '{folder_dataset}' telah dibuat, tetapi masih kosong.")
        print("Silakan masukkan file gambar dataset Anda (format .jpg / .png) ke dalamnya dan jalankan ulang script.")
        return

    # Tarik semua daftar file gambar pada folder tersebut
    list_file = [f for f in os.listdir(folder_dataset) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not list_file:
        print(f"Peringatan: Belum ada file kembalian gambar ditemukan pada folder '{folder_dataset}'.")
        print("Tambahkan gambar terlebih dahulu untuk dapat melanjutkan.")
        return

    # ===== DEFINISI KERNEL/MASK =====
    
    # 1. Mask Smoothing (Filter Average/Box Filter 3x3)
    # Piksel baru hasil rata-rata ketetangganya. (Filter Low-pass)
    kernel_smoothing = np.ones((3, 3), dtype=np.float32) * (1.0 / 9.0)
    
    # 2. Mask Penajam / Sharpening (Laplacian Filter 3x3)
    # Mask menemukan sisi tepian dalam gambar menggunakan turunan kedua (Filter High-pass).
    kernel_laplacian = np.array([
        [0,  1,  0],
        [1, -4,  1],
        [0,  1,  0]
    ], dtype=np.float32)

    # ===== LOOP KE SELURUH FILE DATASET GAMBAR =====
    for nama_file in list_file:
        path_file = os.path.join(folder_dataset, nama_file)
        
        # Baca file dengan format BGR Open CV
        img_bgr = cv2.imread(path_file)
        if img_bgr is None:
            print(f"Gagal memuat gambar: {nama_file}")
            continue
            
        # Konversikan ke RGB murni agar palet warna tampil sesuai di library Matplotlib (Red-Green-Blue)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        
        # [TAMBAHAN PERBAIKAN]: Perkecil ukuran (resize) jika gambar terlalu besar (HD).
        # Karena kita hanya menggunakan kernel kecil berukuran 3x3. Jika gambar asli beresolusi 2000px, 
        # efek blur/tajam 3 pixel tidak akan tertangkap/terlihat oleh mata manusia saat di-zoom out.
        maks_dimensi = 500
        h_img, w_img = img_rgb.shape[:2]
        if max(h_img, w_img) > maks_dimensi:
            skala = maks_dimensi / float(max(h_img, w_img))
            img_rgb = cv2.resize(img_rgb, (int(w_img * skala), int(h_img * skala)), interpolation=cv2.INTER_AREA)
        
        print(f"Memproses gambar: {nama_file} (diubah ukurannya ke {img_rgb.shape[1]}x{img_rgb.shape[0]} agar efek terlihat)...")
        
        # Eksekusi Pemanggilan Proses Konvolusi
        img_smooth = proses_konvolusi_warna(img_rgb, kernel_smoothing)
        img_sharpened = proses_sharpening(img_rgb, kernel_laplacian)
        
        # ===== VISUALISASIKAN GAMBAR BERDAMPINGAN DENGAN MATPLOTLIB =====
        # Atur ukuran kanvas window layout plot
        plt.figure(figsize=(15, 6))
        plt.suptitle(f"Hasil Konvolusi Mask Processing - '{nama_file}'", fontsize=16, fontweight='bold')
        
        # Kolom 1 (Kiri): Citra Asli
        plt.subplot(1, 3, 1)
        plt.imshow(img_rgb)
        plt.title("1. Citra Gambar Asli")
        plt.axis('off') # Hapus koordinat skala x,y
        
        # Kolom 2 (Tengah): Citra Peningkatan Mutu Smoothing
        plt.subplot(1, 3, 2)
        plt.imshow(img_smooth)
        plt.title("2. Smoothing (Box Filter 3x3)")
        plt.axis('off')
        
        # Kolom 3 (Kanan): Citra Peningkatan Mutu Sharpening
        plt.subplot(1, 3, 3)
        plt.imshow(img_sharpened)
        plt.title("3. Sharpening (Laplacian 3x3)")
        plt.axis('off')
        
        # Rapihkan Jarak Agar Rata dan Tampilkan Window Plot
        plt.tight_layout()
        plt.show()

# Pemanggilan root execute script
if __name__ == "__main__":
    main()
