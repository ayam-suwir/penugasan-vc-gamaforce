
import cv2
import matplotlib.pyplot as plt


def load_image(image_path):
    image_bgr = cv2.imread(image_path)
    
    if image_bgr is None:
        raise FileNotFoundError(f"Gambar tidak ditemukan: {image_path}")
    
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    
    return image_bgr, image_rgb, image_gray


def canny_filter(image_gray):
    blurred = cv2.GaussianBlur(image_gray, (5, 5), 1.5)
    canny = cv2.Canny(blurred, 0, 100)
    return canny


def sobel_filter(image_gray):
    blurred = cv2.GaussianBlur(image_gray, (3, 3), 0)
    
    sobel_x = cv2.Sobel(blurred, cv2.CV_16S, 1, 0, ksize=3)
    sobel_x = cv2.convertScaleAbs(sobel_x)
    
    sobel_y = cv2.Sobel(blurred, cv2.CV_16S, 0, 1, ksize=3)
    sobel_y = cv2.convertScaleAbs(sobel_y)
    
    sobel_combined = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
    
    return sobel_combined



def bilateral_filter(image_rgb):
    bilateral = cv2.bilateralFilter(image_rgb, 9, 75, 75)
    return bilateral


def visualize_results(original, canny, sobel, bilateral):
    fig, axes = plt.subplots(1, 4, figsize=(20, 5))
    axes[0].imshow(original)
    axes[0].set_title('Original Image', fontsize=12, fontweight='bold', pad=10)
    axes[0].axis('off')
    
    axes[1].imshow(canny, cmap='gray')
    axes[1].set_title('Canny Filter (Edge Detection)', fontsize=12, fontweight='bold', pad=10)
    axes[1].axis('off')
    
    axes[2].imshow(sobel, cmap='gray')
    axes[2].set_title('Sobel Filter', fontsize=12, fontweight='bold', pad=10)
    axes[2].axis('off')
    
    axes[3].imshow(bilateral)
    axes[3].set_title('Bilateral Filter', fontsize=12, fontweight='bold', pad=10)
    axes[3].axis('off')
    
    plt.tight_layout()
    return fig


def save_results(canny, sobel, bilateral):
    cv2.imwrite('canny_result.png', canny)
    cv2.imwrite('sobel_result.png', sobel)
    bilateral_bgr = cv2.cvtColor(bilateral, cv2.COLOR_RGB2BGR)
    cv2.imwrite('bilateral_result.png', bilateral_bgr)


def main():
    print("=" * 70)
    print("PROGRAM FILTER CANNY, SOBEL, DAN BILATERAL")
    print("=" * 70)
    
    image_path = "tulip.jpg"
    
    try:
        print(f"\nMemuat gambar: {image_path}")
        image_bgr, image_rgb, image_gray = load_image(image_path)
        print(f"Ukuran gambar: {image_rgb.shape[1]}x{image_rgb.shape[0]} pixels")
        
        print("\n\nMenerapkan filter: ")
        print("Canny Filter...")
        canny = canny_filter(image_gray)
        
        print("Sobel Filter...")
        sobel = sobel_filter(image_gray)
        
        print("Bilateral Filter...")
        bilateral = bilateral_filter(image_rgb)
        
        save_results(canny, sobel, bilateral)

        fig = visualize_results(image_rgb, canny, sobel, bilateral)
        plt.savefig('filter_result.png', dpi=300, bbox_inches='tight')
        
        plt.show()
        
        
    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("Pastikan file 'tulip.jpg' ada di folder yang sama dengan script.")
    except Exception as e:
        print(f"\nError: {e}")


if __name__ == "__main__":
    main()