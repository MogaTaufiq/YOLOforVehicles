from ultralytics import YOLO
from PIL import Image


# Muat model pre-trained YOLOv8
model = YOLO('yolov8m.pt')  # Atau 'yolov8m.pt' atau 'yolov8l.pt' jika kamu ingin model yang lebih besar

# Tentukan path ke file konfigurasi dataset
dataset_config = './vehicle.yaml'  # Gantilah dengan path ke file .yaml yang sudah kamu buat

# Fine-tuning model
model.train(
    data=dataset_config,  # Path ke file .yaml yang berisi konfigurasi dataset
    epochs=50,            # Jumlah epoch pelatihan (kamu bisa sesuaikan)
    imgsz=640,            # Ukuran gambar (misalnya 640x640)
    batch=16,             # Ukuran batch
    device='cpu'             # Gunakan GPU (ganti 'cpu' jika tidak ada GPU)
)

# Evaluasi model
model.val()

# Muat model yang sudah dilatih
model = YOLO('runs/train/exp/weights/best.pt')  # Gantilah dengan path ke model hasil pelatihan

# Muat gambar untuk deteksi
img = Image.open('path/to/test/image.jpg')

# Lakukan deteksi
results = model(img)

# Tampilkan hasil deteksi
results.show()
