import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
import networkx as nx
import numpy as np
from PIL import Image
from io import BytesIO

# Konfigurasi halaman
st.set_page_config(page_title="Visualisasi Model Pengolahan Citra", layout="wide")
st.title("📊 Visualisasi Model Pengolahan Citra Fashion")

# Fungsi untuk membuat diagram alir
def create_flowchart():
    st.subheader("📈 Diagram Alir Proses Pengolahan Citra")
    
    # Buat gambar diagram
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_facecolor('#f8f9fa')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Judul diagram
    plt.text(5, 5.5, 'Alur Pengolahan Citra Fashion', 
             fontsize=18, ha='center', va='center', fontweight='bold', color='#1f6aa5')
    
    # Koordinat node
    nodes = {
        'input': (1, 4),
        'resize': (3, 4),
        'rgb': (5, 4),
        'gray': (5, 3),
        'edges': (5, 2),
        'hist_rgb': (7, 4),
        'hist_gray': (7, 3),
        'hist_edges': (7, 2),
        'output': (9, 3)
    }
    
    # Gambar node
    node_shapes = {
        'input': ('s', 'Input Gambar', '#4e73df'),
        'resize': ('d', 'Resize & Normalisasi', '#36b9cc'),
        'rgb': ('o', 'Gambar RGB', '#1cc88a'),
        'gray': ('o', 'Grayscale', '#6f42c1'),
        'edges': ('o', 'Deteksi Tepi', '#e74a3b'),
        'hist_rgb': ('s', 'Histogram RGB', '#1cc88a'),
        'hist_gray': ('s', 'Histogram Grayscale', '#6f42c1'),
        'hist_edges': ('s', 'Histogram Edges', '#e74a3b'),
        'output': ('s', 'Output Analisis', '#5a5c69')
    }
    
    # Gambar semua node
    for node, (x, y) in nodes.items():
        shape, label, color = node_shapes[node]
        
        if shape == 'o':  # Lingkaran
            circle = Circle((x, y), 0.4, facecolor=color, edgecolor='black', alpha=0.8)
            ax.add_patch(circle)
        elif shape == 's':  # Kotak
            rect = Rectangle((x-0.5, y-0.3), 1, 0.6, facecolor=color, edgecolor='black', alpha=0.8)
            ax.add_patch(rect)
        else:  # Diamond
            poly = plt.Polygon([(x, y+0.4), (x+0.4, y), (x, y-0.4), (x-0.4, y)], 
                              facecolor=color, edgecolor='black', alpha=0.8)
            ax.add_patch(poly)
            
        plt.text(x, y, label, ha='center', va='center', color='white', fontweight='bold')
    
    # Gambar koneksi
    connections = [
        ('input', 'resize'),
        ('resize', 'rgb'),
        ('rgb', 'gray'),
        ('rgb', 'hist_rgb'),
        ('gray', 'edges'),
        ('gray', 'hist_gray'),
        ('edges', 'hist_edges'),
        ('hist_rgb', 'output'),
        ('hist_gray', 'output'),
        ('hist_edges', 'output')
    ]
    
    for start, end in connections:
        x1, y1 = nodes[start]
        x2, y2 = nodes[end]
        
        # Buat panah
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#5a5c69", linewidth=1.5, alpha=0.7))
    
    # Tambahkan penjelasan
    plt.text(1, 1, "Keterangan:", fontsize=12, fontweight='bold', color='#1f6aa5')
    plt.text(1, 0.7, "• Kotak: Input/Output", fontsize=10)
    plt.text(1, 0.4, "• Belah Ketupat: Transformasi", fontsize=10)
    plt.text(1, 0.1, "• Lingkaran: Representasi Gambar", fontsize=10)
    
    st.pyplot(fig)

# Fungsi untuk membuat diagram jaringan proses
def create_process_graph():
    st.subheader("🧠 Diagram Jaringan Proses Pengolahan Citra")
    
    G = nx.DiGraph()
    
    # Tambahkan node
    G.add_node("Input Gambar", pos=(0, 3), color="#4e73df")
    G.add_node("Resize & Normalisasi", pos=(2, 3), color="#36b9cc")
    G.add_node("Gambar RGB", pos=(4, 4), color="#1cc88a")
    G.add_node("Grayscale", pos=(4, 3), color="#6f42c1")
    G.add_node("Deteksi Tepi (Canny)", pos=(4, 2), color="#e74a3b")
    G.add_node("Histogram RGB", pos=(6, 4), color="#1cc88a")
    G.add_node("Histogram Grayscale", pos=(6, 3), color="#6f42c1")
    G.add_node("Histogram Edges", pos=(6, 2), color="#e74a3b")
    G.add_node("Analisis & Visualisasi", pos=(8, 3), color="#5a5c69")
    
    # Tambahkan edge
    G.add_edges_from([
        ("Input Gambar", "Resize & Normalisasi"),
        ("Resize & Normalisasi", "Gambar RGB"),
        ("Gambar RGB", "Grayscale"),
        ("Gambar RGB", "Histogram RGB"),
        ("Grayscale", "Deteksi Tepi (Canny)"),
        ("Grayscale", "Histogram Grayscale"),
        ("Deteksi Tepi (Canny)", "Histogram Edges"),
        ("Histogram RGB", "Analisis & Visualisasi"),
        ("Histogram Grayscale", "Analisis & Visualisasi"),
        ("Histogram Edges", "Analisis & Visualisasi")
    ])
    
    # Dapatkan posisi dan warna
    pos = nx.get_node_attributes(G, 'pos')
    colors = [G.nodes[n]['color'] for n in G.nodes()]
    
    # Gambar graf
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_facecolor('#f8f9fa')
    
    nx.draw_networkx_nodes(G, pos, node_size=3000, node_color=colors, alpha=0.8, edgecolors='black')
    nx.draw_networkx_edges(G, pos, edge_color="#5a5c69", width=2, alpha=0.7, arrowsize=20)
    nx.draw_networkx_labels(G, pos, font_color='white', font_weight='bold')
    
    plt.title("Jaringan Proses Pengolahan Citra", fontsize=16, fontweight='bold', color='#1f6aa5')
    plt.axis('off')
    
    st.pyplot(fig)

