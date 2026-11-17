# download_samples.py
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

CLASSES = [
    "Paddy_Bacterial_Blight",
    "Brinjal_Little_Leaf",
    "Groundnut_Tikka_Spot",
    "Sugarcane_Red_Rot",
    "Mango_Anthracnose"
]

def generate_placeholder_images():
    for class_name in CLASSES:
        train_dir = Path(f"dataset/train/{class_name}")
        val_dir = Path(f"dataset/val/{class_name}")
        
        train_dir.mkdir(parents=True, exist_ok=True)
        val_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🎨 Generating samples for {class_name}...")
        
        # Create 4 training images and 2 validation images per class
        for i in range(4):
            img = Image.new("RGB", (224, 224), color=(34, 139, 34)) # Leaf green background
            draw = ImageDraw.Draw(img)
            # Draw random mock disease spots (brownish circles)
            draw.ellipse([50 + i*15, 60, 90 + i*15, 100], fill=(139, 69, 19))
            draw.ellipse([120, 100 + i*10, 150, 130 + i*10], fill=(105, 53, 15))
            
            img.save(train_dir / f"train_sample_{i+1}.jpg")
            
        for i in range(2):
            img = Image.new("RGB", (224, 224), color=(34, 139, 34))
            draw = ImageDraw.Draw(img)
            draw.ellipse([70, 70, 110, 110], fill=(139, 69, 19))
            
            img.save(val_dir / f"val_sample_{i+1}.jpg")

    print("\n✅ All crop folders successfully populated with images!")

if __name__ == "__main__":
    generate_placeholder_images()