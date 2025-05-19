import os
import shutil

# --- KONFIGURASI ---
# Path ke folder utama dataset asli (berisi folder 'images' dan 'labels')
dataset_path = 'dataset/valid'

# Path ke folder baru untuk dataset hasil filter
filtered_dataset_path = 'dataset/new/valid'

# *** PENTING: Daftar class_id yang ingin disimpan ***
# Sesuaikan dengan class_id untuk 'car', 'bus', dan 'van' di dataset Anda
# Berdasarkan daftar kelas sebelumnya: car=0, bus=2, van=5
target_class_ids = {0} # Menggunakan set untuk pencarian cepat

# Nama folder gambar dan label
image_folder_name = 'images'
label_folder_name = 'labels'
# --- AKHIR KONFIGURASI ---

original_image_dir = os.path.join(dataset_path, image_folder_name)
original_label_dir = os.path.join(dataset_path, label_folder_name)

filtered_image_dir = os.path.join(filtered_dataset_path, image_folder_name)
filtered_label_dir = os.path.join(filtered_dataset_path, label_folder_name)

os.makedirs(filtered_image_dir, exist_ok=True)
os.makedirs(filtered_label_dir, exist_ok=True)

print(f"Filtering dataset. Target Class IDs: {target_class_ids}")

for image_name in os.listdir(original_image_dir):
    if image_name.lower().endswith(('.jpg', '.jpeg', '.png')):
        base_name, _ = os.path.splitext(image_name)
        label_name = base_name + '.txt'
        original_label_path = os.path.join(original_label_dir, label_name)
        original_image_path = os.path.join(original_image_dir, image_name)

        if not os.path.exists(original_label_path):
            # print(f"Label missing for {image_name}") # Opsional: notifikasi label hilang
            continue

        has_target_object = False
        try:
            with open(original_label_path, 'r') as f:
                for line in f:
                    parts = line.split()
                    if parts:
                        current_class_id = int(parts[0])
                        # Cek apakah class_id saat ini ada di dalam set target_class_ids
                        if current_class_id in target_class_ids:
                            has_target_object = True
                            break # Jika sudah menemukan salah satu target, tidak perlu cek baris lain
        except Exception as e:
            print(f"Error reading label file {label_name}: {e}")
            continue

        if has_target_object:
            filtered_image_path = os.path.join(filtered_image_dir, image_name)
            filtered_label_path = os.path.join(filtered_label_dir, label_name)
            shutil.copy2(original_image_path, filtered_image_path)
            shutil.copy2(original_label_path, filtered_label_path)
            # print(f"Keeping: {image_name}") # Opsional: notifikasi file yang disimpan

print("Filtering complete.")