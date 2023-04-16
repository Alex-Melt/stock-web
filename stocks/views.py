import datetime
import json

import js2py
import requests
from MySQLdb import ProgrammingError
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.forms import model_to_dict
from django.utils import timezone
from rest_framework.decorators import api_view

from utils.R import result
from utils.token import get_token_info, create_token
from .crawler import crawlStockTimeInfoList, crawlStockDayInfoList
from .models import *
# 获取登录的用户信息
from .sql_concat import SQLConn


# Create your views here.


@api_view(['GET'])
def sys_user_info(request):
    token_info = get_token_info(token=request.COOKIES.get('token'))
    return result(kwargs={'user': token_info})


# 用户登录
@api_view(['POST'])
def sys_login(request):
    json_dict = json.loads(request.body)
    # 先获取到用户名和密码，然后需要做几个判断
    username = json_dict.get("username", None)
    password = json_dict.get("password", None)
    if username:
        # 判断用户名是否存在
        try:
            get_user = Sys_user.objects.get(username=username)
        except:
            return result(code=500, msg="用户不存在")
        # 判断密码是否一致
        if get_user.password != password:
            return result(code=500, msg="密码不正确")
        else:
            # 使用get获取数据会报错
            try:
                get_user_token = Sys_user_token.objects.get(user_id=get_user.user_id)
            except Sys_user_token.DoesNotExist:
                get_user_token = None
            request.session["userId"] = get_user.user_id
            expire = 3600 * 12  # 设置过期时间为12个小时
            exp_time = timezone.now() + timezone.timedelta(seconds=expire)
            now_time = timezone.now()
            token = create_token(user_id=get_user.user_id, username=username, exp_time=exp_time, now_time=now_time)
            if get_user_token is None:
                Sys_user_token.objects.create(
                    user_id=get_user.user_id,
                    token=token,
                    expire_time=exp_time,
                    update_time=now_time)
            else:
                get_user_token.expire_time = exp_time
                get_user_token.update_time = now_time
                get_user_token.save()
            # print(f"token生成了{token}完成了\n过期时间{expire}")
            return result(kwargs={"token": token, "expire": expire})


# 用户注册
@api_view(['POST'])
def sys_register(request):
    json_dict = json.loads(request.body)
    # 先获取到用户名和密码，然后需要做几个判断
    username = json_dict.get("username", None)
    password = json_dict.get("password", None)
    mobile = json_dict.get("telephone", None)
    if username:
        # 判断用户名是否存在
        get_user = Sys_user.objects.filter(username=username)
        if get_user.count() > 0:
            return result(code=500, msg="当前用户已存在")
        user = Sys_user(username=username, password=password, mobile=mobile)
        try:
            user.save()
            get_user = Sys_user.objects.get(username=username)
            request.session["userId"] = get_user.user_id
            expire = 3600 * 12  # 设置过期时间为12个小时
            exp_time = timezone.now() + timezone.timedelta(seconds=expire)
            now_time = timezone.now()
            token = create_token(user_id=get_user.user_id, username=username, exp_time=exp_time, now_time=now_time)
            Sys_user_token.objects.create(
                user_id=get_user.user_id,
                token=token,
                expire_time=exp_time,
                update_time=now_time)
            return result(kwargs={"token": token, "expire": expire})
        except:
            return result(code=500, msg="注册失败，请重试！")


# 当前用户修改密码
@api_view(['POST'])
def sys_user_password(request):
    json_dict = json.loads(request.body)
    get_password = json_dict.get('password')
    get_newPassword = json_dict.get('newPassword')
    if len(get_newPassword) == 0:
        return result(code=500, msg="新密码不能为空")
    token_info = get_token_info(token=request.COOKIES.get('token'))
    query_user = Sys_user.objects.get(user_id=token_info['user_id'])
    if query_user.password != get_password:
        return result(code=500, msg="原密码错误")
    query_user.password = get_newPassword
    query_user.save()
    return result()