# Visualisasi algoritma Canny
def visualize_canny_algorithm():
    st.subheader("🔍 Visualisasi Algoritma Canny Edge Detection")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Tahapan Algoritma Canny:**
        
        1. **Noise Reduction**  
           Menggunakan Gaussian blur untuk mengurangi noise
           ```python
           blurred = cv2.GaussianBlur(gray, (5, 5), 0)
           ```
        
        2. **Gradient Calculation**  
           Menghitung gradien menggunakan operator Sobel
           ```python
           grad_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=3)
           grad_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=3)
           ```
        
        3. **Non-Maximum Suppression**  
           Menipiskan tepi ke lebar satu piksel
           ```python
           magnitude = np.sqrt(grad_x**2 + grad_y**2)
           direction = np.arctan2(grad_y, grad_x)
           ```
        
        4. **Double Thresholding**  
           Mengklasifikasikan tepi menjadi kuat, lemah, dan bukan tepi
           ```python
           strong_edges = (magnitude > high_threshold)
           weak_edges = (magnitude >= low_threshold) & (magnitude <= high_threshold)
           ```
        
        5. **Edge Tracking by Hysteresis**  
           Menghubungkan tepi kuat dan tepi lemah yang terhubung
        """)
    
    with col2:
        # Buat visualisasi diagram
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.set_facecolor('#f8f9fa')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6)
        ax.axis('off')
        
        # Judul
        plt.text(5, 5.5, 'Algoritma Canny Edge Detection', 
                 fontsize=16, ha='center', va='center', fontweight='bold', color='#e74a3b')
        
        # Tahapan
        steps = [
            (2, 4.5, '1. Noise Reduction\n(Gaussian Blur)', '#4e73df'),
            (5, 4.5, '2. Gradient Calculation\n(Sobel Operator)', '#36b9cc'),
            (8, 4.5, '3. Non-Maximum\nSuppression', '#1cc88a'),
            (3, 2.5, '4. Double\nThresholding', '#6f42c1'),
            (7, 2.5, '5. Edge Tracking\nby Hysteresis', '#e74a3b')
        ]
        
        # Gambar tahapan
        for x, y, label, color in steps:
            circle = Circle((x, y), 0.8, facecolor=color, edgecolor='black', alpha=0.8)
            ax.add_patch(circle)
            plt.text(x, y, label, ha='center', va='center', color='white', fontweight='bold')
        
        # Gambar panah
        arrows = [
            ((2, 3.7), (5, 3.7)),
            ((5, 3.7), (8, 3.7)),
            ((8, 3.7), (7, 3.0)),
            ((7, 2.2), (3, 2.2)),
            ((3, 2.2), (2, 3.0))
        ]
        
        for (x1, y1), (x2, y2) in arrows:
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color="#5a5c69", linewidth=1.5, alpha=0.7))
        
        st.pyplot(fig)

# Visualisasi histogram
def visualize_histogram_process():
    st.subheader("🎨 Proses Pembuatan Histogram")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Proses Pembuatan Histogram:**
        
        1. **Ekstraksi Channel Warna**  
           Memisahkan gambar RGB menjadi channel Red, Green, Blue
           ```python
           r = img[:, :, 0]
           g = img[:, :, 1]
           b = img[:, :, 2]
           ```
        
        2. **Perhitungan Distribusi**  
           Menghitung frekuensi intensitas piksel untuk setiap channel
           ```python
           hist_r = cv2.calcHist([img], [0], None, [256], [0, 256])
           hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
           hist_b = cv2.calcHist([img], [2], None, [256], [0, 256])
           ```
        
        3. **Normalisasi (Opsional)**  
           Menyesuaikan nilai histogram untuk visualisasi yang lebih baik
           ```python
           hist_r = hist_r / hist_r.max()
           ```
        
        4. **Visualisasi**  
           Menampilkan hasil dalam bentuk grafik line plot
           ```python
           plt.plot(hist_r, color='red')
           plt.plot(hist_g, color='green')
           plt.plot(hist_b, color='blue')
           ```
        """)
    
    with col2:
        # Buat contoh histogram
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Generate contoh data histogram
        x = np.arange(256)
        hist_r = np.exp(-(x-150)**2/(2*30**2)) * 10000
        hist_g = np.exp(-(x-100)**2/(2*40**2)) * 8000
        hist_b = np.exp(-(x-50)**2/(2*50**2)) * 12000
        
        # Plot histogram
        ax.plot(x, hist_r, color='red', linewidth=2, label='Red Channel')
        ax.plot(x, hist_g, color='green', linewidth=2, label='Green Channel')
        ax.plot(x, hist_b, color='blue', linewidth=2, label='Blue Channel')
        
        ax.set_title('Contoh Histogram RGB', fontsize=14)
        ax.set_xlabel('Intensitas Piksel', fontsize=12)
        ax.set_ylabel('Frekuensi', fontsize=12)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_facecolor('#f8f9fa')
        
        st.pyplot(fig)

