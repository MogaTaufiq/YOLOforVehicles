import torch
from ultralytics import YOLO
from PIL import Image
import os

cuda_available = torch.cuda.is_available()
print(f"CUDA tersedia: {cuda_available}")

if cuda_available:
    device_to_use = 'cuda'
    try:
        print(f"Nama GPU: {torch.cuda.get_device_name(0)}")
    except Exception as e:
        print(f"Tidak dapat mengambil nama GPU: {e}")
else:
    device_to_use = 'cpu'
    print("Menggunakan CPU.")

print(f"Device yang digunakan: {device_to_use}")


model = YOLO('yolov8m.pt')

dataset_config = './vehicle.yaml'

print("Memulai training...")
model.train(
    data=dataset_config,
    epochs=50,
    imgsz=640,
    batch=16,
    device=device_to_use
)
print("Training selesai.")

print("Memulai validasi...")
model.val(device=device_to_use)
print("Validasi selesai.")

trained_model_path = 'runs/train/exp/weights/best.pt'
if not os.path.exists(trained_model_path):
    print(f"Error: Model tidak ditemukan di {trained_model_path}")
else:
    print(f"Memuat model dari: {trained_model_path}")
    model = YOLO(trained_model_path)

    test_image_path = 'path/to/test/image.jpg'
    if not os.path.exists(test_image_path):
         print(f"Error: Gambar uji tidak ditemukan di {test_image_path}")
    else:
        img = Image.open(test_image_path)

        print(f"Melakukan deteksi pada {test_image_path} menggunakan device: {device_to_use}")
        results = model(img, device=device_to_use)
        print("Deteksi selesai.")

        print("Menampilkan hasil deteksi...")
        results[0].show()

print("Program selesai.")