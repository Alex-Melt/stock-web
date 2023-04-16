# @Time : 2023/4/4 12:55 
# @Author : 赵浩栋
# @File : crawler.py 
# @Software: PyCharm
from urllib.parse import unquote

import requests


def crawlStockTimeInfoList(StockNum):
    url = "http://push2his.eastmoney.com/api/qt/stock/trends2/get"
    params = {
        'fields1': unquote('f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6%2Cf7%2Cf8%2Cf9%2Cf10%2Cf11%2Cf12%2Cf13'),
        'fields2': unquote('f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58'),
        'ut': '7eea3edcaed734bea9cbfc24409ed989',
        'ndays': '1',
        'iscr': '0',
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
    prevClose = resp['prePrice']
    sumPrice = 0
    trends = resp['trends']
    res = []
    for index, trend in enumerate(trends):
        trend = str(trend)
        item = trend.split(',')
        price = float(item[2])
        sumPrice += price
        datetime = item[0]
        date = datetime.split(' ')[0].replace('-', '')
        time = datetime.split(' ')[1].replace(':', '') + '00'
        amount = float(item[6])
        volume = float(item[5])
        upDownRange = (price - prevClose) / prevClose
        avgPrice = sumPrice / (index + 1)
        res.append({
            "date": date,
            # "stockId": "",
            "stockCode": StockNum,
            "price": price,
            "time": time,
            "avgPrice": avgPrice,
            "volume": volume,
            "amount": amount,
            "upDownRange": upDownRange,
        })
    return res


def crawlStockDayInfoList(StockNum, klt):
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        'fields1': unquote('f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6'),
        'fields2': unquote('f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58%2Cf59%2Cf60%2Cf61'),
        'ut': '7eea3edcaed734bea9cbfc24409ed989',
        'klt': klt,
        'fqt': '1',
        'secid': f'1.{StockNum}',
        'beg': '0',
        'end': '20500000',
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    try:
        resp = requests.get(url=url, data=params, headers=headers).json()
        klines = resp['data']['klines']
    except:
        return "error"
    res = []
    for line in klines:
        line = str(line)
        item = line.split(',')
        res.append({
            "date": item[0].replace('-', ''),
            "open": float(item[1]),
            "close": float(item[2]),
            "high": float(item[3]),
            "low": float(item[4]),
            "volume": float(item[5]),
            "amount": float(item[6]),
            "preClose": float(item[2]) - float(item[9]),
        })
    return res


if __name__ == '__main__':
    crawlStockDayInfoList(600000)
