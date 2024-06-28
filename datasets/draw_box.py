import cv2
import numpy as np
import math


def draw_rotated_box(img, cx, cy, w, h, angle, color, thickness):
    angle_rad = math.radians(angle)
    R = np.array([[math.cos(angle_rad), -math.sin(angle_rad)],
                  [math.sin(angle_rad), math.cos(angle_rad)]])
    half_w, half_h = w / 2, h / 2
    rect_pts = np.array([[-half_w, -half_h],
                         [half_w, -half_h],
                         [half_w, half_h],
                         [-half_w, half_h]])
    rotated_pts = np.dot(rect_pts, R) + np.array([cx, cy])
    rotated_pts = rotated_pts.astype(int)
    cv2.polylines(img, [rotated_pts], isClosed=True, color=color, thickness=thickness)


image_path = 'E:\\BaiduNetdiskDownload\\train\\images\\images\\P0330.png'
image = cv2.imread(image_path)
if image is None:
    raise ValueError(f"Failed to load the image file {image_path}. Please check the file path and file integrity.")

with open('./train/labelTxt/P0330.txt', 'r') as file:
    lines = file.readlines()

for line in lines:
    parts = line.strip().split()
    cls = int(parts[0])
    cx = float(parts[1]) * image.shape[1]
    cy = float(parts[2]) * image.shape[0]
    w = float(parts[3]) * image.shape[1]
    h = float(parts[4]) * image.shape[0]
    # angle = -float(parts[5])
    draw_rotated_box(image, cx, cy, w, h, 0, color=(0, 255, 0), thickness=2)# angle修改回来！！

# Save the result image to a file
cv2.imwrite('result_test.jpg', image)
