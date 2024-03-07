# -*- coding:utf-8 -*-

"""
@Version  : Python3.8
@FileName : password.py
@Time     : 2024/3/3 1:16
@Author   : wiesZheng
@Function :
"""
import hashlib
import bcrypt

from config import Settings

salt = 'brisk'


def verify_password(plain_password: str, hashed_password: str) -> bool:
    correct_password: bool = bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
    return correct_password


def get_password_hash(password: str) -> str:
    hashed_password: str = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    return hashed_password


def hash_psw(password: str):
    # 每次加密都进行一次salt生成, 让每次加密的hash都不同
    add_salt = bcrypt.gensalt(rounds=Settings.BCRYPT_ROUNDS)
    hashed = bcrypt.hashpw(password.encode(), add_salt)
    return hashed.decode()


def verify_psw(plain_psw: str, hashed_psw: str):
    try:
        result = bcrypt.checkpw(plain_psw.encode(), hashed_psw.encode())
        return result
    except Exception as e:
        return False

# def add_salt(password: str):
#     m = hashlib.md5()
#     bt = f"{password}{salt}".encode("utf-8")
#     m.update(bt)
#     return m.hexdigest()

