from decimal import Decimal


def run(my_stock_list, current_stock_list):
    def calculate_change(old_price, new_price):
        cal_change = ((new_price - old_price) / old_price) * 100
        return cal_change

    if len(my_stock_list) > 0:
        return [current_stock_list[0]]

    sell_list = []
    if len(my_stock_list) == 0 or len(current_stock_list) == 0:
        return []

    for my_stock in my_stock_list:
        for current_stock in current_stock_list:
            if my_stock['code'] == current_stock['code']:
                buy_price = Decimal(my_stock['price'])
                current_price = Decimal(current_stock['current_price'])
                change = calculate_change(buy_price, current_price)
                if change > 8:
                    sell_list.append(current_stock)
                    print('sell:', my_stock, 'earn change:', change)
                elif change <= -5:
                    sell_list.append(current_stock)
                    print('sell:', my_stock, 'loss change:', change)

    print('sell list:', sell_list)
    return sell_list
