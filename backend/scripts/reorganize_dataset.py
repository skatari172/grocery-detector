import os
import shutil
import glob

def reorganize_dataset():
    """
    Reorganize dataset from class-based subdirectories to flat structure for YOLOv5
    """
    base_dir = "datasets/grocery"
    
    # Create flat directories
    os.makedirs(f"{base_dir}/images_flat/train", exist_ok=True)
    os.makedirs(f"{base_dir}/images_flat/val", exist_ok=True)
    os.makedirs(f"{base_dir}/labels_flat/train", exist_ok=True)
    os.makedirs(f"{base_dir}/labels_flat/val", exist_ok=True)
    
    # Process training data
    print("🔄 Reorganizing training data...")
    train_images = glob.glob(f"{base_dir}/images/train/**/*.png", recursive=True)
    train_images.extend(glob.glob(f"{base_dir}/images/train/**/*.jpg", recursive=True))
    train_images.extend(glob.glob(f"{base_dir}/images/train/**/*.jpeg", recursive=True))
    
    for img_path in train_images:
        img_name = os.path.basename(img_path)
        dest_path = f"{base_dir}/images_flat/train/{img_name}"
        shutil.copy2(img_path, dest_path)
    
    # Copy training labels
    train_labels = glob.glob(f"{base_dir}/labels/train/*.txt")
    for label_path in train_labels:
        label_name = os.path.basename(label_path)
        dest_path = f"{base_dir}/labels_flat/train/{label_name}"
        shutil.copy2(label_path, dest_path)
    
    # Process validation data
    print("🔄 Reorganizing validation data...")
    val_images = glob.glob(f"{base_dir}/images/val/**/*.png", recursive=True)
    val_images.extend(glob.glob(f"{base_dir}/images/val/**/*.jpg", recursive=True))
    val_images.extend(glob.glob(f"{base_dir}/images/val/**/*.jpeg", recursive=True))
    
    for img_path in val_images:
        img_name = os.path.basename(img_path)
        dest_path = f"{base_dir}/images_flat/val/{img_name}"
        shutil.copy2(img_path, dest_path)
    
    # Copy validation labels
    val_labels = glob.glob(f"{base_dir}/labels/val/*.txt")
    for label_path in val_labels:
        label_name = os.path.basename(label_path)
        dest_path = f"{base_dir}/labels_flat/val/{label_name}"
        shutil.copy2(label_path, dest_path)
    
    print(f"✅ Training images: {len(train_images)}")
    print(f"✅ Training labels: {len(train_labels)}")
    print(f"✅ Validation images: {len(val_images)}")
    print(f"✅ Validation labels: {len(val_labels)}")
    print("🎉 Dataset reorganization complete!")

if __name__ == "__main__":
    reorganize_dataset() 