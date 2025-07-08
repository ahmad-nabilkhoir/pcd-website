import streamlit as st
import os
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from pathlib import Path
import random

st.set_page_config(page_title="Deteksi Gambar Fashion", layout="wide")
st.title("🧥 Deteksi Gambar Fashion + Pengolahan Citra")

# ========== KONFIGURASI PATH YANG AMAN ==========
# Gunakan raw string untuk menghindari masalah backslash
IMAGE_DIR = Path("data/images/Shoe vs Sandal vs Boot Dataset")

# ========== FUNGSI UTAMA ==========
def main():
    # 1. Verifikasi folder gambar
    if not IMAGE_DIR.exists():
        st.error(f"❌ FOLDER GAMBAR TIDAK DITEMUKAN: {IMAGE_DIR}")
        st.info("Pastikan path folder benar dan gambar ada di dalamnya")
        st.info("Tips: Gunakan path dengan format raw string seperti r'D:\\path\\to\\folder'")
        return
    
    # 2. Dapatkan semua file gambar dari seluruh subfolder
    image_files = []
    valid_extensions = ['.jpg', '.jpeg', '.png', '.JPG', '.JPEG', '.PNG']
    
    # Traverse semua subdirectories
    for root, _, files in os.walk(IMAGE_DIR):
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix.lower() in valid_extensions:
                image_files.append(file_path)
    
    if not image_files:
        st.error("❌ TIDAK ADA FILE GAMBAR YANG DITEMUKAN DI FOLDER")
        st.info(f"Format yang didukung: {', '.join(valid_extensions)}")
        st.info(f"Pastikan folder tidak kosong: {IMAGE_DIR}")
        return
    
    st.success(f"✅ Ditemukan {len(image_files)} gambar di folder")
    
    # 3. Pilih 5 gambar acak
    selected_images = random.sample(image_files, min(5, len(image_files)))
    
    for img_path in selected_images:
        try:
            # Proses gambar
            img = Image.open(img_path).convert("RGB")
            img_np = np.array(img)
            
            # Resize gambar jika terlalu besar
            max_size = 800
            if img_np.shape[1] > max_size or img_np.shape[0] > max_size:
                scale = max_size / max(img_np.shape[1], img_np.shape[0])
                new_width = int(img_np.shape[1] * scale)
                new_height = int(img_np.shape[0] * scale)
                img_np = cv2.resize(img_np, (new_width, new_height))
            
            gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            
            # Tampilkan informasi
            st.markdown(f"### 📁 File: `{img_path.name}`")
            st.markdown(f"**Lokasi:** `{img_path}`")
            
            # Tampilkan gambar - PERBAIKAN DI SINI
            col1, col2, col3 = st.columns(3)
            col1.image(img_np, caption="Gambar Asli", use_container_width=True)  # Diubah
            col2.image(gray, caption="Grayscale", use_container_width=True, channels="GRAY")  # Diubah
            col3.image(edges, caption="Deteksi Tepi", use_container_width=True, channels="GRAY")  # Diubah
            
            # Histogram
            st.subheader("📊 Histogram Warna")
            fig, ax = plt.subplots(1, 2, figsize=(12, 4))
            
            # Histogram RGB
            ax[0].set_title("Histogram RGB")
            colors = ('r', 'g', 'b')
            for i, color in enumerate(colors):
                hist = cv2.calcHist([img_np], [i], None, [256], [0, 256])
                ax[0].plot(hist, color=color)
            ax[0].set_xlim([0, 256])
            
            # Histogram Grayscale
            ax[1].set_title("Histogram Grayscale")
            hist_gray = cv2.calcHist([gray], [0], None, [256], [0, 256])
            ax[1].plot(hist_gray, color='black')
            ax[1].set_xlim([0, 256])
            
            st.pyplot(fig)
            plt.close(fig)  # Tutup plot untuk menghindari memory leak
            
            st.markdown("---")
            
        except Exception as e:
            st.error(f"Gagal memproses {img_path.name}: {str(e)}")
            continue

# ========== JALANKAN APLIKASI ==========
if __name__ == "__main__":
    main()