from utils import *
from RSA import *
from config import *


def encode_message2img(private_key, public_key):
    image_name = input("请输入图片名称：")
    encrypted_image = ImageProcessor("encrypted_image",image_name)
    message = input("请输入要加密的信息：")
    encrypted_message = encrypt_with_public_key(message, public_key)
    sign = sign_message(message, private_key)
    #print("加密后的信息：", encrypted_message)
    encrypted_image.image_decode()
    temp_file = encrypted_image.name + "_PBE.tem"
    with open(temp_file, 'r') as file:
        binary_ends = file.read()  # 读取文件
    binary_message = encode_massage(encrypted_message)
    binary_sign = encode_massage(sign)
    binary_ends = overwrite_binary(binary_ends, binary_message, binary_sign)
    with open(temp_file, 'w') as file:
        file.write(binary_ends)
    encrypted_image.image_encode()


def decode_img2message(private_key, public_key):
    image_name = input("请输入图片名称：")
    decrypted_image = ImageProcessor("decrypted_image",image_name)
    decrypted_image.image_decode()
    temp_file = decrypted_image.name + "_PBE.tem"
    with open(temp_file, 'r') as file:
        binary_ends = file.read()  # 读取文件
    binary_message ,binary_sign =read_binary_message(binary_ends)
    encrypted_message = decode_massage(binary_message)
    sign = decode_massage(binary_sign)
    decrypted_message = decrypt_with_private_key(encrypted_message, private_key)
    verify_signature(decrypted_message, sign, public_key)
    print(decrypted_message)


def OptionMenu():
    private_key = start_private_key()
    print("请选择操作：")
    print("1.加密图片")
    print("2.解密图片")
    option = int(input("请输入选项："))
    if option == 1:
        public_key_name = input("请选择公钥：")
        public_key=load_public_key(public_key_name)
        encode_message2img(private_key,public_key)
        print("图片保存在output文件夹")
    elif option == 2:
        public_key_name = input("请选择公钥：")
        public_key=load_public_key(public_key_name)
        decode_img2message(private_key,public_key)
    else:
        print("无效的选项")


def main():
    start_folder_check()
    config_check()
    OptionMenu()


    #encode_message2img()
    #decode_img2message()
    delete_temp_files()


    


if __name__ == '__main__':
    main()

