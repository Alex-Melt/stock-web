from django.contrib import admin
from .models import Sys_user,Sys_user_token,Sys_menu,Stock

# Register your models here.
# 将创建的模型注册到admin上，方便管理
admin.site.register(Sys_user)
admin.site.register(Sys_user_token)
admin.site.register(Sys_menu)
admin.site.register(Stock)
