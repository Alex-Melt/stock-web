from django.contrib.auth.models import User
from django.db import models, connection


# 用户个人信息表
class Sys_user(models.Model):
    """
    django要求所有的模型必须继承models.Model类
    CharField的max_length参数指定了长度，超过长度的分类名就不能被存入数据库
    """
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=20, verbose_name='用户名')
    password = models.CharField(max_length=20, verbose_name='密码')
    email = models.EmailField(null=True, blank=True, verbose_name='邮箱')
    gender = models.CharField(null=True, blank=True, verbose_name='性别', max_length=10)
    address = models.CharField(null=True, blank=True, verbose_name='居住地', max_length=255)
    mobile = models.CharField(null=True, blank=True, verbose_name="手机号码",max_length=255)
    info = models.TextField(null=True, blank=True, verbose_name="个人简介")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    # 重写str方法，否则当取数据时，取出数据是<QuerySet [<Category: Category onject>]>,不方便阅读
    def __str__(self):
        return self.username


# 用户token表
class Sys_user_token(models.Model):
    user_id = models.IntegerField(primary_key=True)
    token = models.FileField(max_length=255)
    expire_time = models.DateTimeField(verbose_name="过期时间")
    update_time = models.DateTimeField(verbose_name="更新时间")


# 导航栏显示的列表
class Sys_menu(models.Model):
    menu_id = models.IntegerField(primary_key=True)
    parent_id = models.IntegerField(null=True, blank=True, verbose_name="父菜单ID")
    name = models.CharField(null=True, blank=True, max_length=30, verbose_name='菜单名称')
    url = models.CharField(null=True, blank=True, max_length=200, verbose_name='菜单URL')
    perms = models.CharField(null=True, blank=True, max_length=200, verbose_name='授权(多个用逗号隔开，如：user:list)')
    type = models.IntegerField(null=True, blank=True, verbose_name="类型 0:目录 1:菜单 ")
    icon = models.CharField(null=True, blank=True, max_length=30, verbose_name='菜单图标')
    order_num = models.IntegerField(null=True, blank=True, verbose_name="排序 ")


# 股票列表数据
class Stock(models.Model):
    stockId = models.BigAutoField(primary_key=True)
    amount = models.FloatField(null=True, blank=True)
    amplitude = models.FloatField(null=True, blank=True, verbose_name="振幅")
    close = models.FloatField(null=True, blank=True)
    flowMarketValue = models.FloatField(null=True, blank=True)
    high = models.FloatField(null=True, blank=True)
    listingDate = models.CharField(max_length=255, null=True, blank=True, verbose_name="上市时间")
    low = models.FloatField(null=True, blank=True)
    open = models.FloatField(null=True, blank=True)
    preClose = models.FloatField(null=True, blank=True)
    stockName = models.CharField(max_length=255, null=True, blank=True, verbose_name="股票名称")
    stockNum = models.CharField(max_length=255, null=True, blank=True, verbose_name="股票编号")
    totalFlowShares = models.FloatField(null=True, blank=True, verbose_name="流通股本")
    totalMarketValue = models.FloatField(null=True, blank=True)
    totalShares = models.FloatField(null=True, blank=True)
    turnOverrate = models.FloatField(null=True, blank=True, verbose_name="换手率")
    upDownPrices = models.FloatField(null=True, blank=True, verbose_name="涨跌额")
    upDownRange = models.FloatField(null=True, blank=True, verbose_name="单日涨跌幅")
    upDownRange3 = models.FloatField(null=True, blank=True, verbose_name="3日涨跌幅")
    upDownRange5 = models.FloatField(null=True, blank=True, verbose_name="5日涨跌幅")
    updateDate = models.CharField(max_length=255, null=True, blank=True)
    volume = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['stockId']

    # @staticmethod
    # def is_exists(table_name):
    #     return table_name in connection.introspection.table_names()


