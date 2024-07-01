from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
import os
import shutil
import random
import string
import argparse
import questionary
import sys


# AESで暗号化
def encrypt_file_AES(input_file, times):
    # ファイルの読み込み
    if os.path.exists(input_file) is False:
        print("file is not found.")
        sys.exit()
    with open(input_file, "rb") as f:
        data = f.read()
    print(input_file + " is encrypted start.")
    for i in range(0, int(times)):
        # AESで使用する鍵とIV（Initialization Vector）を生成
        backend = default_backend()
        iv = os.urandom(16)  # IVはランダムに生成する
        cipher = Cipher(
            algorithms.AES(randomname(32).encode("utf-8")[:32]),
            modes.CFB(iv),
            backend=backend,
        )
        encryptor = cipher.encryptor()

        # データをAESで暗号化し、IVを先頭に追加
        encrypted_data = encryptor.update(data) + encryptor.finalize()

    # IVと暗号化されたデータをファイルに書き込む
    with open(input_file, "wb") as f:
        f.seek(0)
        f.write(iv + encrypted_data)

    print(input_file + " is encrypted ok.")


# RSA暗号で暗号化
def generate_rsa_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()

    return private_key, public_key


def encrypt_file_RSA(input_file, public_key, times):
    # ファイルの読み込み
    if os.path.exists(input_file) is False:
        print("file is not found.")
        sys.exit()
    # ファイルの読み込み
    with open(input_file, "rb") as f:
        data = f.read()
    print(input_file + " is encrypted start.")
    for i in (0, times):
        # データをRSAで暗号化
        encrypted_data = public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

    # 暗号化されたデータをファイルに書き込む
    with open(input_file, "wb") as f:
        f.seek(0)
        f.write(encrypted_data)

    print(input_file + " is encrypted ok.")


def randomname(n):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return "".join(randlst)


def get_files_in_directory(directory):
    file_list = []

    # ディレクトリを再帰的に探索し、ファイルをリストに追加する
    for root, directories, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_list.append(file_path)
    return file_list


# メインの実行部分
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Please delete directory or file.")
    parser.add_argument(
        "--rm", action="store_true", help="You could remove your encrypted file."
    )
    parser.add_argument(
        "--remove", action="store_true", help="You could remove your encrypted file."
    )
    parser.add_argument(
        "-t", help="You could be set encrypting times.", type=int, default=1
    )
    parser.add_argument(
        "--times", help="You could set encrypting times.", type=int, default=1
    )
    parser.add_argument(
        "-A", help="You could set encrypting algorism.", type=str, default="AES"
    )
    parser.add_argument(
        "--Algorism",
        help="You could be set encrypting algorithm.",
        type=str,
        default="AES",
    )
    parser.add_argument("--rf", action="store_true")
    args = parser.parse_args()
    while args.rf is False:
        que = questionary.text(
            "are you sure you want to delete or encrypt it? y(yes)/n(no)"
        ).ask()
        if que.upper() == "N" or que.upper() == "NO":
            sys.exit()
        elif que.upper() == "Y" or que.upper() == "YES":
            break
        else:
            print("plese response question y/n.")
    if os.path.isdir(args.file):
        for input_file in get_files_in_directory(args.file):
            times = args.t if args.t != 1 else args.times if args.times != 1 else 1
            if args.A.upper() == "AES" or args.Algorism.upper() == "AES":
                # ファイルを暗号化
                encrypt_file_AES(input_file, times)
            elif args.A.upper() == "RSA" or args.Algorism.upper() == "RSA":
                # RSA鍵ペアの生成
                private_key, public_key = generate_rsa_key_pair()
                # ファイルの暗号化
                encrypt_file_RSA(input_file, public_key, times)

        if args.rm or args.remove:
            shutil.rmtree(args.file)
    else:
        times = args.t if args.t != 1 else args.times if args.times != 1 else 1
        if args.A.upper() == "AES" or args.Algorism.upper() == "AES":
            # ファイルを暗号化
            encrypt_file_AES(args.file, times)
        elif args.A.upper() == "RSA" or args.Algorism.upper() == "RSA":
            # RSA鍵ペアの生成
            private_key, public_key = generate_rsa_key_pair()
            # ファイルの暗号化
            encrypt_file_RSA(args.file, public_key, times)
        if args.rm or args.remove:
            os.remove(args.file)
    print("Encryption completed successfully.")

if __name__ == "__main__":
    main()