# Fungsi utama
def main():
    st.markdown("""
    <style>
    .big-font {
        font-size:18px !important;
        line-height: 1.6;
    }
    .highlight {
        background-color: #e6f7ff;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #1f6aa5;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="highlight">
        <p class="big-font">
        Model pengolahan citra ini dirancang khusus untuk analisis gambar fashion. 
        Prosesnya terdiri dari beberapa tahap transformasi dan ekstraksi fitur yang 
        menghasilkan representasi visual yang lebih informatif.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Diagram Alir Proses", 
        "Jaringan Proses", 
        "Algoritma Canny", 
        "Histogram"
    ])
    
    with tab1:
        create_flowchart()
        
        st.markdown("""
        **Penjelasan Diagram Alir:**
        
        1. **Input Gambar**: Gambar fashion asli yang akan diproses
        2. **Resize & Normalisasi**: Penyesuaian ukuran gambar dan normalisasi nilai piksel
        3. **Gambar RGB**: Representasi warna asli gambar
        4. **Grayscale**: Konversi ke skala abu-abu untuk analisis intensitas
        5. **Deteksi Tepi**: Identifikasi tepi objek menggunakan algoritma Canny
        6. **Histogram RGB**: Distribusi warna dalam gambar
        7. **Histogram Grayscale**: Distribusi intensitas cahaya
        8. **Histogram Edges**: Distribusi tepi yang terdeteksi
        9. **Output Analisis**: Hasil akhir berupa visualisasi dan analisis fitur
        """)
    
    with tab2:
        create_process_graph()
        
        st.markdown("""
        **Penjelasan Jaringan Proses:**
        
        - Model ini menunjukkan hubungan antar komponen dalam sistem
        - Setiap node mewakili tahap pemrosesan tertentu
        - Panah menunjukkan alur data dan ketergantungan antar proses
        - Proses paralel (seperti pembuatan histogram) dapat berjalan secara bersamaan
        """)
    
    with tab3:
        visualize_canny_algorithm()
        
        st.markdown("""
        **Detail Algoritma Canny:**
        
        Algoritma Canny adalah metode deteksi tepi yang optimal dengan karakteristik:
        
        - **Daya tangkap tepi yang baik**: Mendeteksi tepi yang lemah dan kuat
        - **Lokalisasi yang akurat**: Tepi ditempatkan pada posisi yang tepat
        - **Respon minimal**: Satu tepi hanya menghasilkan satu respon
        
        Parameter utama:
        ```python
        edges = cv2.Canny(image, threshold1, threshold2)
        ```
        
        - `threshold1`: Nilai ambang rendah untuk tepi lemah
        - `threshold2`: Nilai ambang tinggi untuk tepi kuat
        """)
    
    with tab4:
        visualize_histogram_process()
        
        st.markdown("""
        **Interpretasi Histogram:**
        
        Histogram memberikan informasi penting tentang karakteristik gambar:
        
        - **Distribusi Warna**:
          - Puncak di area merah: Dominasi warna hangat
          - Puncak di area biru: Dominasi warna dingin
        
        - **Kontras Gambar**:
          - Histogram lebar: Kontras tinggi
          - Histogram sempit: Kontras rendah
        
        - **Pencahayaan**:
          - Puncak di kiri: Gambar gelap
          - Puncak di kanan: Gambar terang
          - Puncak di tengah: Pencahayaan seimbang
        """)
    
    st.markdown("---")
    st.subheader("💡 Kesimpulan")
    st.markdown("""
    Model pengolahan citra fashion ini mengimplementasikan teknik-teknik dasar pengolahan citra 
    yang efektif untuk analisis produk fashion. Proses utamanya meliputi:
    
    - **Preprocessing**: Persiapan gambar untuk analisis lebih lanjut
    - **Transformasi**: Konversi ruang warna dan deteksi fitur
    - **Ekstraksi Fitur**: Pengambilan karakteristik visual gambar
    - **Visualisasi**: Penyajian hasil dalam bentuk yang informatif
    
    Dengan model ini, kita dapat menganalisis berbagai aspek visual produk fashion seperti:
    distribusi warna, kontras, tekstur, dan bentuk produk.
    """)

if __name__ == "__main__":
    main()