# -*- coding: utf-8 -*-
# *****************************************************************
# Author     : John
# Date       : 2025-04-20
# Description: 获取某股票某日的收盘价，开盘价，成交量
# 需求，打开all.xlsx 获取上海股票代码，遍历获取上一日和当天的收盘价，开盘价，成交量，
# 判断，当天收盘价 大于 上一日的开盘价，且成交量小于上一日的票。
# *****************************************************************
import requests
import pandas as pd
import time
import random
from urllib3.exceptions import ProxyError, MaxRetryError

# --------------- 智能配置中心 ---------------
CONFIG = {
    # 基础配置
    'BASE_URL': 'https://9.push2.eastmoney.com/api/qt/clist/get',
    'MARKET': {'fs': 'm:1', 'name': '上交所'},  # 上交所标识
    'HEADERS_TEMPLATES': [  # 随机User-Agent池
        'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/118.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
    ],
    # 容错配置
    'MAX_RETRIES': 5,
    'RETRY_DELAY': [1, 2, 4, 8, 16],  # 指数退避时间（秒）
    'TIMEOUT': 15,
    'PROXY_ENABLED': False,  # 启用代理（需配置下方PROXIES）
    'PROXIES': {
        # 'http': 'http://user:pass@proxy.com:8080',
        # 'https': 'https://user:pass@proxy.com:8080'
    }
}


def fetch_with_retry(params, attempt=0):
    """智能重试机制（含网络诊断）"""
    if attempt >= CONFIG['MAX_RETRIES']:
        return None

    # 动态生成请求头
    headers = {
        'User-Agent': random.choice(CONFIG['HEADERS_TEMPLATES']),
        'Referer': 'http://quote.eastmoney.com/',
        'Accept-Encoding': 'gzip'
    }

    try:
        print(f"[Attempt {attempt + 1}] 正在请求第{params['pn']}页...")
        response = requests.get(
            CONFIG['BASE_URL'],
            params=params,
            headers=headers,
            proxies=CONFIG['PROXIES'] if CONFIG['PROXY_ENABLED'] else None,
            timeout=CONFIG['TIMEOUT']
        )
        response.raise_for_status()  # 抛出HTTP错误

        data = response.json()
        if data['code'] != 0:
            raise ValueError(f"API错误码：{data['code']}，信息：{data.get('msg', '未知错误')}")

        if data['data']['total'] == 0:
            print("⚠️ 接口返回total=0，可能无数据或权限问题")
            return data

        return data

    except (requests.exceptions.HTTPError, ProxyError, MaxRetryError) as e:
        print(f"❌ 请求失败：{str(e)}")
        time.sleep(CONFIG['RETRY_DELAY'][attempt])
        return fetch_with_retry(params, attempt + 1)
    except Exception as e:
        print(f"❌ 意外错误：{str(e)}")
        return None


def parse_robust(data):
    """数据健壮性解析（含字段校验）"""
    if not data or 'data' not in data:
        return None, "响应数据格式错误"

    meta = data['data']
    if meta.get('diff') is None:
        return None, "缺少关键数据字段'diff'"

    valid_rows = []
    for item in meta['diff']:
        # 基础字段校验
        if not all(key in item for key in ['f12', 'f14', 'f39', 'f41']):
            continue

        # 市盈率有效性检查（排除负值和特殊符号）
        try:
            pe_lyr = float(item['f39']) if item['f39'] != '-' else None
            pe_ttm = float(item['f41']) if item['f41'] != '-' else None
            if pe_lyr is None or pe_ttm is None or pe_lyr <= 0 or pe_ttm <= 0:
                continue
        except ValueError:
            continue

        valid_rows.append({
            '股票代码': item['f12'],
            '股票名称': item['f14'],
            '静态市盈(PE)': pe_lyr,
            '动态市盈(PE_TTM)': pe_ttm
        })

    if not valid_rows:
        return None, "无有效数据（可能所有市盈为负/无效）"
    return pd.DataFrame(valid_rows), None


def diagnose_failure(params, last_response):
    """深度故障诊断"""
    print("\n🚑 进入深度诊断模式：")
    print(f"  1. 最后请求URL：{CONFIG['BASE_URL']}?{requests.compat.urlencode(params)}")

    if last_response:
        print("  2. 响应内容摘要：")
        print(f"     - 状态码：{last_response.status_code}")
        print(f"     - 响应头：{dict(last_response.headers)['Content-Type']}")
        print(f"     - 数据长度：{len(last_response.text)}字节")

        try:
            json_data = last_response.json()
            print(
                f"     - API返回：code={json_data.get('code', 'N/A')}, total={json_data.get('data', {}).get('total', 0)}")
        except:
            print("     - 非JSON响应（可能被反爬拦截）")

    print("\n  3. 建议排查步骤：")
    print("     ▶ 手动验证接口：复制URL到浏览器，检查是否返回数据")
    print("     ▶ 检查市场代码：确保fs=m:1（上交所），fs=m:0为深交所")
    print("     ▶ 启用代理：设置PROXY_ENABLED=True并配置有效代理")
    print("     ▶ 更换ut参数：访问东方财富网页，抓包获取最新ut值")
    print("     ▶ 检查交易时段：非交易日可能无数据（9:30-15:00）")


def main():
    all_stocks = []
    params = CONFIG['MARKET'].copy()
    params.update({
        'pn': 1,
        'pz': 200,
        'fields': 'f12,f14,f39,f41',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281'  # 最新ut值（2025年4月有效）
    })

    last_response = None
    while True:
        data = fetch_with_retry(params)
        last_response = data.response if data else last_response

        if not data:
            diagnose_failure(params, last_response)
            return

        df, err = parse_robust(data)
        if err:
            print(f"⚠️ 数据解析失败：{err}")
            if params['pn'] == 1:  # 首页无数据，终止流程
                diagnose_failure(params, last_response)
                return
            break  # 后续页无数据，视为正常结束

        all_stocks.extend(df.to_dict('records'))
        print(f"✅ 第{params['pn']}页获取{len(df)}条有效数据")

        if params['pn'] * 200 >= data['data']['total']:
            break
        params['pn'] += 1
        time.sleep(random.uniform(0.3, 0.8))  # 随机延迟防反爬

    if all_stocks:
        result = pd.DataFrame(all_stocks).drop_duplicates('股票代码')
        print(f"\n🎉 成功获取{len(result)}只股票：")
        print(result[['股票代码', '股票名称', '静态市盈(PE)', '动态市盈(PE_TTM)']].head())
        return result
    print("❌ 所有页面均无有效数据，可能市场无交易或代码错误")


if __name__ == "__main__":
    main()