# download_kaggle_dataset.py
import os
import zipfile
import urllib.request
from pathlib import Path
import random

# Direct stable link to a curated open plant disease sample package
DATASET_URL = "https://github.com/classify-org/plant-datasets/raw/main/regional_crops_samples.zip"
ZIP_NAME = "crop_data.zip"

def download_and_extract():
    print("📥 Downloading crop disease dataset package...")
    try:
        req = urllib.request.Request(DATASET_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(ZIP_NAME, 'wb') as f:
            f.write(response.read())
        print("   [OK] Download complete.")
        
        print("📦 Extracting and structuring dataset folders...")
        with zipfile.ZipFile(ZIP_NAME, 'r') as zip_ref:
            zip_ref.extractall("extracted_data")
            
        if os.path.exists(ZIP_NAME):
            os.remove(ZIP_NAME)
            
        print("✅ Dataset successfully ready in workspace!")
    except Exception as e:
        print(f"   ⚠️ Error during download: {e}")

if __name__ == "__main__":
    download_and_extract()