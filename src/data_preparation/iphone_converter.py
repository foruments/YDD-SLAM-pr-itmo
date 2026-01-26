import os
import cv2
import numpy as np
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askdirectory

Tk().withdraw()

print("Выберите корневую папку датасета из Stray Scanner...")
dataset_folder = askdirectory(title="Выберите корневую папку датасета")

if not dataset_folder:
    print("Папка не выбрана. Выход.")
    exit()

print(f"Выбрана папка: {dataset_folder}")

depth_folder = os.path.join(dataset_folder, "depth")
rgb_video = os.path.join(dataset_folder, "rgb.mp4")

# Выходная папка
output_dir = os.path.join(dataset_folder, "tum_dataset")
rgb_dir = os.path.join(output_dir, "rgb")
depth_dir = os.path.join(output_dir, "depth")

os.makedirs(rgb_dir, exist_ok=True)
os.makedirs(depth_dir, exist_ok=True)

print(f"Создаю TUM-датасет в: {output_dir}")

camera_matrix_path = None
for file in os.listdir(dataset_folder):
    if file.startswith("camera_matrix") and file.endswith(".csv"):
        camera_matrix_path = os.path.join(dataset_folder, file)
        break

if not camera_matrix_path:
    print("Ошибка: camera_matrix.csv не найден")
    exit()

print(f"Найден файл калибровки: {camera_matrix_path}")

with open(camera_matrix_path, "r") as f:
    lines = f.readlines()

matrix = []
for line in lines:
    if line.strip() and not line.startswith('#'):
        row = [float(x.replace(',', '')) for x in line.strip().split(',') if x.strip()]
        if row:
            matrix.append(row)

if len(matrix) != 3 or len(matrix[0]) != 3:
    print("Ошибка: неверный формат camera_matrix")
    exit()

fx = matrix[0][0]
fy = matrix[1][1]
cx = matrix[0][2]
cy = matrix[1][2]

example_depth = os.path.join(depth_folder, sorted(os.listdir(depth_folder))[0])
img_depth = Image.open(example_depth)
width, height = img_depth.size

print("\n=== Калибровочные параметры камеры ===")
print(f"Width: {width}")
print(f"Height: {height}")
print(f"fx: {fx:.6f}")
print(f"fy: {fy:.6f}")
print(f"cx: {cx:.6f}")
print(f"cy: {cy:.6f}")

print("Извлекаю RGB кадры из rgb.mp4 с помощью OpenCV...")
cap = cv2.VideoCapture(rgb_video)
if not cap.isOpened():
    print("Ошибка: не могу открыть rgb.mp4")
    exit()

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(frame_rgb)
    img.save(os.path.join(rgb_dir, f"{frame_count:06d}.png"))
    frame_count += 1

cap.release()
print(f"Извлечено {frame_count} RGB кадров")

rgb_files = sorted([f for f in os.listdir(rgb_dir) if f.lower().endswith('.png')])
depth_files = sorted([f for f in os.listdir(depth_folder) if f.lower().endswith('.png')])

min_frames = min(len(rgb_files), len(depth_files))
print(f"Обрабатываю {min_frames} кадров...")

rgb_txt = []
depth_txt = []
associations = []

for i in range(min_frames):
    rgb_file = rgb_files[i]
    depth_file = depth_files[i]

    timestamp = i * 0.033333  # 30 FPS

    rgb_src = os.path.join(rgb_dir, rgb_file)
    rgb_dst = os.path.join(rgb_dir, f"{timestamp:.6f}.png")
    os.rename(rgb_src, rgb_dst)

    depth_src = os.path.join(depth_folder, depth_file)
    depth_dst = os.path.join(depth_dir, f"{timestamp:.6f}.png")
    img_depth = Image.open(depth_src)
    img_depth.save(depth_dst)

    rgb_line = f"{timestamp:.6f} rgb/{timestamp:.6f}.png"
    depth_line = f"{timestamp:.6f} depth/{timestamp:.6f}.png"
    assoc_line = f"{timestamp:.6f} rgb/{timestamp:.6f}.png {timestamp:.6f} depth/{timestamp:.6f}.png"

    rgb_txt.append(rgb_line)
    depth_txt.append(depth_line)
    associations.append(assoc_line)

with open(os.path.join(output_dir, "rgb.txt"), "w") as f:
    f.write("# RGB images\n")
    f.write("\n".join(rgb_txt))

with open(os.path.join(output_dir, "depth.txt"), "w") as f:
    f.write("# Depth images\n")
    f.write("\n".join(depth_txt))

with open(os.path.join(output_dir, "associations.txt"), "w") as f:
    f.write("\n".join(associations))

print(f"\nГотово! {len(rgb_txt)} кадров обработано.")
print(f"TUM-датасет создан в: {output_dir}")
