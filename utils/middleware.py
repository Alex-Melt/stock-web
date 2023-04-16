# @Time : 2023/3/16 16:17 
# @Author : 赵浩栋
# @File : middleware.py 
# @Software: PyCharm
import logging

from utils.R import result
from utils.token import check_token

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object

# 白名单，表示请求里面的路由时不验证登录信息
API_WHITELIST = ["/sys/login", "/sys/register"]


class AuthorizeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger = logging.getLogger()
        if request.path.startswith("/admin"):
            pass
        elif request.path not in API_WHITELIST:
            logger.info(f"url拦截===========>{request.path}")
            # 从请求头中获取 username 和 token
            token = request.COOKIES.get('token')
            # if username is None or token is None:
            if token is None:
                return result(code=500, msg="未查询到登录信息")
            else:
                # 调用 check_token 函数验证
                if check_token(token):
                    pass
                else:
                    return result(code=500, msg="登录信息错误或已过期")