# 获取用户菜单列表
@api_view(['GET'])
def sys_menu_nav(request):
    menu_filter = Sys_menu.objects.filter(parent_id=0)
    menuList = [model_to_dict(menu) for menu in menu_filter]
    for i in menuList:
        if i['type'] == 0:
            i['list'] = [model_to_dict(j) for j in Sys_menu.objects.filter(parent_id=i['menu_id'])]
    return result(kwargs={'menuList': menuList})


# 用户登出
@api_view(['GET'])
def sys_logout(request):
    if request.session.get("userId"):
        del request.session["userId"]
    token_info = get_token_info(token=request.COOKIES.get('token'))
    user_token = Sys_user_token.objects.get(user_id=token_info['user_id'])
    user_token.token = None
    user_token.save()
    return result()


# 获取股票数据信息
@api_view(['GET'])
def stock_get_stock_list(request):
    page = request.GET.get('page')
    pageSize = request.GET.get('limit')
    stockNum = str(request.GET.get('stockNum')).strip()
    stockName = str(request.GET.get('stockName')).strip()
    stock_all = Stock.objects.filter(stockNum__contains=stockNum, stockName__contains=stockName).order_by('stockId')
    paginator = Paginator(stock_all, pageSize)
    try:
        stock_list = paginator.page(page)
    except PageNotAnInteger:
        stock_list = paginator.page(1)
    except EmptyPage:
        stock_list = paginator.page(paginator.num_pages)
    stock_list = json.loads(serializers.serialize("json", stock_list))
    return result(kwargs={"page": {"list": stock_list, "totalCount": paginator.count}})


# 获取上证指数
@api_view(['GET'])
def stock_get_sh_stock(request):
    res = ShStock.objects.filter(INDEX_CODE__in=["000001", "000688", "000010", "000016", "000009"])
    sh_stock = json.loads(serializers.serialize("json", res))
    return result(kwargs={"list": sh_stock})


