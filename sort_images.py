# sort_images.py
import os
import shutil
from pathlib import Path

def organize_folder(crop_name: str, raw_source_dir: str):
    """
    Takes raw images from a source folder and splits them 
    automatically into dataset/train/ and dataset/val/
    """
    source_path = Path(raw_source_dir)
    if not source_path.exists():
        print(f"⚠️ Source folder '{raw_source_dir}' not found. Skipping.")
        return

    # Find all images
    images = sorted(list(source_path.glob("*.jpg")) + list(source_path.glob("*.JPG")) + list(source_path.glob("*.png")))
    
    if not images:
        print(f"⚠️ No images found inside '{raw_source_dir}'.")
        return

    # 80% train, 20% validation split
    split_index = int(len(images) * 0.8)
    train_imgs = images[:split_index]
    val_imgs = images[split_index:]

    # Destination directories
    train_dest = Path(f"dataset/train/{crop_name}")
    val_dest = Path(f"dataset/val/{crop_name}")
    train_dest.mkdir(parents=True, exist_ok=True)
    val_dest.mkdir(parents=True, exist_ok=True)

    # Copy files
    for img in train_imgs:
        shutil.copy(img, train_dest / img.name)
    for img in val_imgs:
        shutil.copy(img, val_dest / img.name)

    print(f"✅ Successfully sorted {crop_name}: {len(train_imgs)} train images, {len(val_imgs)} val images added.")

if __name__ == "__main__":
    # Example mapping: Map your raw download folders to your official dataset classes
    mapping = {
        "Paddy_Bacterial_Blight": "raw_downloads/paddy_blight",
        "Brinjal_Little_Leaf": "raw_downloads/brinjal_leaf",
        "Groundnut_Tikka_Spot": "raw_downloads/groundnut_spot",
        "Sugarcane_Red_Rot": "raw_downloads/sugarcane_rot",
        "Mango_Anthracnose": "raw_downloads/mango_spot"
    }

    for crop_class, raw_folder in mapping.items():
        organize_folder(crop_class, raw_folder)