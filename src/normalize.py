import cv2
import os

def count_images_in_folders(root, folders):
    """
    Counts the number of images in each folder and prints the totals.

    Parameters:
    root (str): Root directory containing the folders.
    folders (list): List of folder names to count images in.

    Returns:
    int: Total number of images across all folders.
    """
    total_images = 0
    for folder in folders:
        path = os.path.join(root, folder)
        folder_image_count = len(os.listdir(path))
        print(f'{folder}: {folder_image_count} images')
        total_images += folder_image_count
    print(f'Total: {total_images} images')
    return total_images

def normalize_images(root, folders, size=(48, 48)):
    """
    Normalizes images in the specified folders to a given size and saves them.

    Parameters:
    root (str): Root directory containing the folders.
    folders (list): List of folder names containing images to normalize.
    size (tuple): Desired size for the normalized images.

    Returns:
    None
    """
    for folder in folders:
        path = os.path.join(root, folder)
        for img_name in os.listdir(path):
            img_path = os.path.join(path, img_name)
            img = cv2.imread(img_path, 0)
            if img is None:
                print(f"Warning: Failed to read image {img_path}")
                continue
            img = cv2.resize(img, size)
            cv2.imwrite(img_path, img)
        print(f'Normalized {folder} images')

if __name__ == "__main__":
    try:
        root = 'characters-48x48'
        folders = ['bold', 'boldNitalic', 'italic', 'normal']
        
        # Count and print the number of images in each folder and the total
        count_images_in_folders(root, folders)
        
        # Normalize images in each folder
        normalize_images(root, folders)

    except Exception as e:
        print(f"Error: {e}")