# 更新上证指数
@api_view(['GET'])
def update_sh_stock(request):
    jsonpCallback_num = js2py.eval_js("Math.floor(Math.random() * (100000000 + 1))")
    now_time = js2py.eval_js("new Date().getTime()")
    url = f"http://query.sse.com.cn/commonQuery.do?jsonCallBack=jsonpCallback{jsonpCallback_num}&isPagination=false&sqlId=COMMON_SSE_SJ_SZZS_ZDZSJYBBXXX&_={now_time}"
    headers = {
        "Referer": "http://www.sse.com.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url=url, headers=headers).text
        resp = resp[22:-1]
        res_list = json.loads(resp)['result']
    except:
        return result(code=500, msg="上证指数链接失效")
    for res in res_list:
        try:
            update_info = ShStock.objects.get(INDEX_CODE=res['INDEX_CODE'])
            update_info.INDEX_ABBR = res['INDEX_ABBR']
            update_info.TOTAL_VALUE = res['TOTAL_VALUE']
            update_info.AVG_PRICE = res['AVG_PRICE']
            update_info.TRADE_AMT = res['TRADE_AMT']
            update_info.VALUE_RATIO = res['VALUE_RATIO']
            update_info.CLOSE_POINT = res['CLOSE_POINT']
            update_info.KIND_NUM = res['KIND_NUM']
            update_info.TRADE_DATE = res['TRADE_DATE']
            update_info.RANK = res['RANK']
            update_info.PE_RATIO = res['PE_RATIO']
            update_info.AVG_VOL = res['AVG_VOL']
            update_info.save()
        except ShStock.DoesNotExist:
            create_sh_stock = ShStock(
                INDEX_ABBR=res['INDEX_ABBR'],
                TOTAL_VALUE=res['TOTAL_VALUE'],
                AVG_PRICE=res['AVG_PRICE'],
                TRADE_AMT=res['TRADE_AMT'],
                VALUE_RATIO=res['VALUE_RATIO'],
                INDEX_CODE=res['INDEX_CODE'],
                CLOSE_POINT=res['CLOSE_POINT'],
                KIND_NUM=res['KIND_NUM'],
                TRADE_DATE=res['TRADE_DATE'],
                RANK=res['RANK'],
                PE_RATIO=res['PE_RATIO'],
                AVG_VOL=res['AVG_VOL']
            )
            create_sh_stock.save()
    return result(msg="更新上证数据成功！")


# 更新股票列表
@api_view(['GET'])
def update_stock_list(request):
    size = request.GET.get('size')
    url = "http://19.push2.eastmoney.com/api/qt/clist/get"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    params = {
        'pn': '1',
        'pz': f'{size}',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:1+t:2,m:1+t:23',
        'fields': "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f38,f39,f22,f11,f62,f128,f136,f115,f152,f297"
    }
    try:
        resp = requests.get(url=url, data=params, headers=headers).json()
        resp = resp['data']
    except:
        return result(code=500, msg='股票列表更新失败')
    new_stock_list = resp['diff']
    old_stock_list = [list(i.values())[0] for i in Stock.objects.values('stockNum')]
    for new_stock in new_stock_list:
        if new_stock['f12'] not in old_stock_list:
            stock = Stock(
                stockNum=new_stock['f12'],
                stockName=new_stock['f14'],
                totalFlowShares=new_stock['f39'],
                totalShares=new_stock['f38'],
                upDownRange=new_stock['f3'],
                turnOverrate=new_stock['f8'],
                upDownPrices=new_stock['f4'],
                open=new_stock['f17'],
                close=new_stock['f2'],
                high=new_stock['f15'],
                low=new_stock['f16'],
                preClose=new_stock['f18'],
                volume=new_stock['f5'],
                amount=new_stock['f6'],
                amplitude=new_stock['f7'],
                totalMarketValue=new_stock['f26'],
                flowMarketValue=new_stock['f21'],
                listingDate=new_stock['f26'],
            )
            stock.save()
    return result(msg="更新股票列表成功！")


# 单股数据展示
@api_view(['GET'])
def get_stock_info_by_id(request):
    stockId = str(request.GET.get('stockId')).strip()
    try:
        # stock_information = Stock.objects.filter(Q(stockNum=stockId) | Q(stockName=stockId))
        stock_information = Stock.objects.filter(stockNum=stockId)
        if stock_information.count() == 0:
            return result(code=500, msg="暂未查询到交易信息")
        stock_list = json.loads(serializers.serialize("json", stock_information))
        return result(kwargs={'data': stock_list})
    except Stock.DoesNotExist:
        return result(code=500, msg="暂无该目标数据信息")


# 得到交易信息
@api_view(['GET'])
def get_stock_bid(request):
    stock_information = StockBid.objects.filter(stockNum=str(request.GET.get('stockNum')).strip())
    if stock_information.count() == 0:
        return result(code=500, msg="暂未查询到交易信息")
    stock_list = json.loads(serializers.serialize("json", stock_information))
    return result(kwargs={'data': stock_list})


# 获取分钟线数据
@api_view(["GET"])
def get_stock_time_bar(request):
    stockNum = request.GET.get('stockNum')
    try:
        fetchall = SQLConn(stockNum=stockNum).select_table(table_name=f'stocktimeinfo_{stockNum}')
    except ProgrammingError:
        return result(code=500, msg="暂未查询到信息，请更新数据！")
    if fetchall is None:
        return result(code=500, msg="暂未查询到信息，请更新数据！")
    return result(kwargs={'data': fetchall})


# 获取日线数据
@api_view(["GET"])
def get_stock_day_bar(request):
    stockNum = request.GET.get('stockNum')
    try:
        fetchall = SQLConn(stockNum=stockNum).select_table(table_name=f'stockdayinfo_{stockNum}')
    except ProgrammingError:
        return result(code=500, msg="暂未查询到信息，请更新数据！")
    if fetchall is None:
        return result(code=500, msg="暂未查询到信息，请更新数据！")
    return result(kwargs={'data': fetchall})


# 获取周线数据
@api_view(["GET"])
def get_stock_week_bar(request):
    stockNum = request.GET.get('stockNum')
    try:
        fetchall = SQLConn(stockNum=stockNum).select_table(table_name=f'stockweekinfo_{stockNum}')
    except ProgrammingError:
        return result(code=500, msg="暂未查询到信息，请更新数据！")
    if fetchall is None:
        return result(code=500, msg="暂未查询到信息，请更新数据！")
    return result(kwargs={'data': fetchall})


# 获取月线数据
@api_view(["GET"])
def get_stock_month_bar(request):
    stockNum = request.GET.get('stockNum')
    try:
        fetchall = SQLConn(stockNum=stockNum).select_table(table_name=f'stockmonthinfo_{stockNum}')
    except ProgrammingError:
        return result(code=500, msg="暂未查询到信息，请更新数据！")
    if fetchall is None:
        return result(code=500, msg="暂未查询到信息，请更新数据！")
    return result(kwargs={'data': fetchall})


# 获取股票新闻数据
@api_view(["GET"])
def stock_get_news_list(request):
    news_list = News.objects.all().order_by('-createTime')[:10]
    if news_list.count() == 0:
        return result(code=500, msg="暂未新闻信息")
    news_list = json.loads(serializers.serialize("json", news_list))
    return result(kwargs={'data': news_list})


# 更新股票新闻数据
@api_view(["GET"])
def stock_update_news_list(request):
    url = 'https://shankapi.ifeng.com/c/api/content/graphic/recommend/getRecommend?callback=getRecommend'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url=url, headers=headers).text[13:-1]
        news_list = json.loads(resp)['data']['data']
    except:
        return result(code=500, msg="更新新闻列表失败！")
    for news in news_list:
        save_news = News(
            createTime=news['createtime'],
            thumbnail=news['thumbnail'],
            pcUrl=news['pcUrl'],
            newsId=news['id'],
            source=news['source'],
            title=news['title'],
            mediaName=news['mediaName'],
            sourceFrom=news['sourceFrom'],
        )
        save_news.save()
    return result(code=200, msg="更新新闻列表成功！")