# 上证指数
class ShStock(models.Model):
    shstockId = models.BigAutoField(primary_key=True)
    INDEX_ABBR = models.CharField(null=True, blank=True, verbose_name="指数名称", max_length=255)
    TOTAL_VALUE = models.CharField(null=True, blank=True, verbose_name="", max_length=255)
    AVG_PRICE = models.CharField(null=True, blank=True, verbose_name="", max_length=255)
    TRADE_AMT = models.CharField(null=True, blank=True, verbose_name="成交额(亿元)", max_length=255)
    VALUE_RATIO = models.CharField(null=True, blank=True, verbose_name="", max_length=255)
    INDEX_CODE = models.CharField(null=True, blank=True, verbose_name="指数代码", max_length=255)
    CLOSE_POINT = models.CharField(null=True, blank=True, verbose_name="收盘", max_length=255)
    KIND_NUM = models.CharField(null=True, blank=True, verbose_name="", max_length=255)
    TRADE_DATE = models.CharField(null=True, blank=True, verbose_name="追踪时间", max_length=255)
    RANK = models.CharField(null=True, blank=True, verbose_name="", max_length=255)
    PE_RATIO = models.CharField(null=True, blank=True, verbose_name="静态市盈率", max_length=255)
    AVG_VOL = models.CharField(null=True, blank=True, verbose_name="平均股本(亿股)", max_length=255)


# 交易数据
class StockBid(models.Model):
    stockBidId = models.AutoField(primary_key=True)
    boughtCount1 = models.IntegerField(null=True, blank=True, verbose_name="", )
    boughtCount2 = models.IntegerField(null=True, blank=True, verbose_name="", )
    boughtCount3 = models.IntegerField(null=True, blank=True, verbose_name="", )
    boughtCount4 = models.IntegerField(null=True, blank=True, verbose_name="", )
    boughtCount5 = models.IntegerField(null=True, blank=True, verbose_name="", )
    boughtPrice1 = models.FloatField(null=True, blank=True, verbose_name="", )
    boughtPrice2 = models.FloatField(null=True, blank=True, verbose_name="", )
    boughtPrice3 = models.FloatField(null=True, blank=True, verbose_name="", )
    boughtPrice4 = models.FloatField(null=True, blank=True, verbose_name="", )
    boughtPrice5 = models.FloatField(null=True, blank=True, verbose_name="", )
    date = models.CharField(null=True, blank=True, verbose_name="", max_length=255)
    sellCount1 = models.IntegerField(null=True, blank=True, verbose_name="", )
    sellCount2 = models.IntegerField(null=True, blank=True, verbose_name="", )
    sellCount3 = models.IntegerField(null=True, blank=True, verbose_name="", )
    sellCount4 = models.IntegerField(null=True, blank=True, verbose_name="", )
    sellCount5 = models.IntegerField(null=True, blank=True, verbose_name="", )
    sellPrice1 = models.FloatField(null=True, blank=True, verbose_name="", )
    sellPrice2 = models.FloatField(null=True, blank=True, verbose_name="", )
    sellPrice3 = models.FloatField(null=True, blank=True, verbose_name="", )
    sellPrice4 = models.FloatField(null=True, blank=True, verbose_name="", )
    sellPrice5 = models.FloatField(null=True, blank=True, verbose_name="", )
    stockNum = models.CharField(null=True, blank=True, verbose_name="", max_length=255)
    time = models.CharField(null=True, blank=True, verbose_name="", max_length=255)


# 新闻数据
class News(models.Model):
    id = models.AutoField(primary_key=True)
    newsId = models.CharField(null=True, blank=True, max_length=255, verbose_name="")
    createTime = models.CharField(null=True, blank=True, max_length=255, verbose_name="")
    thumbnail = models.CharField(null=True, blank=True, max_length=255, verbose_name="")
    pcUrl = models.CharField(null=True, blank=True, max_length=255, verbose_name="")
    source = models.CharField(null=True, blank=True, max_length=255, verbose_name="")
    title = models.CharField(null=True, blank=True, max_length=255, verbose_name="")
    mediaName = models.CharField(null=True, blank=True, max_length=255, verbose_name="")
    sourceFrom = models.CharField(null=True, blank=True, max_length=255, verbose_name="")

# 单股时间数据
# class SingleTimeStock(models.Model):
#     timeInfoId = models.AutoField(primary_key=True)
#     date = models.DateField(null=True, blank=True)
#     stockId = models.IntegerField(null=True, blank=True)
#     stockCode = models.CharField(null=True, blank=True, max_length=255)
#     price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=3)
#     time = models.TimeField(null=True, blank=True)
#     avgPrice = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=3)
#     volume = models.DecimalField(null=True, blank=True, max_digits=15, decimal_places=0)
#     amount = models.DecimalField(null=True, blank=True, max_digits=15, decimal_places=0)
#     upDownRange = models.DecimalField(null=True, blank=True, max_digits=5, decimal_places=4)
