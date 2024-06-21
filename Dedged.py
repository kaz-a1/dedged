from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import shutil
import random
import string
import argparse

def encrypt_file(input_file, times):

    # ファイルの読み込み
    with open(input_file, 'rb') as f:
        data = f.read()
    print(input_file + "is encrypted start.")
    for i in range(0, int(times)):
        # AESで使用する鍵とIV（Initialization Vector）を生成
        backend = default_backend()
        iv = os.urandom(16)  # IVはランダムに生成する
        cipher = Cipher(algorithms.AES(randomname(32).encode('utf-8')[:32]), modes.CFB(iv), backend=backend)
        encryptor = cipher.encryptor()

        # データをAESで暗号化し、IVを先頭に追加
        encrypted_data = encryptor.update(data) + encryptor.finalize()

    # IVと暗号化されたデータをファイルに書き込む
    with open(input_file, 'wb') as f:
        f.write(iv + encrypted_data)

    print(input_file + "is encrypted ok.")

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
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="please delete directory or file.")
    parser.add_argument("-rm", action="store_true", help="you could remove your encrypted file.")
    parser.add_argument("-remove", action="store_true", help="you could remove your encrypted file.")
    parser.add_argument("-t", help="you could be set ecryting times.", type=int, default=1)
    parser.add_argument("-times", help="you could be set ecryting times.", type=int, default=1)
    args = parser.parse_args()
    if os.path.isdir(args.file):
        for input_file in get_files_in_directory(args.file):
            times = args.t if args.t != 1 else args.times if args.times != 1 else 1
            # ファイルを暗号化
            encrypt_file(input_file, times)

        if args.rm or args.remove:
            shutil.rmtree(args.file)
    else:
        times = args.t if args.t != 1 else args.times if args.times != 1 else 1
        encrypt_file(args.file, times)
        if args.rm or args.remove:
            os.remove(args.file)
            
    print("Encryption completed successfully.")
