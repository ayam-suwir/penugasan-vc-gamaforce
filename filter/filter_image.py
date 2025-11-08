"""
============================================================================
PROGRAM PENERAPAN FILTER CANNY, SOBEL, DAN BILATERAL
============================================================================
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


def load_image(image_path):
    """Memuat gambar dari path yang diberikan"""
    image_bgr = cv2.imread(image_path)
    
    if image_bgr is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {image_path}")
    
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    
    return image_bgr, image_rgb, image_gray


def apply_canny_filter(image_gray):
    """Menerapkan Canny Edge Detection dengan parameter optimal"""
    blurred = cv2.GaussianBlur(image_gray, (5, 5), 1.5)
    canny = cv2.Canny(blurred, 40, 120)
    return canny


def apply_sobel_filter(image_gray):
    """Menerapkan Sobel Filter dengan normalisasi optimal"""
    blurred = cv2.GaussianBlur(image_gray, (3, 3), 0)
    
    sobel_x = cv2.Sobel(blurred, cv2.CV_64F, 1, 0, ksize=5)
    sobel_y = cv2.Sobel(blurred, cv2.CV_64F, 0, 1, ksize=5)
    
    sobel_combined = np.sqrt(sobel_x**2 + sobel_y**2)
    sobel_combined = np.uint8(np.clip(sobel_combined, 0, 255))
    
    return sobel_combined


def apply_bilateral_filter(image_rgb):
    """Menerapkan Bilateral Filter dengan parameter optimal"""
    bilateral = cv2.bilateralFilter(image_rgb, 9, 75, 75)
    return bilateral


def visualize_results(original, canny, sobel, bilateral):
    """Menampilkan 4 hasil filter dalam 1 baris"""
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    fig.suptitle('HASIL PENERAPAN FILTER PADA GAMBAR', 
                 fontsize=16, fontweight='bold')
    
    axes[0].imshow(original)
    axes[0].set_title('Original Image', fontsize=12, fontweight='bold', pad=10)
    axes[0].axis('off')
    
    axes[1].imshow(canny, cmap='gray')
    axes[1].set_title('Canny Edge Detection', fontsize=12, fontweight='bold', pad=10)
    axes[1].axis('off')
    
    axes[2].imshow(sobel, cmap='gray')
    axes[2].set_title('Sobel Filter', fontsize=12, fontweight='bold', pad=10)
    axes[2].axis('off')
    
    axes[3].imshow(bilateral)
    axes[3].set_title('Bilateral Filter', fontsize=12, fontweight='bold', pad=10)
    axes[3].axis('off')
    
    plt.tight_layout()
    return fig


def save_individual_results(canny, sobel, bilateral):
    """Menyimpan hasil masing-masing filter"""
    cv2.imwrite('hasil_canny.png', canny)
    cv2.imwrite('hasil_sobel.png', sobel)
    bilateral_bgr = cv2.cvtColor(bilateral, cv2.COLOR_RGB2BGR)
    cv2.imwrite('hasil_bilateral.png', bilateral_bgr)


def print_filter_info():
    """Menampilkan informasi singkat tentang filter"""
    print("\nINFORMASI FILTER:")
    print("-" * 70)
    print("1. CANNY EDGE DETECTION")
    print("   Fungsi: Mendeteksi tepi/kontur objek pada gambar")
    print("   Kegunaan: Segmentasi objek, deteksi bentuk, ekstraksi fitur")
    print("   Parameter: Threshold 40-120, Gaussian Blur 5x5")
    
    print("\n2. SOBEL FILTER")
    print("   Fungsi: Menghitung gradien intensitas gambar")
    print("   Kegunaan: Deteksi tepi, analisis tekstur, edge detection")
    print("   Parameter: Kernel 5x5, magnitude normalisasi")
    
    print("\n3. BILATERAL FILTER")
    print("   Fungsi: Smoothing dengan preservasi tepi")
    print("   Kegunaan: Noise reduction, image enhancement, denoising")
    print("   Parameter: d=9, sigma_color=75, sigma_space=75")
    print("-" * 70)


def main():
    """Fungsi utama"""
    print("=" * 70)
    print("PROGRAM FILTER CANNY, SOBEL, DAN BILATERAL")
    print("=" * 70)
    
    image_path = "tulip.jpg"
    
    try:
        print(f"\nMemuat gambar: {image_path}")
        image_bgr, image_rgb, image_gray = load_image(image_path)
        print(f"Ukuran gambar: {image_rgb.shape[1]}x{image_rgb.shape[0]} pixels")
        
        print_filter_info()
        
        print("\n\nMenerapkan filter...")
        print("- Canny Edge Detection...")
        canny = apply_canny_filter(image_gray)
        
        print("- Sobel Filter...")
        sobel = apply_sobel_filter(image_gray)
        
        print("- Bilateral Filter...")
        bilateral = apply_bilateral_filter(image_rgb)
        
        print("\nMenyimpan hasil individual...")
        save_individual_results(canny, sobel, bilateral)
        print("  - hasil_canny.png")
        print("  - hasil_sobel.png")
        print("  - hasil_bilateral.png")
        
        print("\nMenampilkan visualisasi...")
        fig = visualize_results(image_rgb, canny, sobel, bilateral)
        plt.savefig('hasil_filter_lengkap.png', dpi=300, bbox_inches='tight')
        print("  - hasil_filter_lengkap.png")
        
        plt.show()
        
        print("\n" + "=" * 70)
        print("SELESAI!")
        print("=" * 70)
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Pastikan file 'tulip.jpg' ada di folder yang sama dengan script.")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()