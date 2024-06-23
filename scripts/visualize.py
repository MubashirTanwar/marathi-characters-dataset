import csv
import random
import cv2
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

# Path to the CSV file and custom font
csv_file = 'data.csv'
font_path = r'Noto_Sans_Devanagari\NotoSansDevanagari-VariableFont_wdth,wght.ttf'  # Replace with the path to your downloaded font file

# Load the custom font
font_prop = FontProperties(fname=font_path, size=14)

# Read CSV file
with open(csv_file, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    data = list(reader)

# Remove header
data = data[1:]

# Function to display 9 random images with labels
def display_random_images(data, num_images=9):
    fig, axs = plt.subplots(3, 3, figsize=(10, 10))
    for i in range(num_images):
        img_path, label = random.choice(data)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        ax = axs[i // 3, i % 3]
        ax.imshow(img, cmap='gray')
        ax.axis('off')
        ax.set_title(label, fontproperties=font_prop)
    plt.tight_layout()
    plt.show()

# Display 9 random images
display_random_images(data)
