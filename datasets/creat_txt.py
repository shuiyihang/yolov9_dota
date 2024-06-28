
# 将train中所有图片的相对路径保存到dota_train.txt中

import os

open_dir = './images/train/images'
save_file = 'dota_train.txt'
def save_image_paths_to_txt():
    # 获取当前工作目录
    current_directory = os.getcwd()

    # 定义imgs文件夹的路径
    imgs_directory = os.path.join(current_directory, open_dir)

    # 检查imgs文件夹是否存在
    if not os.path.exists(imgs_directory):
        print("imgs文件夹不存在")
        return

    # 定义要保存的txt文件的路径
    output_file = os.path.join(current_directory, save_file)

    # 打开txt文件进行写入
    with open(output_file, "w") as file:
        # 遍历imgs文件夹中的所有文件
        for root, dirs, files in os.walk(imgs_directory):
            for name in files:
                # 获取文件的相对路径
                relative_path = os.path.join(open_dir, name).replace(os.sep,'/')

                # 将相对路径写入txt文件
                file.write(relative_path + "\n")
                print(relative_path)

    print(f"图片路径已保存到 {output_file}")


# 调用函数执行操作
save_image_paths_to_txt()
