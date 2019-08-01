"""
Takes a folder path given in the command line.
Remove the background from all JPEG files in the folder and sub-folders.
Source: https://stackoverflow.com/questions/29313667/how-do-i-remove-the-background-from-this-kind-of-image
"""

import os, sys, cv2
import numpy as np

def main(argv):
    input_dir = check_input_dir(argv)
    output_dir = make_output_dir(input_dir)
    get_images(input_dir, output_dir)


def check_input_dir(argv):
    """
    Takes an argument and checks if it's a folder that exists.
    """
    if len(argv) == 1:
        raise ValueError("Must provide a folder!")
    elif len(argv) > 2:
        raise ValueError("Only one folder allowed!")
    elif not os.path.exists(argv[1]):
        raise ValueError("Image folder does not exist: " + argv[1])
    else:
        print("Status: Input folder confirmed")
    return argv[1]


def make_output_dir(dir_path):
    """
    Create output folder.
    """
    # Get parent folder
    parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir))
    # Get name of new folder
    output_name = os.path.basename(os.path.normpath(dir_path)) + ' output'
    output_folder = parent_dir + '/' + output_name
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    return output_folder


def get_images(input_dir, output_dir):
    """
    Takes a folder path and gets all JPEG images.
    For each image, remove background and save new file in output folder.
    Calls:
        remove_background()
    """
    i = 0
    for sub_dir, dirs, files in os.walk(input_dir):
        for file in files:
            f = os.path.join(sub_dir, file)
            out_f = os.path.join(output_dir, file)
            if f.endswith(".jpg"):
                i += 1
                remove_background(f, out_f)
    if i == 0:
        print('No JPEG files found!')


def remove_background(filepath, savepath):
    # Parameters
    BLUR = 21
    CANNY_THRESH_1 = 10
    CANNY_THRESH_2 = 200
    MASK_DILATE_ITER = 10
    MASK_ERODE_ITER = 10
    MASK_COLOR = (0.0,0.0,1.0) # In BGR format

    # Read image
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Edge detection
    edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
    edges = cv2.dilate(edges, None)
    edges = cv2.erode(edges, None)

    # Find contours in edges, sort by area
    contour_info = []
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    for c in contours:
        contour_info.append((
            c,
            cv2.isContourConvex(c),
            cv2.contourArea(c),
        ))
    contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
    max_contour = contour_info[0]

    # Create empty mask
    # Draw filled polygon on it corresponding to largest contour
    # Mask is black, polygon is white
    mask = np.zeros(edges.shape)
    cv2.fillConvexPoly(mask, max_contour[0], (255))

    # Smooth mask, then blur it
    mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
    mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
    mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
    mask_stack = np.dstack([mask]*3)    # Create 3-channel alpha mask

    # Blend masked img into MASK_COLOR background
    # Use float matrics, for easy blending
    mask_stack  = mask_stack.astype('float32') / 255.0
    img         = img.astype('float32') / 255.0

    # Blend
    masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR)

    # Convert back to 8-bit
    masked = (masked * 255).astype('uint8')

    # Save
    cv2.imwrite(savepath, masked)


if __name__ == '__main__':
    main(sys.argv)