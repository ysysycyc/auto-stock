import numpy as np
from scipy.stats import linregress


def format_pure_stock_code(code):
    def format_one(one_code):
        return f'sh{one_code}' if one_code[0] == '6' or one_code == '000001' else f'sz{one_code}'

    if isinstance(code, list):
        return [format_one(item) for item in code]
    return format_one(code)


def check_increase(volume_data):
    """
    判断成交量的拟合曲线是否是增长趋势
    :param volume_data: 成交量数组
    :return:
    """
    volume_data = np.array(volume_data).astype(np.float64)
    x = np.arange(len(volume_data))
    slope, intercept, r_value, p_value, std_err = linregress(x, volume_data)
    return slope > 0


def check_above_by_minutes(sh_stock_price, target_stock_price):
    """
    判断分时曲线是否高于上证指数
    :param sh_stock_price 上证指数分时数组
    :param target_stock_price 需要比对的股票的分时数组
    :return:
    """

    # 找到较短的长度
    min_length = min(len(sh_stock_price), len(target_stock_price))

    # 裁剪数组
    sh_stock_price_trimmed = np.array(sh_stock_price[:min_length]).astype(np.float64)
    target_stock_price_trimmed = np.array(target_stock_price[:min_length]).astype(np.float64)

    # 计算缩放因子
    scale_factor = np.mean(sh_stock_price_trimmed) / np.mean(target_stock_price_trimmed)

    # 对 array2 进行缩放
    target_stock_price_trimmed = target_stock_price_trimmed * scale_factor
    rate = np.sum(target_stock_price_trimmed > sh_stock_price_trimmed) / len(sh_stock_price_trimmed)
    print('rate: ', rate)
    return rate

