import math
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

"""
TO DO:
-(DONE)how to size a pdf to 8.5x11
-(DONE)get images to fit on pdf
-(DONE)change background to white
-(DONE W PROBLEM IN OFFSET BRANCH)change image location to offset grid
-pulling links from a csv
-pulling images from a link
-rewriting image paths to accept this
-parse csv into 28 link blocks to create multiple pages
-test with less than 28 links

Current state: 
"""

def crop_to_circle(image, target_size):
    channels = 4
    height, width, channels = image.shape

    image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)

    center_x, center_y = width // 2, height // 2
    radius = min(width, height) // 2
    
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    cv2.circle(mask, (center_x, center_y), radius, 255, -1)

    cropped_image = cv2.bitwise_and(image, image, mask=mask)
   
    side_length = min(cropped_image.shape[:2])
    start_x = (cropped_image.shape[1] - side_length) // 2
    start_y = (cropped_image.shape[0] - side_length) // 2
    cropped_image = cropped_image[start_y:start_y + side_length, start_x:start_x + side_length]

    resized_image = cv2.resize(cropped_image, target_size, interpolation=cv2.INTER_AREA)

    return resized_image

def arrange_grid(images, ph, pw, img_width, img_height, pic_rows, pic_cols, border, spacing_vert, spacing_hor):
    channels = 4
    grid = np.zeros((ph, pw, channels), dtype=np.uint8)

    for row in range(pic_rows):
        for col in range(pic_cols):
            index = row * pic_cols + col
            if index < len(images):
                grid[(row * img_height)+(row*spacing_vert)+border:(row + 1) * img_height + (row*spacing_vert)+border, (col * img_width)+(col*spacing_hor)+border:(col + 1) * img_width+(col*spacing_hor)+border] = images[index]
                #cv2.imwrite("test.png", grid)
    return grid

def create_pdf(grid, output_path, pw_inch, ph_inch):
    
    temp_image_path = "temp.png" 
    cv2.imwrite(temp_image_path, grid)
    
    pagesize = [pw_inch*inch,ph_inch*inch]
    pdf = canvas.Canvas(output_path, pagesize = pagesize)
    pdf.drawImage(temp_image_path, 0, 0, width=pagesize[0], height=pagesize[1], mask = "auto")
    pdf.save()



def main():
    pic_rows = 6
    pic_cols = 4
    
    ppi = 300
    pw_inch = 8.5
    ph_inch = 11
    diameter_inch = 1.7233
    border_inch = 0.1333
    spacing_vert_inch= 0.0787 #spacing set to evenly space 4x6 grid
    spacing_hor_inch= 0.4467
    pw = int(pw_inch*ppi)
    ph = int(ph_inch*ppi)
    diameter= int(diameter_inch*ppi)
    border= int(border_inch*ppi)
    spacing_vert= int(spacing_vert_inch*ppi)
    spacing_hor= int(spacing_hor_inch*ppi)

    target_size = (diameter, diameter)
    
    image_directory = r"c:\Users\papay\OneDrive\Desktop\Pictures\AlbumCovers"
    image_filenames = os.listdir(image_directory)
    image_paths = [os.path.join(image_directory,image_filename) for image_filename in image_filenames]

    images = [cv2.imread(path) for path in image_paths]
    cropped_images = [crop_to_circle(image, target_size) for image in images]
    grid = arrange_grid(cropped_images, ph, pw, target_size[0], target_size[1], pic_rows, pic_cols, border, spacing_vert, spacing_hor)

    create_pdf(grid, r"c:\Users\papay\OneDrive\Desktop\Pictures\output.pdf", pw_inch, ph_inch)

if __name__ == "__main__":
    main()