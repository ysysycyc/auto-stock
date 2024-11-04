import json
from util import *

import requests

data_dict = {
    'volume': {
        'name': '成交量',
        'key': 'volume'
    },
    'high': {
        'name': '最高',
        'key': 'highest'
    },
    'low': {
        'name': '最低',
        'key': 'lowest'
    },
    'open': {
        'name': '今开',
        'key': 'open',
    },
    'close': {
        'name': '昨收',
        'key': 'close'
    },
    'day': {
        'name': '日期',
        'key': 'datetime'
    }
}


# scale: 5, 15, 30, 60 - 时间间隔
def get_volume(pure_stock_code, scale=5, page_size=30):
    def transform_data(data, mapping):
        trans_result = []
        for item in data:
            transformed_item = {}
            for key, value in mapping.items():
                if key in item:
                    transformed_item[value['key']] = item[key]
            trans_result.append(transformed_item)
        return trans_result

    if not isinstance(pure_stock_code, list):
        pure_stock_code = [pure_stock_code]
    stock_code = format_pure_stock_code(pure_stock_code)
    result = []
    for item in stock_code:
        response = requests.get(
            f'https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData'
            f'?symbol={item}&scale={scale}&ma=no&datalen={page_size}')
        if response.status_code == 200:
            text = response.json()
            result.append(transform_data(text, data_dict))
        else:
            print('Error:', response.status_code, response.text)
    return result

