import math

GRAVITASI = 9.81 

# Variable Input (Data Dummy)
kecepatan_pesawat_ms = 80.0

ketinggian_pesawat_m = 500.0  # Ketinggian pesawat relatif terhadap target dalam meter

posisi_pesawat_saat_ini = [1000.0, 500.0, 500.0]  # Asumsi: x = horizontal (arah terbang), y = lateral, z = vertikal

posisi_target_di_permukaan = [3500.0, 500.0, 0.0]  # Posisi target di permukaan tanah [x, y, z]

# Fungsi Perhitungan
def hitung_waktu_jatuh(ketinggian):
    if ketinggian <= 0:
        return 0.0
    
    try:
        waktu = math.sqrt((2 * ketinggian) / GRAVITASI)
        return waktu
    except (ValueError, ZeroDivisionError):
        return 0.0


def hitung_jarak_horizontal_ideal(kecepatan_horizontal, ketinggian):
    waktu_jatuh = hitung_waktu_jatuh(ketinggian)
    jarak_horizontal = kecepatan_horizontal * waktu_jatuh
    
    return jarak_horizontal


def hitung_jarak_3d(posisi_a, posisi_b):
    dx = posisi_b[0] - posisi_a[0]
    dy = posisi_b[1] - posisi_a[1]
    dz = posisi_b[2] - posisi_a[2]
    
    return math.sqrt(dx**2 + dy**2 + dz**2)


def hitung_jarak_horizontal_2d(posisi_a, posisi_b):
    dx = posisi_b[0] - posisi_a[0]
    dy = posisi_b[1] - posisi_a[1]
    
    return math.sqrt(dx**2 + dy**2)


def analisis_kondisi_penjatuhan(posisi_pesawat, posisi_target, jarak_ideal):
    jarak_ke_target = hitung_jarak_horizontal_2d(posisi_pesawat, posisi_target)
    selisih = jarak_ke_target - jarak_ideal
    
    toleransi = 10.0
    
    if abs(selisih) < toleransi:
        status = "SIAP JATUHKAN"
        rekomendasi = "Pesawat berada di posisi optimal untuk menjatuhkan paket."
    elif selisih > 0:
        status = "TERLALU JAUH"
        rekomendasi = f"Tunggu {selisih:.2f} meter lagi sebelum menjatuhkan paket."
    else:
        status = "SUDAH MELEWATI"
        rekomendasi = f"Pesawat sudah melewati titik optimal {abs(selisih):.2f} meter."
    
    return {
        "jarak_ke_target": jarak_ke_target,
        "selisih": selisih,
        "status": status,
        "rekomendasi": rekomendasi
    }


def hitung_kecepatan_saat_tiba(waktu_jatuh):
    return GRAVITASI * waktu_jatuh


# Fungsi Display
def cetak_garis(karakter="-", panjang=70):
    print(karakter * panjang)


def tampilkan_hasil_perhitungan():
    cetak_garis("=")
    print("   KALKULATOR JARAK JATUH PAKET (GERAK PARABOLA)")
    cetak_garis("=")
    print()
    
    print("DATA INPUT:")
    cetak_garis()
    print(f"   Kecepatan Pesawat      : {kecepatan_pesawat_ms} m/s "
          f"(~{kecepatan_pesawat_ms * 3.6:.1f} km/jam)")
    print(f"   Ketinggian Pesawat     : {ketinggian_pesawat_m} m")
    print(f"   Gravitasi              : {GRAVITASI} m/s^2")
    print(f"   Posisi Pesawat (x,y,z) : {posisi_pesawat_saat_ini}")
    print(f"   Posisi Target (x,y,z)  : {posisi_target_di_permukaan}")
    print()
    
    waktu_jatuh = hitung_waktu_jatuh(ketinggian_pesawat_m)
    jarak_ideal = hitung_jarak_horizontal_ideal(kecepatan_pesawat_ms, ketinggian_pesawat_m)
    kecepatan_tiba = hitung_kecepatan_saat_tiba(waktu_jatuh)
    
    print("HASIL PERHITUNGAN FISIKA:")
    cetak_garis()
    print(f"   Waktu Jatuh            : {waktu_jatuh:.2f} detik")
    print(f"   Jarak Horizontal Ideal : {jarak_ideal:.2f} meter")
    print(f"   Kecepatan Vertikal     : {kecepatan_tiba:.2f} m/s (saat tiba)")
    print()
    
    analisis = analisis_kondisi_penjatuhan(
        posisi_pesawat_saat_ini, 
        posisi_target_di_permukaan, 
        jarak_ideal
    )
    
    print("ANALISIS KONDISI PENJATUHAN:")
    cetak_garis()
    print(f"   Jarak ke Target        : {analisis['jarak_ke_target']:.2f} meter")
    print(f"   Selisih dari Ideal     : {analisis['selisih']:+.2f} meter")
    print(f"   Status                 : {analisis['status']}")
    print(f"   Rekomendasi            : {analisis['rekomendasi']}")
    print()
    
    print("KESIMPULAN:")
    cetak_garis()
    print(f"   Untuk mengenai target, pesawat harus menjatuhkan paket")
    print(f"   saat berada {jarak_ideal:.2f} meter SEBELUM target.")
    print()
    
    print("ASUMSI:")
    cetak_garis()
    print("   - Tidak ada hambatan udara (kondisi vakum)")
    print("   - Tidak ada angin")
    print("   - Permukaan tanah datar")
    print("   - Paket tidak berputar/stabil")
    cetak_garis("=")


# Eksekusi Program
if __name__ == "__main__":
    tampilkan_hasil_perhitungan()