import cv2
import numpy as np
import os
import sys

def process_image_for_text_detection(img_path):
    """
    Processes the input image to highlight and extract text regions.

    Parameters:
    img_path (str): Path to the input image file.

    Returns:
    None
    """
    # Read and split the image into RGB planes
    img = cv2.imread(img_path)
    rgb_planes = cv2.split(img)
    result_planes = []
    
    # Enhance the image by removing the background
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.GaussianBlur(dilated_img, (5, 5), 0)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        result_planes.append(diff_img)
    
    img = cv2.merge(result_planes)
    
    # Convert to grayscale and apply thresholding
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Save the processed image
    processed_img_path = 'processed.png'
    cv2.imwrite(processed_img_path, img)
    
    # Draw contours around detected text regions
    draw_text_contours(processed_img_path)

def draw_text_contours(img_path):
    """
    Draws contours around detected text regions in the image and saves the result.

    Parameters:
    img_path (str): Path to the processed image file.

    Returns:
    None
    """
    # Read the processed image
    img = cv2.imread(img_path, 0)
    original_img = img.copy()
    cv2.imwrite(os.path.join(output_dir, 'original.png'), original_img)

    # Apply Gaussian blur and adaptive thresholding
    img = cv2.GaussianBlur(img, (5, 5), 0)
    threshed = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY_INV, 11, 1)

    # Erode and dilate the image to highlight text regions
    kernel = np.ones((2, 2), np.uint8)
    erosion = cv2.erode(threshed, kernel)
    cv2.imwrite(os.path.join(output_dir, 'erosion.png'), erosion)

    kernel = np.ones((2, 10), np.uint8)
    dilated = cv2.dilate(erosion, kernel, iterations=1)
    cv2.imwrite(os.path.join(output_dir, 'dilated.png'), dilated)

    kernel = np.ones((2, 10), np.uint8)
    closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite(os.path.join(output_dir, 'closed.png'), closed)

    # Find contours and filter out empty ones
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cnt for cnt in contours if cnt.size > 0]

    # Sort contours from top to bottom and then left to right
    sorted_contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])
    lines = []
    current_line = []
    current_y = 0
    for cnt in sorted_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if current_line and abs(y - current_y) > 10:
            lines.append(current_line)
            current_line = []
        current_line.append((x, y, w, h))
        current_y = y
    if current_line:
        lines.append(current_line)
    sorted_contours = [sorted(line, key=lambda b: b[0]) for line in lines]
    sorted_contours = [item for sublist in sorted_contours for item in sublist]

    # Draw contours and save individual word images
    img_contours = original_img.copy()
    cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 1)
    cv2.imwrite(os.path.join(output_dir, 'contours.png'), img_contours)

    box_count = 0
    boxes = []
    min_area_threshold = 700  # Minimum area threshold for filtering out small contours
    for i, (x, y, w, h) in enumerate(sorted_contours):
        if w * h > min_area_threshold:
            top_increase_factor = 20
            bottom_increase_factor = 20
            y -= top_increase_factor
            h += (top_increase_factor + bottom_increase_factor)
            if w > h:
                diff = w - h
                y -= diff // 2
                h += diff
            else:
                diff = h - w
                x -= diff // 2
                w += diff
            cv2.rectangle(original_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            word_img = ogimg[y:y + h, x:x + w]
            box_count += 1
            cv2.imwrite(os.path.join(output_dir, f'word_{box_count}.png'), word_img)
            boxes.append((x, y, w, h))

    for box in boxes:
        x, y, w, h = box
    filename = os.path.join(output_dir, 'word_boxes.png')
    cv2.imwrite(filename, original_img)
    print('Saved as', filename)

    return original_img

if __name__ == "__main__":
    try:
        # Ensure correct number of command line arguments
        if len(sys.argv) != 3:
            raise ValueError("Usage: script.py <input_image_path> <output_directory>")
        
        img_path = sys.argv[1]
        output_dir = sys.argv[2]
        
        # Ensure the output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Load and resize the input image
        ogimg = cv2.imread(img_path)
        if ogimg is None:
            raise FileNotFoundError(f"Image not found: {img_path}")
        
        ogimg = cv2.resize(ogimg, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        
        # Process the image to detect and highlight text
        process_image_for_text_detection(img_path)
    
    except Exception as e:
        print(f"Error: {e}")
