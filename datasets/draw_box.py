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

    # 计算字体厚度
    # tf = 1
    # label = 'test'
    # # 计算文本的宽度和高度
    # w_text, h_text = cv2.getTextSize(label, 0, fontScale=thickness / 3, thickness=tf)[0]
    #
    # # 找到长边的两个顶点
    # dists = [np.linalg.norm(rotated_pts[i] - rotated_pts[(i + 1) % 4]) for i in range(4)]
    # max_idx = np.argmax(dists)
    # pt1 = rotated_pts[max_idx]
    # pt2 = rotated_pts[(max_idx + 1) % 4]
    #
    # # 确定标签的位置（在长边的上方）
    # midpoint = (pt1 + pt2) / 2
    # angle_perpendicular = math.atan2(pt2[1] - pt1[1], pt2[0] - pt1[0]) + math.pi / 2
    #
    # # 计算标签背景的位置
    # rect_pts = np.array([[-w_text / 2, -h_text / 2],
    #                      [w_text / 2, -h_text / 2],
    #                      [w_text / 2, h_text / 2],
    #                      [-w_text / 2, h_text / 2]])
    # label_rotated_pts = np.dot(rect_pts, R) + np.array(midpoint)
    # label_rotated_pts = label_rotated_pts.astype(int)
    #
    # # 绘制标签背景
    # cv2.polylines(img, [label_rotated_pts], isClosed=True, color=color, thickness=tf, lineType=cv2.LINE_AA)
    #
    # # 计算标签文本的位置
    # label_pos = (int(midpoint[0] - w_text / 2), int(midpoint[1] + h_text / 2))
    #
    # # 绘制标签文本
    # cv2.putText(img, label, label_pos, 0, thickness / 3, (255,255,255), thickness=tf, lineType=cv2.LINE_AA)


image_path = r'E:\yolov9\yolov9\data\P0002__1__1533___824.png'
image = cv2.imread(image_path)
if image is None:
    raise ValueError(f"Failed to load the image file {image_path}. Please check the file path and file integrity.")

with open(r'E:\yolov9\yolov9\data\P0002__1__1533___824.txt', 'r') as file:
    lines = file.readlines()

#
for line in lines:
    parts = line.strip().split()
    cls = int(parts[0])
    cx = float(parts[1]) * image.shape[1]
    cy = float(parts[2]) * image.shape[0]
    w = float(parts[3]) * image.shape[1]
    h = float(parts[4]) * image.shape[0]
    angle = -float(parts[5])
    draw_rotated_box(image, cx, cy, w, h, angle, color=(0, 255, 0), thickness=2)# angle修改回来！！


# # Save the result image to a file
cv2.imwrite('result_test.jpg', image)

# orig = np.array([[1,2,3,4],[5,6,7,8]])
# boxes = orig[:,1:].T
# print(boxes[[0,2]])
# print(boxes[0])

# rect_pts = np.array([[1,2],[3, 4],
#                          [5,6],
#                          [7, 8]])
# print(np.sum(rect_pts,axis=1))
