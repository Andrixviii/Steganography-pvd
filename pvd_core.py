from PIL import Image
import math

# Tabel jangkauan kuantisasi yang telah ditentukan
RANGE_TABLE = [
    (0, 7, 3),    # (lower_bound, upper_bound, bits_to_embed)
    (8, 15, 3),
    (16, 31, 4),
    (32, 63, 5),
    (64, 127, 6),
    (128, 255, 7)
]

def get_range_for_diff(diff):
    """Mencari jangkauan yang sesuai untuk nilai perbedaan absolut."""
    abs_diff = abs(diff)
    for lower, upper, bits in RANGE_TABLE:
        if lower <= abs_diff <= upper:
            return (lower, upper, bits)
    return None

def message_to_binary(message):
    """Mengonversi pesan string menjadi representasi biner."""
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    return binary_message

def binary_to_message(binary_str):
    """Mengonversi representasi biner kembali menjadi string."""
    message = ""
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i+8]
        if len(byte) < 8:
            break # Mengabaikan bit sisa yang tidak membentuk byte penuh
        message += chr(int(byte, 2))
    return message

def calculate_capacity(image):
    """Menghitung total kapasitas penyisipan (dalam bit) dari sebuah gambar."""
    pixels = list(image.getdata())
    width, height = image.size
    capacity = 0
    
    for c in range(3): # Iterasi melalui kanal R, G, B
        for i in range(0, len(pixels) - 1, 2):
            p1_val = pixels[i][c]
            p2_val = pixels[i+1][c]

            diff = p2_val - p1_val
            range_info = get_range_for_diff(diff)
            
            if range_info:
                # Simulasi penyisipan untuk memeriksa masalah batas
                # Kita hanya perlu memeriksa kasus ekstrim (b = 0 dan b = 2^t - 1)
                # Namun untuk kesederhanaan, kita asumsikan kapasitas tersedia jika rentang ditemukan
                # dan pemeriksaan batas akan dilakukan saat penyisipan aktual.
                # Logika yang lebih ketat akan memeriksa apakah modifikasi akan keluar batas.
                # capacity += range_info
                capacity += range_info[2]
                
    return capacity

def embed(image, message):
    """Menyisipkan pesan ke dalam gambar menggunakan PVD."""
    binary_message = message_to_binary(message)
    binary_message += "00000000" # Menambahkan terminator null
    
    # Pengecekan kapasitas
    max_capacity = calculate_capacity(image)
    if len(binary_message) > max_capacity:
        raise ValueError("Pesan terlalu besar untuk disisipkan ke dalam gambar ini.")

    pixels = list(image.getdata())
    width, height = image.size
    
    new_pixels = [list(p) for p in pixels]
    
    data_index = 0
    message_len = len(binary_message)
    
    # Iterasi melalui setiap kanal warna (R, G, B)
    for c in range(3):
        if data_index >= message_len:
            break
        # Iterasi melalui pasangan piksel
        for i in range(0, len(pixels) - 1, 2):
            if data_index >= message_len:
                break

            p1_val = pixels[i][c]
            p2_val = pixels[i+1][c]

            diff = p2_val - p1_val
            range_info = get_range_for_diff(diff)

            if range_info:
                lower, upper, t = range_info
                
                if data_index + t > message_len:
                    continue # Tidak cukup bit tersisa untuk blok ini

                b_str = binary_message[data_index : data_index + t]
                b = int(b_str, 2)

                new_diff = lower + b if diff >= 0 else -(lower + b)
                
                m = new_diff - diff
                m1 = m // 2
                m2 = m - m1

                new_p1_val = p1_val - m1
                new_p2_val = p2_val + m2

                # Pemeriksaan batas (Graceful Degradation)
                if 0 <= new_p1_val <= 255 and 0 <= new_p2_val <= 255:
                    new_pixels[i][c] = new_p1_val
                    new_pixels[i+1][c] = new_p2_val
                    data_index += t

    stego_image = Image.new(image.mode, image.size)
    stego_image.putdata([tuple(p) for p in new_pixels])
    return stego_image

def extract(stego_image):
    """Mengekstrak pesan dari citra stego."""
    pixels = list(stego_image.getdata())
    binary_message = ""

    for c in range(3): # Iterasi melalui kanal R, G, B
        for i in range(0, len(pixels) - 1, 2):
            p1_val = pixels[i][c]
            p2_val = pixels[i+1][c]

            diff = p2_val - p1_val
            range_info = get_range_for_diff(diff)

            if range_info:
                lower, upper, t = range_info
                
                b = abs(diff) - lower
                binary_chunk = format(b, f'0{t}b')
                binary_message += binary_chunk
    
    # Cari terminator null
    null_terminator_index = binary_message.find("00000000")
    if null_terminator_index!= -1:
        binary_message = binary_message[:null_terminator_index]

    return binary_to_message(binary_message)