# 更新单股数据
@api_view(["GET"])
def update_single_stock(request):
    stockNum = request.GET.get('stockNum')
    sql_conn = SQLConn(stockNum)
    sql_conn.create_table()
    res_time = crawlStockTimeInfoList(stockNum)
    sql_conn.insert_time_data(res_time)
    res_day = crawlStockDayInfoList(StockNum=stockNum, klt=101)
    res_week = crawlStockDayInfoList(StockNum=stockNum, klt=102)
    res_month = crawlStockDayInfoList(StockNum=stockNum, klt=103)
    sql_conn.insert_day_data(res_day)
    sql_conn.insert_week_data(res_week)
    sql_conn.insert_month_data(res_month)
    res_bid = update_bid(stockNum)
    if res_time == "error" or res_day == "error" or res_bid == "error":
        return result(code=500, msg="更新失败！")
    return result(msg="更新详细数据成功")


# 爬取bid数据
def update_bid(StockNum):
    url = "http://push2.eastmoney.com/api/qt/stock/get"
    params = {
        'ut': 'fa5fd1943c7b386f172d6893dbfba10b',
        'invt': '2',
        'fltt': '2',
        'fields': 'f43,f57,f58,f169,f170,f46,f44,f51,f168,f47,f164,f163,f116,f60,f45,f52,f50,f48,f167,f117,f71,f161,f49,f530,f135,f136,f137,f138,f139,f141,f142,f144,f145,f147,f148,f140,f143,f146,f149,f55,f62,f162,f92,f173,f104,f105,f84,f85,f183,f184,f185,f186,f187,f188,f189,f190,f191,f192,f107,f111,f86,f177,f78,f110,f262,f263,f264,f267,f268,f250,f251,f252,f253,f254,f255,f256,f257,f258,f266,f269,f270,f271,f273,f274,f275,f127,f199,f128,f193,f196,f194,f195,f197,f80,f280,f281,f282,f284,f285,f286,f287,f292',
        'secid': f'1.{StockNum}',
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url=url, data=params, headers=headers).json()
        resp = resp['data']
    except:
        return "error"

    for key, val in resp.items():
        if val == '-':
            resp[key] = 0
    try:
        get_obj = StockBid.objects.get(stockNum=StockNum)
        get_obj.sellPrice5 = resp['f31']
        get_obj.sellCount5 = resp['f32']
        get_obj.sellPrice4 = resp['f33']
        get_obj.sellCount4 = resp['f34']
        get_obj.sellPrice3 = resp['f35']
        get_obj.sellCount3 = resp['f36']
        get_obj.sellPrice2 = resp['f37']
        get_obj.sellCount2 = resp['f38']
        get_obj.sellPrice1 = resp['f39']
        get_obj.sellCount1 = resp['f40']
        get_obj.boughtPrice1 = resp['f19']
        get_obj.boughtCount1 = resp['f20']
        get_obj.boughtPrice2 = resp['f17']
        get_obj.boughtCount2 = resp['f18']
        get_obj.boughtPrice3 = resp['f15']
        get_obj.boughtCount3 = resp['f16']
        get_obj.boughtPrice4 = resp['f13']
        get_obj.boughtCount4 = resp['f14']
        get_obj.boughtPrice5 = resp['f11']
        get_obj.boughtCount5 = resp['f12']
        get_obj.save()
    except StockBid.DoesNotExist:
        create_stock_bid = StockBid(
            stockNum=StockNum,
            sellPrice5=resp['f31'],
            sellCount5=resp['f32'],
            sellPrice4=resp['f33'],
            sellCount4=resp['f34'],
            sellPrice3=resp['f35'],
            sellCount3=resp['f36'],
            sellPrice2=resp['f37'],
            sellCount2=resp['f38'],
            sellPrice1=resp['f39'],
            sellCount1=resp['f40'],
            boughtPrice1=resp['f19'],
            boughtCount1=resp['f20'],
            boughtPrice2=resp['f17'],
            boughtCount2=resp['f18'],
            boughtPrice3=resp['f15'],
            boughtCount3=resp['f16'],
            boughtPrice4=resp['f13'],
            boughtCount4=resp['f14'],
            boughtPrice5=resp['f11'],
            boughtCount5=resp['f12'],
        )
        create_stock_bid.save()
    return "success"


# 用户个人中心
@api_view(["GET"])
def user_info(request):
    userId = request.session.get("userId")
    info = Sys_user.objects.get(user_id=userId)
    res = {
        'user_id': info.user_id,
        'username': info.username,
        'gender': info.gender,
        'address': info.address,
        'email': info.email,
        'mobile': info.mobile,
        'info': info.info,
        'create_time': info.create_time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    return result(kwargs={'data': res})


# 用户个人中心
@api_view(["POST"])
def user_save(request):
    userId = request.session.get("userId")
    info_obj = Sys_user.objects.get(user_id=userId)
    json_dict = json.loads(request.body)
    # 先获取到用户名和密码，然后需要做几个判断
    info_obj.username = json_dict.get("username", None)
    info_obj.gender = json_dict.get("gender", None)
    info_obj.address = json_dict.get("address", None)
    info_obj.email = json_dict.get("email", None)
    info_obj.mobile = json_dict.get("mobile", None)
    info_obj.info = json_dict.get("info", None)
    try:
        info_obj.save()
        return result()
    except:
        return result(code=500, msg="修改数据异常")
