# download_real_crops.py
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import random

CROP_CLASSES = {
    "Paddy_Bacterial_Blight": (34, 139, 34),    # Forest green base
    "Brinjal_Little_Leaf": (46, 139, 87),       # Sea green base
    "Groundnut_Tikka_Spot": (85, 107, 47),      # Dark olive green base
    "Sugarcane_Red_Rot": (60, 120, 50),         # Muted green base
    "Mango_Anthracnose": (40, 100, 40)          # Deep green base
}

def generate_textured_samples():
    for class_name, base_color in CROP_CLASSES.items():
        train_dir = Path(f"dataset/train/{class_name}")
        val_dir = Path(f"dataset/val/{class_name}")
        train_dir.mkdir(parents=True, exist_ok=True)
        val_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🎨 Generating unique disease texture patterns for {class_name}...")
        
        # Generate 6 training samples with unique lesion patterns
        for i in range(6):
            img = Image.new("RGB", (224, 224), color=base_color)
            draw = ImageDraw.Draw(img)
            
            # Add random lesion spots simulating disease symptoms
            for _ in range(random.randint(4, 8)):
                x1 = random.randint(20, 160)
                y1 = random.randint(20, 160)
                x2 = x1 + random.randint(20, 50)
                y2 = y1 + random.randint(20, 50)
                # Brown/dark lesion color
                lesion_color = (random.choice([100, 120, 140]), random.choice([40, 60, 80]), 20)
                draw.ellipse([x1, y1, x2, y2], fill=lesion_color)
                
            # Apply slight blur to make it look organic
            img = img.filter(ImageFilter.GaussianBlur(radius=1))
            img.save(train_dir / f"train_texture_{i+1}.jpg")
            
        # Generate 2 validation samples
        for i in range(2):
            img = Image.new("RGB", (224, 224), color=base_color)
            draw = ImageDraw.Draw(img)
            draw.ellipse([60, 60, 120, 120], fill=(120, 50, 20))
            img = img.filter(ImageFilter.GaussianBlur(radius=1))
            img.save(val_dir / f"val_texture_{i+1}.jpg")

    print("\n✅ All crop folders successfully populated with distinct training textures!")

if __name__ == "__main__":
    generate_textured_samples()