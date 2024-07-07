import os
import cv2
import numpy as np
from PIL import Image
import shutil


class_15 = ['plane', 'baseball-diamond', 'bridge', 'ground-track-field', 'small-vehicle',
            'large-vehicle', 'ship', 'tennis-court','basketball-court', 'storage-tank',
            'soccer-ball-field', 'roundabout', 'harbor', 'swimming-pool', 'helicopter']


def parse_dota_poly(filename):
    objects = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            parts = line.strip().split()
            if len(parts) > 8:
                poly = [(float(parts[0]), float(parts[1])), (float(parts[2]), float(parts[3])),
                        (float(parts[4]), float(parts[5])), (float(parts[6]), float(parts[7]))]
                name = parts[8]
                objects.append({'poly': poly, 'name': name})
    return objects


# 调整范围
def cvminAreaRect2longsideformat(c_x, c_y, w, h, theta):
    if w < h:
        w, h = h, w
        theta += 90
    if theta >= 180:
        theta -= 180
    elif theta < -90:
        theta += 180
    return c_x, c_y, w, h, theta


def draw_poly_and_rect(image, poly, rect):
    # 原来的dota标签对应的多边形框（可能不是矩形）
    poly_points = np.array(poly, np.int32)
    poly_points = poly_points.reshape((-1, 1, 2))
    cv2.polylines(image, [poly_points], isClosed=True, color=(0, 255, 0), thickness=2)

    # 这个是最小外接矩形，也就是转换后的标签画得框
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)
    # cv2.drawContours(image, [box], 0, (255, 0, 0), 2)

    return image


def adjust_bbox(poly, img_w, img_h):
    # 改变点，先调整坐标，在进行归一化处理，效果好于相反顺序
    rect = cv2.minAreaRect(poly)
    c_x, c_y = rect[0]
    w, h = rect[1]
    theta = rect[2]

    c_x, c_y, longside, shortside, theta_longside = cvminAreaRect2longsideformat(c_x, c_y, w, h, theta)

    c_x /= img_w
    c_y /= img_h
    longside /= img_w
    shortside /= img_h

    return c_x, c_y, longside, shortside, theta_longside


def dota2YOLOFormat(imgpath, txtpath, dstpath, extractclassname):
    if os.path.exists(dstpath):
        shutil.rmtree(dstpath)
    os.makedirs(dstpath)
    filelist = [os.path.join(txtpath, f) for f in os.listdir(txtpath) if f.endswith('.txt')]

    for fullname in filelist:
        objects = parse_dota_poly(fullname)
        name = os.path.splitext(os.path.basename(fullname))[0]
        img_fullname = os.path.join(imgpath, name + '.png')

        # 防止检测错误
        if not os.path.exists(img_fullname):
            print(f"Image file {img_fullname} not found, skipping.")
            continue

        img = Image.open(img_fullname)
        img_w, img_h = img.size

        img_cv2 = cv2.imread(img_fullname)

        with open(os.path.join(dstpath, name + '.txt'), 'w') as f_out:
            for obj in objects:
                poly = obj['poly']
                poly = np.float32(np.array(poly))

                c_x, c_y, longside, shortside, theta_longside = adjust_bbox(poly, img_w, img_h)

                if longside <= 0 or shortside <= 0 or c_x < 0 or c_y < 0 or c_x > 1 or c_y > 1:
                    continue

                if obj['name'] in extractclassname:
                    class_id = extractclassname.index(obj['name'])
                else:
                    continue

                theta_label = int(theta_longside + 180.5)
                if theta_label == 180:
                    theta_label = 179

                # outline = f"{class_id} {c_x} {c_y} {longside} {shortside} {theta_label}"
                outline = f"{class_id} {c_x} {c_y} {longside} {shortside}"
                f_out.write(outline + '\n')

    # 注释部分为对原始图像画框并生成debug文件
    #                 img_cv2 = draw_poly_and_rect(img_cv2, poly, cv2.minAreaRect(poly))

    #         debug_img_name = os.path.join(dstpath, name + '_debug.png')
    #         cv2.imwrite(debug_img_name, img_cv2)

    print('DOTA to YOLO format conversion completed')


def delete_invalid_files(imgpath, txtpath):
    filelist = [os.path.join(txtpath, f) for f in os.listdir(txtpath) if f.endswith('.txt')]
    for fullname in filelist:
        name = os.path.splitext(os.path.basename(fullname))[0]
        img_fullname = os.path.join(imgpath, name + '.png')
        if not os.path.exists(img_fullname):
            print(f"Deleting label file {fullname} because image file {img_fullname} does not exist.")
            os.remove(fullname)


if __name__ == '__main__':
    # delete_invalid_files('./val/images', './val/labelTxt')

    dota2YOLOFormat(imgpath='E:\\yolov9\train\labels',
                    txtpath='E:\\BaiduNetdiskDownload\\train\\labelTxt-v1.0\\labelTxt',
                    dstpath='labels/train',
                    extractclassname=class_15)

