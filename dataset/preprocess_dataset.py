import os
import shutil
import random
from pathlib import Path
from tqdm import tqdm

SOURCE_DIR = "../scraping/output"
DEST_DIR = "processed_dataset"
CLASSES = ["cancer", "non_cancer"]
SPLIT_RATIO = 0.8  # 80% train, 20% test


def ensure_dirs():
    for split in ["train", "test"]:
        for cls in CLASSES:
            os.makedirs(os.path.join(DEST_DIR, split, cls), exist_ok=True)


def gather_all_images():
    images = {cls: [] for cls in CLASSES}
    for site_folder in Path(SOURCE_DIR).iterdir():
        for cls in CLASSES:
            cls_path = site_folder / cls.capitalize()
            if cls_path.exists():
                for img_file in cls_path.glob("*.jpg"):
                    images[cls].append(img_file)
    return images


def split_and_copy(images):
    for cls in CLASSES:
        data = images[cls]
        random.shuffle(data)
        split_idx = int(len(data) * SPLIT_RATIO)
        train_set, test_set = data[:split_idx], data[split_idx:]

        for idx, img_path in enumerate(tqdm(train_set, desc=f"Copying {cls} train")):
            dest = Path(DEST_DIR) / "train" / cls / f"{cls}_{idx}.jpg"
            shutil.copy(img_path, dest)

        for idx, img_path in enumerate(tqdm(test_set, desc=f"Copying {cls} test")):
            dest = Path(DEST_DIR) / "test" / cls / f"{cls}_{idx}.jpg"
            shutil.copy(img_path, dest)


if __name__ == "__main__":
    ensure_dirs()
    all_images = gather_all_images()
    split_and_copy(all_images)
    print("✅ Dataset preprocessing complete.")
