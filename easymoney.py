import time

import requests

data_dict = {
    'f2': {
        'name': '最新价',
        'key': 'current_price'
    },
    'f3': {
        'name': '涨跌幅',
        'key': 'change_percent'
    },
    'f4': {
        'name': '涨跌额',
        'key': 'change_price'
    },
    'f5': {
        'name': '成交量',
        'key': 'volume'
    },
    'f6': {
        'name': '成交额',
        'key': 'amount'
    },
    'f7': {
        'name': '振幅',
        'key': 'amplitude'
    },
    'f8': {
        'name': '换手率',
        'key': 'turnover_rate'
    },
    'f9': {
        'name': '市盈率',
        'key': 'pe'
    },
    'f10': {
        'name': '量比',
        'key': 'volume_rate'
    },
    'f11': {
        'name': '5分钟涨跌',
        'key': '5min_change_percent'
    },
    'f12': {
        'name': '代码',
        'key': 'code'
    },
    'f14': {
        'name': '名称',
        'key': 'name'
    },
    'f15': {
        'name': '最高',
        'key': 'highest'
    },
    'f16': {
        'name': '最低',
        'key': 'lowest'
    },
    'f17': {
        'name': '今开',
        'key': 'open',
    },
    'f18': {
        'name': '昨收',
        'key': 'close'
    },
    'f20': {
        'name': '总市值',
        'key': 'market_value'
    },
    'f21': {
        'name': '流通市值',
        'key': 'circulation_market_value'
    },
    'f22': {
        'name': '涨速',
        'key': 'change_speed'
    },
    'f23': {
        'name': '市净率',
        'key': 'pb'
    },
    'f24': {
        'name': '60日涨跌幅',
        'key': '60day_change_percent'
    },
    'f25': {
        'name': '年初至今涨跌幅',
        'key': 'year_change_percent'
    }
}


def batch_get_data(page_no=1, page_size=20):
    def transform_data(data, mapping):
        trans_result = []
        for item in data:
            transformed_item = {}
            for key, value in mapping.items():
                if key in item:
                    transformed_item[value['key']] = item[key]
            trans_result.append(transformed_item)
        return trans_result

    timestamp = int(round(time.time() * 1000))
    response = requests.get('https://70.push2.eastmoney.com/api/qt/clist/get'
                            f'?pn={page_no}'
                            f'&pz={page_size}'
                            '&po=1'  # 1-倒序 0-正序
                            '&np=1'
                            '&ut=bd1d9ddb04089700cf9c27f6f7426281'
                            '&fltt=2'
                            '&invt=2'
                            '&dect=1'
                            '&fid=f3'  # 排序字段
                            '&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23,m:0+t:81+s:2048'
                            '&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11'
                            f'&_={timestamp}')

    if response.status_code == 200:
        result = response.json()
        diff = result['data']['diff']
        return transform_data(diff, data_dict)
    else:
        print('Error:', response.status_code, response.json())
