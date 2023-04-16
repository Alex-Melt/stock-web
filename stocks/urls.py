# @Time : 2023/3/16 11:20 
# @Author : 赵浩栋
# @File : urls.py 
# @Software: PyCharm
from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('sys/user/info', views.sys_user_info, name='sys_user_info'),
    path('sys/login', views.sys_login, name='sys_login'),
    path('sys/register', views.sys_register, name='sys_register'),
    path('sys/logout', views.sys_logout, name='sys_logout'),
    path('sys/user/password', views.sys_user_password, name='sys_user_password'),
    path('sys/menu/nav', views.sys_menu_nav, name='sys_menu_nav'),

    path('stock/getnewslist', views.stock_get_news_list, name='stock_get_news_list'),
    path('stock/updatenewslist', views.stock_update_news_list, name='stock_update_news_list'),

    path('stock/getstocklist', views.stock_get_stock_list, name='stock_get_stock_list'),
    path('stock/getshstock', views.stock_get_sh_stock, name='stock_get_sh_stock'),
    path('stock/updateshstock', views.update_sh_stock, name='update_sh_stock'),
    path('stock/updatestocklist', views.update_stock_list, name='update_stock_list'),
    path('stock/getstockinfobyid', views.get_stock_info_by_id, name='get_stock_info_by_id'),
    path('stock/getstockbid', views.get_stock_bid, name='get_stock_bid'),

    path('stock/getstocktimebar', views.get_stock_time_bar, name='get_stock_time_bar'),
    path('stock/getstockdaybar', views.get_stock_day_bar, name='get_stock_day_bar'),
    path('stock/getstockweekbar', views.get_stock_week_bar, name='get_stock_week_bar'),
    path('stock/getstockmonthbar', views.get_stock_month_bar, name='get_stock_month_bar'),
    path('stock/updatesinglestock', views.update_single_stock, name='update_single_stock'),

    path('user/info', views.user_info, name='user_info'),
    path('user/save', views.user_save, name='user_save'),


]
