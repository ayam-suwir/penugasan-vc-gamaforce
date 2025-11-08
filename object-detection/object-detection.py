import cv2
import numpy as np
import matplotlib.pyplot as plt

def Object_Detection(input):
    # Membaca gambar input
    original_image = cv2.imread(input)
    
    if original_image is None:
        print(f"Error: Gagal membaca gambar '{input}'.")
        print("Pastikan file gambar ada di direktori yang sama dengan script ini.")
        return

    result_image = original_image.copy()
    hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

    # Definisi Warna (BGR) & Kernel
    GREEN = (0, 255, 0)
    CYAN = (255, 255, 0)
    YELLOW = (0, 255, 255)
    PURPLE = (255, 0, 255)
    BLUE = (255, 0, 0)
    kernel = np.ones((5, 5), np.uint8)

    # Mendeteksi Landzone (Biru)
    lower_blue = np.array([100, 100, 50])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_CLOSE, kernel)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contours_blue:
        if cv2.contourArea(c) > 1000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(result_image, (x, y), (x + w, y + h), GREEN, 2)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.drawMarker(result_image, (cX, cY), CYAN, cv2.MARKER_CROSS, 20, 2)
            cv2.putText(result_image, "LANDZONE", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, GREEN, 2)

    # Mendeteksi Dropzone (Oranye)
    lower_orange = np.array([10, 100, 100])
    upper_orange = np.array([25, 255, 255])
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_orange = cv2.morphologyEx(mask_orange, cv2.MORPH_CLOSE, kernel)
    contours_orange, _ = cv2.findContours(mask_orange, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contours_orange:
        if cv2.contourArea(c) > 1000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(result_image, (x, y), (x + w, y + h), GREEN, 2)
            cv2.putText(result_image, "DROPZONE", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, GREEN, 2)
    
    # Mendeteksi Target Dropzone (Lingkaran abu-abu)
    lower_grey = np.array([0, 0, 180])
    upper_grey = np.array([180, 50, 255])
    mask_grey = cv2.inRange(hsv, lower_grey, upper_grey)
    mask_grey = cv2.morphologyEx(mask_grey, cv2.MORPH_CLOSE, kernel)
    
    contours_white, _ = cv2.findContours(mask_grey, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contours_white:
        if cv2.contourArea(c) > 500:
            ((cx_c, cy_c), radius) = cv2.minEnclosingCircle(c)
            
            cv2.circle(result_image, (int(cx_c), int(cy_c)), int(radius), PURPLE, 2) 
            
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.drawMarker(result_image, (cX, cY), BLUE, cv2.MARKER_CROSS, 20, 2)

    # Mendeteksi Bucket (Merah)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
    
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for c in contours_red:
        if cv2.contourArea(c) > 500:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(result_image, (x, y), (x + w, y + h), GREEN, 2)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.drawMarker(result_image, (cX, cY), YELLOW, cv2.MARKER_CROSS, 20, 2)
            cv2.putText(result_image, "BUCKET", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, GREEN, 2)
                
    # Menampilkan Hasil
    img_rgb_orig = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    img_rgb_result = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(16, 8))
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(img_rgb_orig)
    plt.axis('on')

    plt.subplot(1, 2, 2)
    plt.title("Result")
    plt.imshow(img_rgb_result)
    plt.axis('on')

    plt.show()
    
    cv2.imwrite("result.png", result_image)
    print("Gambar hasil deteksi disimpan sebagai 'result.png'")


input = "input.png" 
Object_Detection(input)