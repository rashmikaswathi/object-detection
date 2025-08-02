import os

def remove_corrupt_images(images_dir, labels_dir, corrupt_images):
    for img_name in corrupt_images:
        img_path = os.path.join(images_dir, img_name)
        label_name = os.path.splitext(img_name)[0] + '.txt'
        label_path = os.path.join(labels_dir, label_name)

        # Remove image
        if os.path.exists(img_path):
            os.remove(img_path)
            print(f"Deleted corrupt image: {img_name}")
        else:
            print(f"Image not found (already removed?): {img_name}")

        # Remove corresponding label
        if os.path.exists(label_path):
            os.remove(label_path)
            print(f"Deleted label for corrupt image: {label_name}")
        else:
            print(f"Label not found (already removed?): {label_name}")

if __name__ == "__main__":
    images_path = r"C:\Users\samba\Downloads\object_detection-cvvqj-3\train\images"
    labels_path = r"C:\Users\samba\Downloads\object_detection-cvvqj-3\train\labels"

    corrupt_imgs = [
        "ideal-prime-leak-proof-stainless-steel-insulated-lunch-box-with-small-veggie-box-900-ml-elegant-steel-thermoware-tiffin-box-for-office-school-kids-pack-of-1-product-images-orvku24a5xo-p605388448-6-202310021553_jpg.rf.2d6ab04c27f77c0ce84cbfd4c3233a23.jpg",
        "kartunbox-lunch-box-rectangular-shape-stainless-steel-hot-insulated-lunch-tiffin-box-container-with-transparent-lid-710-ml-random-color-product-images-orv5deeh67v-p595451106-3-202211221509_jpg.rf.7a24b5895c8c47cc826166d4def77df2.jpg"
    ]

    remove_corrupt_images(images_path, labels_path, corrupt_imgs)
