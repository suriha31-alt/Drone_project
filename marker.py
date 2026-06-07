import cv2
import numpy as np

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

marker = cv2.aruco.generateImageMarker(
    aruco_dict,
    0,
    400
)

# Add a white border around the marker
border_size = 100
marker_with_border = cv2.copyMakeBorder(
    marker,
    border_size,
    border_size,
    border_size,
    border_size,
    cv2.BORDER_CONSTANT,
    value=255
)

cv2.imwrite("landing_pad.jpg", marker_with_border)

print("Marker Created Successfully")