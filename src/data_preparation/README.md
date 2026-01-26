# Скрипты подготовки данных

## associate.py

Создает ассоциации между RGB и Depth изображениями на основе временных меток.

**Использование:**
```bash
python associate.py rgb.txt depth.txt > associations.txt
```

**Параметры:**
- `--offset` — временной сдвиг между RGB и Depth
- `--max_difference` — максимальная разница во времени (по умолчанию 0.02 сек)

## iphone_converter.py

Конвертирует экспорт Stray Scanner в TUM RGB-D формат.

**Использование:**
```bash
python iphone_converter.py \
  --input /path/to/stray_scanner_export \
  --output ./iphone_tum_dataset
```

**Входные данные:**
- `rgb.mp4` — видео поток
- `depth/` — папка с depth картами (256×192)
- `odometry.csv` — ARKit траектория

**Выходные данные:**
- `rgb/` — PNG кадры (1920×1440)
- `depth/` — масштабированные depth карты (1920×1440)
- `rgb.txt`, `depth.txt`, `associations.txt`
- `groundtruth.txt` — траектория в TUM формате
