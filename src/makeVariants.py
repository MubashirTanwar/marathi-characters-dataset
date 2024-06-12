import cv2
import os

def create_variant_folders(root, sub_folder, folders, new_folders):
    """
    Creates new folders for image variants.

    Parameters:
    root (str): Root directory containing the sub-folder.
    sub_folder (str): Sub-folder containing the original folders.
    folders (list): List of original folder names.
    new_folders (list): List of new variant folder names to create.

    Returns:
    None
    """
    for new_folder in new_folders:
        for folder in folders:
            path = os.path.join(root, sub_folder, new_folder, folder)
            os.makedirs(path, exist_ok=True)
            print(f'Created {new_folder}/{folder} folder')

def shift_and_save_images(root, sub_folder, folders, new_folders):
    """
    Shifts images by 8 pixels in specified directions and saves them in new folders.

    Parameters:
    root (str): Root directory containing the sub-folder.
    sub_folder (str): Sub-folder containing the original folders.
    folders (list): List of original folder names.
    new_folders (list): List of new variant folder names.

    Returns:
    None
    """
    shift_amount = 8
    for folder in folders:
        for new_folder in new_folders:
            path = os.path.join(root, sub_folder, new_folder, folder)
            for img_name in os.listdir(os.path.join(root, sub_folder, folder)):
                img_path = os.path.join(root, sub_folder, folder, img_name)
                img = cv2.imread(img_path, 0)
                if img is None:
                    print(f"Warning: Failed to read image {img_path}")
                    continue
                if new_folder == 'left':
                    shifted_img = img[:, shift_amount:]
                elif new_folder == 'right':
                    shifted_img = img[:, :-shift_amount]
                elif new_folder == 'up':
                    shifted_img = img[shift_amount:, :]
                elif new_folder == 'down':
                    shifted_img = img[:-shift_amount, :]
                cv2.imwrite(os.path.join(path, img_name), shifted_img)
            print(f'Shifted {new_folder}/{folder} images')

if __name__ == "__main__":
    try:
        root = 'characters-48x48'
        sub_folder = 'classic'
        folders = ['bold', 'boldNitalic', 'italic', 'normal']
        
        # Variants to create
        new_folders = ['left', 'right', 'up', 'down']
        # Optionally include diagonal shifts
        # new_folders += ['up-left', 'up-right', 'down-left', 'down-right']

        # Create the necessary folders for variants
        create_variant_folders(root, sub_folder, folders, new_folders)

        # Shift images and save them in the new folders
        shift_and_save_images(root, sub_folder, folders, new_folders)

    except Exception as e:
        print(f"Error: {e}")
