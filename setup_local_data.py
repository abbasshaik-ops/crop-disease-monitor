import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random

crops = {
    "Paddy_Bacterial_Blight": (34, 139, 34),
    "Brinjal_Little_Leaf": (46, 139, 87),
    "Groundnut_Tikka_Spot": (85, 107, 47),
    "Sugarcane_Red_Rot": (60, 120, 50),
    "Mango_Anthracnose": (40, 100, 40)
}

print("🛠️ Setting up local dataset directories and initial samples...")

for class_name, base_color in crops.items():
    train_dir = Path(f"dataset/train/{class_name}")
    val_dir = Path(f"dataset/val/{class_name}")
    train_dir.mkdir(parents=True, exist_ok=True)
    val_dir.mkdir(parents=True, exist_ok=True)
    
    # Create 10 training images per class
    for i in range(10):
        img = Image.new("RGB", (224, 224), color=base_color)
        draw = ImageDraw.Draw(img)
        for _ in range(5):
            x1 = random.randint(20, 150)
            y1 = random.randint(20, 150)
            draw.ellipse([x1, y1, x1 + 40, y1 + 40], fill=(110, 50, 20))
        img = img.filter(ImageFilter.GaussianBlur(radius=1))
        img.save(train_dir / f"sample_{i+1}.jpg")
        
    # Create 3 validation images per class
    for i in range(3):
        img = Image.new("RGB", (224, 224), color=base_color)
        draw = ImageDraw.Draw(img)
        draw.ellipse([60, 60, 120, 120], fill=(110, 50, 20))
        img.save(val_dir / f"val_{i+1}.jpg")

print("✅ Local dataset folders and samples successfully generated!")
