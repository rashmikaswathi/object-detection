import os

def check_dataset(images_dir, labels_dir, image_exts=['.jpg', '.jpeg', '.png']):
    # Get list of image files
    image_files = [f for f in os.listdir(images_dir) if os.path.splitext(f)[1].lower() in image_exts]
    # Get list of label files
    label_files = [f for f in os.listdir(labels_dir) if f.endswith('.txt')]

    # Check for images without labels
    images_without_labels = []
    for img in image_files:
        label_name = os.path.splitext(img)[0] + '.txt'
        if label_name not in label_files:
            images_without_labels.append(img)

    # Check for labels without images
    labels_without_images = []
    for label in label_files:
        image_name_jpg = os.path.splitext(label)[0] + '.jpg'
        image_name_png = os.path.splitext(label)[0] + '.png'
        if image_name_jpg not in image_files and image_name_png not in image_files:
            labels_without_images.append(label)

    # Check for corrupt images by trying to open them with PIL
    from PIL import Image
    corrupt_images = []
    for img in image_files:
        img_path = os.path.join(images_dir, img)
        try:
            with Image.open(img_path) as im:
                im.verify()  # verify does not load image fully but checks integrity
        except Exception as e:
            corrupt_images.append(img)

    # Print results
    if images_without_labels:
        print(f"Images without label files ({len(images_without_labels)}):")
        for f in images_without_labels:
            print(f"  {f}")
    else:
        print("All images have corresponding label files.")

    if labels_without_images:
        print(f"Label files without images ({len(labels_without_images)}):")
        for f in labels_without_images:
            print(f"  {f}")
    else:
        print("All label files have corresponding images.")

    if corrupt_images:
        print(f"Corrupt images detected ({len(corrupt_images)}):")
        for f in corrupt_images:
            print(f"  {f}")
    else:
        print("No corrupt images found.")

if __name__ == "__main__":
    images_path = r"C:\Users\samba\Downloads\object_detection-cvvqj-3\train\images"
    labels_path = r"C:\Users\samba\Downloads\object_detection-cvvqj-3\train\labels"
    check_dataset(images_path, labels_path)
