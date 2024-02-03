from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import os
from ast import literal_eval
from constants import *
from config import *


# 生成RSA密钥对
def generate_key_pair():
    key = RSA.generate(4096)  # 4096位的RSA密钥对
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


# 使用公钥加密消息
def encrypt_with_public_key(message, public_key):
    key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(key)
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message


# 使用私钥解密消息
def decrypt_with_private_key(encrypted_message_str, private_key):
    encrypted_message = literal_eval(encrypted_message_str)
    key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(key)
    decrypted_message = cipher.decrypt(encrypted_message).decode()
    return decrypted_message


# 使用私钥签名消息
def sign_message(message, private_key_bytes):
    private_key = serialization.load_pem_private_key(
        private_key_bytes,
        password=None,
        backend=default_backend()
    )
    signature = private_key.sign(
        message.encode('utf-8'),  # 将消息编码为字节
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


# 使用公钥验证签名
def verify_signature(message, signature_bytes, public_key_bytes):
    public_key = serialization.load_pem_public_key(
        public_key_bytes,
        backend=default_backend()
    )
    signature = literal_eval(signature_bytes)
    try:
        public_key.verify(
            signature,
            message.encode('utf-8'),  # 将消息编码为字节
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("Signature is valid.")
        return True
    except Exception as e:
        print("Signature is invalid:", str(e))
        return False


# 检查是否有私钥文件，如果没有生成私钥，并保存在本地，如果有读取并返回
def load_private_key(key_name):
    private_key_path = key_path + key_name + '_private_key.pem'
    public_key_path = key_path + key_name + '_public_key.pem'
    if not os.path.exists(private_key_path):
        private_key, public_key = generate_key_pair()
        with open(private_key_path, "wb") as f:
            f.write(private_key)
        with open(public_key_path, "wb") as f:
            f.write(public_key)
        return private_key
    else:
        with open(private_key_path, "rb") as f:
            private_key = f.read()
        return private_key


# 读取公钥
def load_public_key(key_name):
    public_key_path = key_path + key_name
    with open(public_key_path, "rb") as f:
        public_key = f.read()
    return public_key

def start_private_key():
    private_key_name =search_config("private_key_name")
    if not (private_key_name== None):
        private_key =load_private_key(search_config("private_key_name"))
    else:
        print("找不到密钥，现在创建密钥")
        key_name = input("请输入密钥名称：")
        private_key = load_private_key(key_name)
        save_config("private_key_name", key_name)
    return private_key