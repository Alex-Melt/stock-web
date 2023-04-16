## 股票推荐系统

## 1.python解决跨域问题

1. pip install django-cors-headers
2. 配置settings.py文件

```python
INSTALLED_APPS = [
    ...,
    'corsheaders',  # 1 用来解决跨域 
]
MIDDLEWARE = [
    ...,
    'corsheaders.middleware.CorsMiddleware',  # 2 解决跨域-中间件的位置是固定的
    'django.middleware.common.CommonMiddleware',
    ...
]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'GET',
    'POST',
    'DELETE',
    'OPTIONS',
    'PATCH',
    'PUT',
    'VIEW'
)
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'x-csrftoken',
    'x-requested-with',
    'origin',
    'dnt'
)
```

## 2.修改数据库设置

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'reco_system',  # 数据库的名字，可以在mysql的提示符下先创建好
        'USER': 'root',  # 数据库用户名
        'PASSWORD': 'root',  # 数据库密码
        'HOST': 'localhost',  # 数据库主机，留空默认为"localhost"
        'PORT': '3308',  # 数据库使用的端口
    }
}
```

## 3.修改项目端口

在manage.py中修改
```python
if __name__ == '__main__':
    from django.core.management.commands.runserver import Command as RunServer
    RunServer.default_port = '8001'
    main()
```

## 4.编写统一的返回格式

```python
from django.http import JsonResponse, HttpResponse
# 自定义状态码
class HttpCode(object):
    ok = 200
    paramserrors = 400
    unauth = 401
    methoderror = 405
# 定义统一的json字符串返回
def result(code=0, msg="success", data=None, kwargs=None):
    json_dict = {"code": 0, "msg": msg, "data": data}
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)
```

## 使用restful风格

1. pip install djangorestframework
2. 添加到app配置中
```python
INSTALLED_APPS = [
    ...,
    'rest_framework'
]
```

## token校验

1. 创建token.py
2. 若登陆成功则生成token
3. 中间件拦截验证py文件
4. 注册进中间件

## token时间设置

```python
"""
fromtimestamp()     #时间戳转换成时间
timedelta()         #加减时间
now()               #获取当前时间,并转换为字符串
timestamp()         #时间转换成时间戳
strftime()          #转换为字符串   cls
strptime()          #字符串转换为时间 self   datetime.datetime
datetime()          #定格时间
date()              #返回dt年月日
time()              #返回时分秒
"""

import datetime
import time

ts = time.time()
print(datetime.datetime.fromtimestamp(ts))
delta = datetime.timedelta(days=5)  # 加减时间
d = datetime.datetime.now()  # 获取当前时间
d3 = d.timestamp()#时间转换成时间戳
d1 = d.strftime("%Y%m%d")
d2 = datetime.datetime.strptime(d1, "%Y%m%d")  # 字符串转换为时间     self
dt = datetime.datetime(year=2023, month=12, day=1)  # 定格时间
########################################
#其他:私有化和实例化
print(type(dt))  # <class 'datetime.datetime'>
y = dt.year
m = dt.month
d = dt.day
str_time = dt.strftime("%Y")  # self   实例化方法
print(str_time)
dt = datetime.datetime.strptime("2022-2-2", "%Y-%m-%d")  # cls  类方法
print(dt)
#dt=datetime.datetime(year=2033,month=11,day=11)
print(dt.date())
print(dt.time())
```

## 5.编写stocks应用

### 1.创建app

- 生成独立的app应用：`python manage.py startapp stocks`
- 将生成的app注册到settings中，

```python
INSTALLED_APPS = [
    ..., # 这些是默认的配置
    'stocks',# 将你创建的app注册在此处
]
```

### 2.进行库表分析，设计数据库结构

### 3.请求与响应、绑定url与视图函数

1. 在stocks下创建`urls.py`
2. 对`urls.py`编辑
```python
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
]
```
3. 编辑views
4. 将配置的urls注册到项目根urls当中
```python
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    # 前端接口统一采用api前缀
    path('', include('stocks.urls')),
    path('admin/', admin.site.urls),
]
```

   ```python
   from django.shortcuts import render
   from django.http import HttpResponse
   
   
   # Create your views here.
   def index(request):
       return HttpResponse("hello")
   ```

7. 将配置的应用路由告诉django，将此配置写入到项目的总的urls配置中，编辑`urls.py`

   1. 使用`include`将自己配置的url包含

   ```python
   from django.contrib import admin
   from django.urls import path,include
   
   urlpatterns = [
       path('', include('blog.urls')),
       path('admin/', admin.site.urls),
   ]
   ```

### 6. 模板系统