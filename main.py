import datetime
from decimal import Decimal
from apscheduler.schedulers.blocking import BlockingScheduler

import pick_stock
import trade_stock
from supplier.tencent import get_by_code


def run_pick_stock():
    pick_result = pick_stock.run()
    if len(pick_result) > 0:
        pick_file_path = 'db/pick_stock.txt'
        with open(pick_file_path, 'r', encoding='utf-8') as file:
            pick_lines = file.readlines()

        pick_log_line = [f'{datetime.date.today()}|{stock["code"]}|{stock["name"]}|{stock["current_price"]}\n' for stock
                         in pick_result]
        pick_log_line += '-' * 50 + '\n'
        pick_lines = pick_log_line + pick_lines
        with open(pick_file_path, 'w', encoding='utf-8') as file:
            file.writelines(pick_lines)

        my_file_path = 'db/my_stock.txt'
        with open(my_file_path, 'r', encoding='utf-8') as file:
            my_lines = file.readlines()
        # 如果不在我的持股中，加入持股
        my_log_line = []
        for stock in pick_result:
            if stock['code'] not in [line.split('|')[1] for line in my_lines]:
                my_log_line += f'{datetime.date.today()}|{stock["code"]}|{stock["name"]}|{stock["current_price"]}\n'
        my_lines = my_log_line + my_lines
        with open(my_file_path, 'w', encoding='utf-8') as file:
            file.writelines(my_lines)


def run_trade_stock():
    my_file_path = 'db/my_stock.txt'
    with open(my_file_path, 'r', encoding='utf-8') as file:
        my_lines = file.readlines()

    my_stock_line = [line.split('|') for line in my_lines]
    my_stock_list = [{'date': line[0], 'code': line[1], 'name': line[2], 'price': Decimal(line[3].strip())}
                     for line in my_stock_line
                     if datetime.datetime.strptime(line[0], '%Y-%m-%d').date() != datetime.date.today()]
    my_stock_code_list = [line['code'] for line in my_stock_list]
    stock_info_list = get_by_code(my_stock_code_list)
    sell_stock_list = trade_stock.run(my_stock_list, stock_info_list)
    if len(sell_stock_list) > 0:
        trade_stock_list = []
        for stock_line in my_stock_list:
            for line in sell_stock_list:
                if stock_line['code'] == line['code']:
                    # 从我的持股中删除，加入交易记录
                    my_stock_list.remove(stock_line)
                    diff_price = Decimal(stock_line['price']) - Decimal(line['current_price'])
                    trade_log = (
                        f'{stock_line["date"]}|{line["code"]}|{line["name"]}|{stock_line["price"]}|{datetime.date.today()}'
                        f'|{line["current_price"]}|{diff_price}\n')
                    trade_stock_list.append(trade_log)

        with open(my_file_path, 'w', encoding='utf-8') as file:
            my_log_list = []
            for my_stock in my_stock_list:
                my_log_list += f'{datetime.date.today()}|{my_stock["code"]}|{my_stock["name"]}|{my_stock["price"]}\n'
            file.writelines(my_log_list)

        trade_file_path = 'db/trade_stock.txt'
        with open(trade_file_path, 'r', encoding='utf-8') as file:
            trade_lines = file.readlines()
        trade_stock_list += '-' * 50 + '\n'
        trade_lines = trade_stock_list + trade_lines
        with open(trade_file_path, 'w', encoding='utf-8') as file:
            file.writelines(trade_lines)


# run_pick_stock()
# run_trade_stock()
scheduler = BlockingScheduler()
scheduler.add_job(run_pick_stock, 'cron', day_of_week='mon-fri', hour=14, minute='30-55')
scheduler.start()
