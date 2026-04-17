import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def tampilkan_gambar(asli, hasil, judul_hasil):
    """Fungsi pembantu untuk menampilkan dua gambar bersandingan menggunakan matplotlib."""
    plt.figure(figsize=(12, 6))
    
    # Konversi BGR (format OpenCV) ke RGB (format Matplotlib)
    img_asli_rgb = cv2.cvtColor(asli, cv2.COLOR_BGR2RGB)
    img_hasil_rgb = cv2.cvtColor(hasil, cv2.COLOR_BGR2RGB)
    
    plt.subplot(1, 2, 1)
    plt.imshow(img_asli_rgb)
    plt.title("Original Image (Gambar Asli)")
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(img_hasil_rgb)
    plt.title("Enhanced Image (" + judul_hasil + ")")
    plt.axis('off')
    
    plt.tight_layout()
    plt.show()

def main():
    folder_dataset = 'dataset_bunga'
    
    # Pengecekan folder dataset
    if not os.path.exists(folder_dataset):
        os.makedirs(folder_dataset)
        print(f"Folder '{folder_dataset}' telah dibuat. Silakan masukkan file gambar ke dalamnya dan ulangi.")
        return
        
    list_file = [f for f in os.listdir(folder_dataset) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not list_file:
        print(f"Belum ada gambar di folder '{folder_dataset}'. Silakan tambahkan file gambar terlebih dahulu.")
        return
        
    # Ambil salah satu gambar pertama di dalam folder untuk mempraktikkan konvolusi
    path_file = os.path.join(folder_dataset, list_file[0])
    img = cv2.imread(path_file)
    
    if img is None:
        print(f"Gagal membaca gambar {path_file}")
        return

    # [Opsional] Menyamakan ukuran gambar maksimal agar filter 3x3 terlihat jelas detailnya
    maks_dimensi = 800
    h, w = img.shape[:2]
    if max(h, w) > maks_dimensi:
        skala = maks_dimensi / float(max(h, w))
        img = cv2.resize(img, (int(w * skala), int(h * skala)), interpolation=cv2.INTER_AREA)

    print(f"Menerapkan operasi filter konvolusi otomatis dari cv2.filter2D pada: {list_file[0]}")

    # =========================================================================
    # 1. Image Sharpening (Penajaman Citra)
    # Mask dengan center kuat (5) yang berfungsi meningkatkan kontras garis tepi
    # =========================================================================
    kernel_sharpening = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0]
    ], dtype=np.float32)
    
    # Menggunakan cv2.filter2D() untuk mengaplikasikan mask terhadap citra
    # ddepth = -1 berarti kedalaman warna citra hasil akan sama persis dengan citra input (contoh: np.uint8)
    img_sharpened = cv2.filter2D(src=img, ddepth=-1, kernel=kernel_sharpening)
    
    print("-> Menampilkan hasil Image Sharpening (Tutup jendela grafik untuk melihat filter selanjutnya)")
    tampilkan_gambar(img, img_sharpened, "Image Sharpening")


    # =========================================================================
    # 2. Edge Detection (Deteksi Tepi)
    # Mask akan memadamkan warna datar (center + 8 dikurangi sekeliling = 0)
    # dan hanya akan memunculkan nilai pixel pada pinggiran objek (sudut yang curam).
    # =========================================================================
    kernel_edge_detection = np.array([
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ], dtype=np.float32)

    img_edges = cv2.filter2D(src=img, ddepth=-1, kernel=kernel_edge_detection)
    
    print("-> Menampilkan hasil Edge Detection")
    tampilkan_gambar(img, img_edges, "Edge Detection (Laplacian)")

if __name__ == "__main__":
    main()
