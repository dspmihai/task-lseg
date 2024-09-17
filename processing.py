import glob
import os
import random
import csv
from datetime import datetime, timedelta


date_format = '%d-%m-%Y'

def str_to_date(s):
    return datetime.strptime(s, date_format)


def date_to_str(d):
    return d.strftime(date_format)


def get_db_tree(db_path):
    if not os.path.exists(db_path):
        raise Exception('Database directory doesn\'t exist.')

    db_tree = {}
    exchange_paths = glob.glob(os.path.join(db_path, '*'))
    for exchange_path in exchange_paths:
        exchange_name = os.path.basename(exchange_path)
        stocks_paths = glob.glob(os.path.join(exchange_path, '*.csv'))
        if len(stocks_paths) == 0:
            continue
        db_tree[exchange_name] = [{'path': path} for path in stocks_paths]
    return db_tree


def prune_exchanges(db, n):
    for exchange in db.keys():
        if n < len(db[exchange]):
            db[exchange] = random.choices(db[exchange], k=n)


def load_stock_slice(stock_path, slice_len):
    with open(stock_path, newline='\n') as csvfile:
        prices = list(csv.reader(csvfile, delimiter=','))
        if len(prices) <= slice_len:
            return None
        else:
            start_slice = random.randint(0, len(prices) - slice_len)
            return prices[start_slice : start_slice + slice_len]


def load(n):
    db = get_db_tree('stock_price_data_files')
    prune_exchanges(db, n)
    for exchange, stocks in db.items():
        for i, stock in enumerate(stocks):
            stock['prices'] = load_stock_slice(stock['path'], 10)
            stock['name'] = os.path.basename(stock['path'])[:-4]
            del stock['path']
    for exchange in list(db.keys()):
        db[exchange] = [stock for stock in db[exchange] if stock['prices'] is not None]
        if len(db[exchange]) == 0:
            del db[exchange]
    return db


def predict_next_3(prices):
    exchange = prices[0][0]
    last_date = str_to_date(prices[-1][1])
    prices = [float(price[2]) for price in prices]
    predictions = [0, 0, 0]
    predictions[0] = sorted(prices)[-2]
    predictions[1] = prices[-1] + (predictions[0] - prices[-1]) / 2
    predictions[2] = predictions[0] + (predictions[1] - predictions[0]) / 4
    return [
        (exchange, date_to_str(last_date + timedelta(days=i+1)), prediction)
        for i, prediction in enumerate(predictions)
    ]


def predict(db):
    for exchange in db.keys():
        for stock in db[exchange]:
            stock['prediction'] = predict_next_3(stock['prices'])
            del stock['prices']
    return db


if __name__ == '__main__':
    from pprint import pprint
    db = load(2)
    pprint(db)
    db = predict(db)
    pprint(db)
