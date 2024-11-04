from supplier.easymoney import batch_get_data
from supplier.sina import get_volume
from supplier.tencent import get_by_minutes
from util import *


# 每天2点半开始每隔5分钟查询一次潜力股
# 1.涨幅在3~5之间
# 2.量比大于1
# 3.换手率5-10之间
# 4.流通市值50-200亿
# 5.交易量持续放大
#
# 7.分时图全天位于上证指数上方
def run():
    page_no = 1
    match_result = []
    while True:
        stock_list = batch_get_data(page_no=page_no, page_size=500)
        if stock_list is None:
            print('exit with None')
            break
        print('page_no:', page_no, ',total:', len(stock_list))
        filter_stock_list = stock_list

        # 过滤我能买的股票
        hu_shen_stock_prefix = ["000", "001", "002", "600", "601", "603"]
        filter_stock_list = [stock for stock in filter_stock_list if stock['code'][:3] in hu_shen_stock_prefix]
        print('after filter hu_shen_stock_prefix:', len(filter_stock_list))
        # 涨幅在3~5之间
        filter_stock_list = [stock for stock in filter_stock_list if 3 <= stock['change_percent'] <= 5]
        print('after filter change_percent:', len(filter_stock_list))
        # 量比大于1
        filter_stock_list = [stock for stock in filter_stock_list if stock['volume_rate'] > 1]
        print('after filter volume_rate:', len(filter_stock_list))
        # 换手率5-10之间
        filter_stock_list = [stock for stock in filter_stock_list if 5 <= stock['turnover_rate'] <= 10]
        print('after filter turnover_rate:', len(filter_stock_list))
        # 流通市值50-200亿
        filter_stock_list = [stock for stock in filter_stock_list if
                             50_0000_0000 <= stock['circulation_market_value'] <= 200_0000_0000]
        print('after filter circulation_market_value:', len(filter_stock_list))
        # 交易量持续放大
        volume_stock_list = get_volume([stock['code'] for stock in filter_stock_list])
        stock_volume = [[stock['volume'] for stock in stocks] for stocks in volume_stock_list]
        filter_stock_list = [filter_stock_list[i] for i, v in enumerate(stock_volume) if check_increase(v)]
        print('after filter volume:', len(filter_stock_list))
        if 5 > len(filter_stock_list) > 0:
            print('after filter volume filter_stock_list:', [stock['code'] for stock in filter_stock_list])

        # 分时图全天位于上证指数上方
        sh_stock_price = get_by_minutes('000001')[0]
        stock_price_list = get_by_minutes([stock['code'] for stock in filter_stock_list])
        filter_stock_list = [filter_stock_list[i] for i, v in enumerate(stock_price_list) if
                             check_above_by_minutes(sh_stock_price, v) > 0.6]
        print('after filter k minutes:', filter_stock_list)

        match_result += filter_stock_list

        # 查询到的数据根据涨跌幅排序，如果涨跌幅已经不满足要求，跳出循环
        if stock_list[-1]['change_percent'] < 3:
            break

        page_no += 1

    print('match_result:', match_result)
    return match_result
