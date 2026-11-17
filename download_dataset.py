import os
import zipfile
import urllib.request
from pathlib import Path
import random

DATASET_URL = "https://github.com/classify-org/plant-datasets/raw/main/regional_crops_samples.zip"
ZIP_NAME = "crop_data.zip"

def download_and_organize():
    print("📥 Downloading crop image dataset...")
    try:
        req = urllib.request.Request(DATASET_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response, open(ZIP_NAME, "wb") as f:
            f.write(response.read())
        print("   [OK] Download complete.")
        
        print("📦 Extracting and structuring folders...")
        with zipfile.ZipFile(ZIP_NAME, "r") as zip_ref:
            zip_ref.extractall("temp_extracted")
            
        if os.path.exists(ZIP_NAME):
            os.remove(ZIP_NAME)
            
        for root, dirs, files in os.walk("temp_extracted"):
            for dirname in dirs:
                class_path = Path(root) / dirname
                images = [img for img in os.listdir(class_path) if img.lower().endswith((".jpg", ".jpeg", ".png"))]
                
                if len(images) > 0:
                    train_dest = Path(f"dataset/train/{dirname}")
                    val_dest = Path(f"dataset/val/{dirname}")
                    train_dest.mkdir(parents=True, exist_ok=True)
                    val_dest.mkdir(parents=True, exist_ok=True)
                    
                    random.shuffle(images)
                    split_idx = int(len(images) * 0.8)
                    
                    for img in images[:split_idx]:
                        os.rename(class_path / img, train_dest / img)
                    for img in images[split_idx:]:
                        os.rename(class_path / img, val_dest / img)

        import shutil
        if os.path.exists("temp_extracted"):
            shutil.rmtree("temp_extracted")
            
        print("✅ Dataset successfully downloaded and sorted!")
    except Exception as e:
        print(f"   ⚠️ Download error: {e}")

if __name__ == "__main__":
    download_and_organize()
