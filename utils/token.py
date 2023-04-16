# @Time : 2023/3/16 14:14 
# @Author : 赵浩栋
# @File : token.py 
# @Software: PyCharm
import time

import jwt
from django.core import signing
import hashlib

# HEADER = {'typ': 'JWP', 'alg': 'default'}
# KEY = "stock"
# SALT = "blog.zewan.cc"
#
#
# def encrypt(obj):
#     """加密：signing 加密 and Base64 编码"""
#     value = signing.dumps(obj, key=KEY, salt=SALT)
#     value = signing.b64_encode(value.encode()).decode()
#     return value
#
#
# def decrypt(src):
#     """解密：Base64 解码 and signing 解密"""
#     src = signing.b64_decode(src.encode()).decode()
#     raw = signing.loads(src, key=KEY, salt=SALT)
#     return raw
#
#
# def create_token(username):
#     """生成token信息"""
#     # 1. 加密头信息
#     header = encrypt(HEADER)
#     # 2. 构造Payload(有效期14天)
#     payload = {"username": username, "iat": time.time(),
#                "exp": time.time() + 1209600.0}
#     payload = encrypt(payload)
#     # 3. MD5 生成签名
#     md5 = hashlib.md5()
#     md5.update(("%s.%s" % (header, payload)).encode())
#     signature = md5.hexdigest()
#     token = "%s.%s.%s" % (header, payload, signature)
#     return token
#
#
# def get_payload(token):
#     """解析 token 获取 payload 数据"""
#     payload = str(token).split('.')[1]
#     payload = decrypt(payload)
#     return payload
#
#
# def get_username(token):
#     """解析 token 获取 username"""
#     payload = get_payload(token)
#     return payload['username']
#
#
# def get_exp_time(token):
#     """解析 token 获取过期时间"""
#     payload = get_payload(token)
#     return payload['exp']
from jwt import ExpiredSignatureError


def create_token(user_id, username, exp_time, now_time):
    """生成token信息"""
    b = {'user_id': user_id,
         'username': username,
         'exp': exp_time,
         'iat': now_time,
         }
    token = jwt.encode(b, 'stock', algorithm='HS256')
    return token


def check_token(token):
    """验证 token：检查 username 和 token 是否一致且未过期"""
    try:
        jwt.decode(token, key='stock', algorithms=['HS256'])
    except ExpiredSignatureError:
        return False
    # return get_username(token) == username and get_exp_time(token) > time.time()
    return True


def get_token_info(token):
    token_info = jwt.decode(token, key='stock', algorithms=['HS256'])
    return {'user_id': token_info['user_id'], 'username': token_info['username']}
