import requests
from util import *

data_dict = {
    1: {'name': '名字', 'key': 'name'},
    2: {'name': '代码', 'key': 'code'},
    3: {'name': '当前价格', 'key': 'current_price'},
    4: {'name': '昨收', 'key': 'close'},
    5: {'name': '今开', 'key': 'open'},
    6: {'name': '成交量', 'key': 'volume'},
    7: {'name': '外盘', 'key': 'outside'},
    8: {'name': '内盘', 'key': 'inside'},
    9: {'name': '买一', 'key': 'bid1'},
    10: {'name': '买一量（手）', 'key': 'bid1_volume'},
    11: {'name': '买二', 'key': 'bid2'},
    12: {'name': '买三', 'key': 'bid3'},
    13: {'name': '买四', 'key': 'bid4'},
    14: {'name': '买五', 'key': 'bid5'},
    15: {'name': '买二量（手）', 'key': 'bid2_volume'},
    16: {'name': '买三量（手）', 'key': 'bid3_volume'},
    17: {'name': '买四量（手）', 'key': 'bid4_volume'},
    18: {'name': '买五量（手）', 'key': 'bid5_volume'},
    19: {'name': '卖一', 'key': 'ask1'},
    20: {'name': '卖一量', 'key': 'ask1_volume'},
    21: {'name': '卖二', 'key': 'ask2'},
    22: {'name': '卖三', 'key': 'ask3'},
    23: {'name': '卖四', 'key': 'ask4'},
    24: {'name': '卖五', 'key': 'ask5'},
    25: {'name': '卖二量', 'key': 'ask2_volume'},
    26: {'name': '卖三量', 'key': 'ask3_volume'},
    27: {'name': '卖四量', 'key': 'ask4_volume'},
    28: {'name': '卖五量', 'key': 'ask5_volume'},
    29: {'name': '最近逐笔成交', 'key': 'recent_trades'},
    30: {'name': '时间', 'key': 'time'},
    31: {'name': '涨跌', 'key': 'change_price'},
    32: {'name': '涨跌%', 'key': 'change_percent'},
    33: {'name': '最高', 'key': 'highest'},
    34: {'name': '最低', 'key': 'lowest'},
    35: {'name': '价格/成交量（手）/成交额', 'key': 'price_volume_amount'},
    36: {'name': '成交量（手）', 'key': 'total_volume'},
    37: {'name': '成交额（万）', 'key': 'total_amount'},
    38: {'name': '换手率', 'key': 'turnover_rate'},
    39: {'name': '市盈率', 'key': 'pe'},
    44: {'name': '流通市值', 'key': 'circulation_market_value'},
    45: {'name': '总市值', 'key': 'market_value'},
    46: {'name': '市净率', 'key': 'pb'},
    47: {'name': '涨停价', 'key': 'limit_up_price'},
    48: {'name': '跌停价', 'key': 'limit_down_price'}
}


def get_by_code(pure_stock_code):
    def transform_data(data, mapping):
        data = data.split(";")
        result = []
        for item in data:
            if not item.strip():
                continue
            item = item.strip()[0:-1].split('~')
            transformed_item = {}
            for key, value in mapping.items():
                transformed_item[value['key']] = item[key]

            result.append(transformed_item)
        return result

    if not isinstance(pure_stock_code, list):
        pure_stock_code = [pure_stock_code]
    stock_code = format_pure_stock_code(pure_stock_code)
    stock_code = ','.join(stock_code)
    response = requests.get(f'https://qt.gtimg.cn/q={stock_code}')
    if response.status_code == 200:
        text = response.text
        return transform_data(text, data_dict)
    else:
        print('Error:', response.status_code, response.text)


def get_by_minutes(pure_stock_code):
    def transform_data(data, s_code):
        data = data['data'][s_code]['data']['data']
        return [item.split(' ')[1] for item in data]

    if not isinstance(pure_stock_code, list):
        pure_stock_code = [pure_stock_code]
    result = []
    stock_code = format_pure_stock_code(pure_stock_code)
    for item in stock_code:
        response = requests.get(f'https://web.ifzq.gtimg.cn/appstock/app/minute/query?code={item}')
        if response.status_code == 200:
            text = response.json()
            print(text)
            result.append(transform_data(text, item))
        else:
            print('Error:', response.status_code, response.text)
    return result
