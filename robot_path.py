import cv2
import numpy as np
import sys

# # Function to compute the path to be taken
def find_path(depth):
    # # Loading the Depth Image
    image = np.loadtxt(depth)
    # # Rescaling the depth image to 8 bit range
    image *= 256/image.max()
    # # Thresholding the image values to eliminate noise
    image[image>40] = 255
    # # Converting the Image to 8bit int format
    image = np.array(image, dtype='uint8')
    # # Creating a copy of the image for computations with out any modification
    # # to the depth image
    image_copy = image
    # # Blurring the image with a kernal of 7x7
    image = cv2.GaussianBlur(image,(7,7),0)
    # # Creating a person classifier with the trained xml file
    person_cascade = cv2.CascadeClassifier('cascadG.xml')
    # # Itentifying humans in the image
    rects = person_cascade.detectMultiScale(image, 1.1, 5, 0)
    # # Getting the x,y,w,h for the box around humans
    for (x, y, w, h) in rects:
        count = 0
        avg = 0
        # # Computing the x axis point of the human in the image
        human_depth_coor = int((x+x+w)/2)
        # # Iterating through the height of the human to get the average depth value
        for a in range(y,y+h):
            if image_copy[a][human_depth_coor] > 20 and image_copy[a][human_depth_coor] < 30:
                count += 1
                avg = (avg + image_copy[a][int((x+x+w)/2)])
        human_depth_value = avg/count
        # # Iterating Through the x asis of the image with y as the center point of human
        dist_calc = []
        for b in range(image.shape[1]):
            # # Getting the pixels on the wall and shelve in front and back of the humans
            if image_copy[int((y+y+h)/2)][b] >= (human_depth_value-1) and image_copy[int((y+y+h)/2)][b] <= (human_depth_value+1) and not b in range(x,x+w):
                dist_calc.append(b)
            # # To get the distance between human and wall
            if image_copy[int((y+y+h)/2)][b] == human_depth_value and not b in range(0,x+w):
                wall_pixal = b
        # # To get the length of the coridor in pixal values
        pixel_width_coridor = max(dist_calc)-min(dist_calc)
        distance_human = 2
        actual_width_coridor = 1.5

        # # Computing the focal length
        focal_length = (pixel_width_coridor * distance_human)/actual_width_coridor

        # # Converting the distance between human and wall in pixals
        distance_wall_human_pixal = wall_pixal - human_depth_coor
        # # Converting the distance between human and wall in meters
        distance_wall_human = (distance_wall_human_pixal * distance_human)/focal_length
        # # Thresholding the path as left or right
        if(distance_wall_human > 0.75):
            print'right',distance_wall_human
        else:
            print'left',(1.5-distance_wall_human)
        # # Drawing a box around the human
        cv2.rectangle(image_copy, (x,y), (x+w,y+h),(0,255,0),2)
    # # Displaying the image
    cv2.imshow('image',image_copy)
    cv2.waitKey(0)
"""
Begining of the program
"""
if __name__ == '__main__':

    # # Getting the depth files as arguments
    try:
        path = sys.argv[1]
    except:
        path = raw_input("Give the path to the depth files: ")
    # # Calling the function to compute the path
    find_path(sys.argv[1])
