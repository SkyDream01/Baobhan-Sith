import os
import csv
from constants import *


def config_check():
    config_file_path = config_path + 'config.csv'
    if not os.path.exists(config_file_path):
        # 如果文件不存在，创建文件
        with open(config_file_path, 'w', newline='') as csvfile:
            fieldnames = ['key', 'value']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    return True


# 保存项目与值,如果遇到相同的项目就覆写
def save_config(key, value):
    config_file_path = config_path + 'config.csv'

    # 读取现有配置
    existing_config = {}
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            existing_config = {row['key']: row['value'] for row in reader}

    # 更新或添加新的配置项
    existing_config[key] = value

    # 写入配置到文件
    with open(config_file_path, 'w', newline='') as csvfile:
        fieldnames = ['key', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for key, value in existing_config.items():
            writer.writerow({'key': key, 'value': value})


def read_config():
    config_file_path = config_path + 'config.csv'

    config_data = {}
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                config_data[row['key']] = row['value']

    return config_data


def search_config(key):
    config_file_path = config_path + 'config.csv'

    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['key'] == key:
                    return row['value']

    # 如果键不存在，返回None或者你认为合适的默认值
    return None
