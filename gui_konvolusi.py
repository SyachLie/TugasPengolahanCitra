import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk
import os

class KonvolusiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Program Konvolusi Citra Digital (OpenCV GUI)")
        self.root.geometry("1100x650")
        self.root.configure(bg="#2D3035")
        
        # Variabel Internal
        self.img_path = None
        self.img_bgr = None
        self.img_rgb = None
        self.img_result = None
        
        # --- UI LAYOUT MAKER ---
        # Frame Atas untuk Kontrol
        self.top_frame = tk.Frame(self.root, bg="#1E2024", bd=2, relief=tk.FLAT)
        self.top_frame.pack(side=tk.TOP, fill=tk.X, pady=10, padx=20)
        
        # Frame Bawah untuk Panel Gambar Asli vs Hasil
        self.mid_frame = tk.Frame(self.root, bg="#2D3035")
        self.mid_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Tombol Buka Gambar
        self.btn_buka = tk.Button(self.top_frame, text="📁 Buka Gambar...", command=self.load_image, 
                                  font=("Segoe UI", 11, "bold"), fg="white", bg="#3B82F6", 
                                  activebackground="#2563EB", activeforeground="white", 
                                  relief=tk.FLAT, padx=15, pady=8, cursor="hand2")
        self.btn_buka.pack(side=tk.LEFT, padx=15, pady=10)
        
        # Dropdown Pilih Filter
        self.label_filter = tk.Label(self.top_frame, text="Pilih Kernel Filter:", bg="#1E2024", fg="white", font=("Segoe UI", 11))
        self.label_filter.pack(side=tk.LEFT, padx=(20, 5))
        
        self.var_filter = tk.StringVar()
        self.var_filter.set("Sharpening") 
        
        style = ttk.Style()
        style.configure("TCombobox", padding=5)
        
        self.dropdown = ttk.Combobox(self.top_frame, textvariable=self.var_filter, state="readonly", 
                                     font=("Segoe UI", 11), width=25)
        self.dropdown['values'] = (
            "Sharpening", 
            "Edge Detection", 
            "Smoothing (Box Filter)",
            "Emboss Effect",
            "Sobel X (Garis Vertikal)",
            "Sobel Y (Garis Horizontal)",
            "Motion Blur",
            "Tanpa Filter (Original)"
        )
        self.dropdown.pack(side=tk.LEFT, padx=5)
        self.dropdown.bind("<<ComboboxSelected>>", lambda e: self.apply_filter())
        
        # Tombol Simpan Hasil
        self.btn_simpan = tk.Button(self.top_frame, text="💾 Simpan Hasil Hasil", command=self.save_image, 
                                  font=("Segoe UI", 11, "bold"), fg="white", bg="#10B981", 
                                  activebackground="#059669", activeforeground="white", 
                                  relief=tk.FLAT, padx=15, pady=8, cursor="hand2", state=tk.DISABLED)
        self.btn_simpan.pack(side=tk.RIGHT, padx=15, pady=10)
        
        # --- KANVAS GAMBAR ---
        # Panel Kiri (Asli)
        self.panel_asli_container = tk.Frame(self.mid_frame, bg="#1E2024", bd=0)
        self.panel_asli_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        self.label_asli_title = tk.Label(self.panel_asli_container, text="📸 GAMBAR ASLI", bg="#1E2024", fg="#9CA3AF", font=("Segoe UI", 12, "bold"))
        self.label_asli_title.pack(side=tk.TOP, pady=10)
        
        self.panel_asli = tk.Label(self.panel_asli_container, bg="#1E2024", text="Pilih Gambar untuk Memulai", fg="#4B5563", font=("Segoe UI", 14))
        self.panel_asli.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)
        
        # Panel Kanan (Hasil)
        self.panel_hasil_container = tk.Frame(self.mid_frame, bg="#1E2024", bd=0)
        self.panel_hasil_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.label_hasil_title = tk.Label(self.panel_hasil_container, text="✨ HASIL KONVOLUSI", bg="#1E2024", fg="#9CA3AF", font=("Segoe UI", 12, "bold"))
        self.label_hasil_title.pack(side=tk.TOP, pady=10)
        
        self.panel_hasil = tk.Label(self.panel_hasil_container, bg="#1E2024")
        self.panel_hasil.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Pilih Gambar",
            filetypes=(("Semua File Gambar", "*.jpg;*.jpeg;*.png;*.bmp;*.webp"), 
                       ("JPEG", "*.jpg;*.jpeg"), 
                       ("PNG", "*.png"))
        )
        if file_path:
            self.img_path = file_path
            
            # Membaca gambar menggunakan OpenCV
            self.img_bgr = cv2.imread(self.img_path)
            if self.img_bgr is None:
                messagebox.showerror("Error", f"Gagal membaca format gambar pada path:\n{self.img_path}")
                return
                
            # Konversi untuk display Matplotlib/Tkinter yang membaca format RGB
            self.img_rgb = cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2RGB)
            
            # Tampilkan Gambar Asli ke UI
            self.display_image(self.img_rgb, self.panel_asli)
            
            # Otomatis langsung eksekusi filter yang terpilih dan aktifkan tombol simpan
            self.apply_filter()
            self.btn_simpan.config(state=tk.NORMAL)

    def apply_filter(self):
        # Hindari eksekusi saat user belum masukin gambar
        if self.img_rgb is None:
            return
            
        choice = self.var_filter.get()
        
        if choice == "Tanpa Filter (Original)":
            self.img_result = self.img_rgb.copy()
            self.label_hasil_title.config(text="✨ HASIL: TANPA FILTER", fg="#9CA3AF")
            
        elif choice == "Sharpening":
            # Mask Sharpening
            kernel = np.array([
                [ 0, -1,  0],
                [-1,  5, -1],
                [ 0, -1,  0]
            ], dtype=np.float32)
            self.img_result = cv2.filter2D(self.img_rgb, -1, kernel)
            self.label_hasil_title.config(text="✨ HASIL: IMAGE SHARPENING", fg="#34D399")
            
        elif choice == "Edge Detection":
            # Mask Log/Laplacian Tepi
            kernel = np.array([
                [-1, -1, -1],
                [-1,  8, -1],
                [-1, -1, -1]
            ], dtype=np.float32)
            self.img_result = cv2.filter2D(self.img_rgb, -1, kernel)
            self.label_hasil_title.config(text="✨ HASIL: EDGE DETECTION", fg="#FBBF24")
            
        elif choice == "Smoothing (Box Filter)":
            # Mask Box Rata-Rata
            kernel = np.ones((5, 5), dtype=np.float32) / 25.0
            self.img_result = cv2.filter2D(self.img_rgb, -1, kernel)
            self.label_hasil_title.config(text="✨ HASIL: SMOOTHING", fg="#60A5FA")

        elif choice == "Emboss Effect":
            # Mask Emboss (Efek Gambar Timbul)
            kernel = np.array([
                [-2, -1,  0],
                [-1,  1,  1],
                [ 0,  1,  2]
            ], dtype=np.float32)
            # Karena emboss menghasilkan nilai banyak negatif/nol, biasanya ditambahkan +128 untuk abu-abu
            # Tetapi filter2D memotong di 0, jadi tetap estetik dengan warna gelap
            self.img_result = cv2.filter2D(self.img_rgb, -1, kernel)
            self.img_result = cv2.add(self.img_result, np.array([128.0])) 
            self.label_hasil_title.config(text="✨ HASIL: EMBOSS EFFECT", fg="#C084FC")

        elif choice == "Sobel X (Garis Vertikal)":
            # Mendeteksi Tepi Vertikal
            kernel = np.array([
                [-1,  0,  1],
                [-2,  0,  2],
                [-1,  0,  1]
            ], dtype=np.float32)
            self.img_result = cv2.filter2D(self.img_rgb, -1, kernel)
            self.label_hasil_title.config(text="✨ HASIL: SOBEL X (VERTIKAL)", fg="#F472B6")

        elif choice == "Sobel Y (Garis Horizontal)":
            # Mendeteksi Tepi Horizontal
            kernel = np.array([
                [-1, -2, -1],
                [ 0,  0,  0],
                [ 1,  2,  1]
            ], dtype=np.float32)
            self.img_result = cv2.filter2D(self.img_rgb, -1, kernel)
            self.label_hasil_title.config(text="✨ HASIL: SOBEL Y (HORIZONTAL)", fg="#F472B6")

        elif choice == "Motion Blur":
            # Mask Kabur seperti bergerak horizontal
            size = 15
            kernel = np.zeros((size, size), dtype=np.float32)
            kernel[int((size-1)/2), :] = np.ones(size, dtype=np.float32)
            kernel /= size
            self.img_result = cv2.filter2D(self.img_rgb, -1, kernel)
            self.label_hasil_title.config(text="✨ HASIL: MOTION BLUR", fg="#818CF8")
            
        self.display_image(self.img_result, self.panel_hasil)

    def display_image(self, img_array, panel):
        h, w = img_array.shape[:2]
        
        # Responsif: Resize layar GUI (Maks ukuran panel 500x500 di dalam frame)
        max_width = 500
        max_height = 500
        scale = min(max_width/w, max_height/h)
        
        # Mengecilkan gambar yang terlalu besar agar bisa dilihat secara proporsional. 
        # Jika gambar sudah kecil d biarkan saja.
        if scale < 1:
            new_w, new_h = int(w * scale), int(h * scale)
            img_resized = cv2.resize(img_array, (new_w, new_h), interpolation=cv2.INTER_AREA)
        else:
            img_resized = img_array
            
        # Konversi array Numpy -> PIL Image -> tk ImageTk
        img_pil = Image.fromarray(img_resized)
        img_tk = ImageTk.PhotoImage(image=img_pil)
        
        # Masukkan / Ubah isi Label untuk merender gambar
        panel.config(image=img_tk, text="") 
        panel.image = img_tk  # Menahan reference agar tidak terhapus Garbage Collector Python

    def save_image(self):
        if self.img_result is None:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("Semua File", "*.*")],
            title="Pilih Lokasi untuk Menyimpan Hasil"
        )
        if file_path:
            # Kembalikan gambar ke tipe BGR karena standard penyimpanan OpenCV adalah BGR
            result_bgr = cv2.cvtColor(self.img_result, cv2.COLOR_RGB2BGR)
            cv2.imwrite(file_path, result_bgr)
            messagebox.showinfo("Berhasil! 🎉", f"Gambar Filtered berhasil disimpan ke:\n{file_path}")

if __name__ == "__main__":
    # Inisiasi engine GUI Tkinter
    root = tk.Tk()
    app = KonvolusiGUI(root)
    # Loop Render Window
    root.mainloop()
