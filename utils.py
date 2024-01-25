from PIL import Image
import os
import glob
from constants import *


class ImageProcessor:
    def __init__(self, name, image_name):
        self.name = name
        self.image_path = input_path + image_name
        self.image = None
        self.load_image()

    def load_image(self):
        try:
            self.image = Image.open(self.image_path)
        except Exception:
            pass

    def image_decode(self):
        if self.image:
            pixels = self.image.load()
            binary_ends = []

            for y in range(self.image.size[1]):
                for x in range(self.image.size[0]):
                    pixel = pixels[x, y]
                    binary_end = format(pixel[0] % 2, 'b')  # 获取红色通道的最低位
                    binary_ends.append(binary_end)

            # 保存2进制末尾到文件
            output_file_path = self.name + "_PBE.tem"
            binary_ends_str = ''.join(binary_ends)
            with open(output_file_path, 'w') as file:
                file.write(binary_ends_str)

            # 统计每个像素二进制末尾0和1出现的频率
            zero_count, one_count = image_count(binary_ends)
            return zero_count, one_count
        else:
            raise ValueError("未加载图片。")

    def image_encode(self):
        if self.image:
            # 读取2进制末尾文件
            input_file_path = self.name + "_PBE.tem"

            with open(input_file_path, 'r') as file:
                binary_ends = file.read()  # 读取文件

            pixels = self.image.load()
            index = 0

            for y in range(self.image.size[1]):
                for x in range(self.image.size[0]):
                    pixel = list(pixels[x, y])
                    #print(f"index: {index}, len(binary_ends): {len(binary_ends)}")
                    pixel[0] = (pixel[0] & 0xFE) | int(binary_ends[index], 2)  # 设置红色通道的最低位
                    pixels[x, y] = tuple(pixel)
                    index += 1
            output_image_path = output_path + self.name + "_out.png"

            self.image.save(output_image_path)

            # 返回临时文件路径以便删除
            return input_file_path
        else:
            raise ValueError("未加载图片。")


# 统计每个像素二进制末尾0和1出现的频率
def image_count(binary_ends):
    zero_count = 0
    one_count = 0

    for binary_end in binary_ends:
        zero_count += binary_end.count('0')
        one_count += binary_end.count('1')

    return zero_count, one_count


# 将字符串转换为二进制
def encode_massage(message):
    str_message = str(message)
    binary_message = ''.join(format(ord(char), '08b') for char in str_message)
    return binary_message


# 将二进制末尾转换为字符串
def decode_massage(binary_ends):
    message = ''.join(chr(int(''.join(binary_ends[i:i+8]), 2)) for i in range(0, len(binary_ends), 8))
    return message


# 文件夹检测
def folder_check(check_folder):
    if not os.path.exists(check_folder):
        # 如果文件夹不存在，创建文件夹
        os.makedirs(check_folder)


# 开始文件夹检测
def start_folder_check():
    for check_folder in all_folders:
        folder_check(check_folder)


# 临时文件清理
def delete_temp_files():
    # 获取当前工作目录
    current_directory = os.getcwd()

    # 构建匹配模式以查找.tem文件
    pattern = os.path.join(current_directory, '*.tem')

    # 使用glob.glob查找匹配的文件列表
    temp_files = glob.glob(pattern)

    # 循环遍历并删除每个文件
    for file_path in temp_files:
        try:
            os.remove(file_path)
        except Exception:
            pass


def overwrite_binary(binary_end, binary_message, binary_sign):
    if len(binary_end) >= (128 + len(binary_message) +128 + len(binary_sign)):
        #print(len(binary_end))
        # 计算 binary_message 的长度，并将二进制数据
        message_length = len(binary_message)
        sign_length = len(binary_sign)
        binary_message_length = bin(message_length)[2:].zfill(128)
        binary_sign_length = bin(sign_length)[2:].zfill(128)
 
        binary_message_list = list(binary_message)
        binary_end_list = list(binary_end)
        binary_message_length_list = list(binary_message_length)
        binary_sign_list = list(binary_sign)
        binary_sign_length_list = list(binary_sign_length)

        # 在 binary_end 的前 128 字节写入长度标记
        binary_end_list[:128] = binary_message_length_list
        # 将 binary_message 覆写到 binary_end，保留原来的部分
        binary_end_list[128:128+len(binary_message)] = binary_message_list
        binary_end_list[128+len(binary_message):128+len(binary_message)+128] = binary_sign_length_list
        binary_end_list[128+len(binary_message)+128:128+len(binary_message)+128+len(binary_sign)] = binary_sign_list
        return ''.join(binary_end_list)
    else:
        # 如果binary_end较小，可以选择抛出异常或执行其他操作
        raise ValueError("文本过长")


def read_binary_message(binary_end):
    # 从binary_end的前128字节读取message_length
    message_length_bytes = binary_end[:128]

    # 将message_length解码为整数
    message_length = int(message_length_bytes, 2)

    # 从binary_end的128到128+message_length字节之间读取binary_message
    binary_message = binary_end[128:128 + message_length]

    sign_length_bytes = binary_end[128 + message_length:128 + message_length+128]
    sign_length = int(sign_length_bytes, 2)
    sign = binary_end[128+message_length+128: 128 + message_length + 128 + sign_length]
    return binary_message, sign

