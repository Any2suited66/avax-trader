import asyncio
import csv
import statistics

import pandas
import pandas as pd
from alpaca.data.live import CryptoDataStream
from alpaca.trading.enums import TimeInForce, OrderSide
from alpaca.trading.requests import MarketOrderRequest

from api_config import ALPACA_API_KEY, ALPACA_SECRET
from trading_client import paper_trading_client, trading_client

AVAX_SYMBOL = 'AVAXUSD'
SMA_FIVE_MIN = 10
SMA_TEN_MIN = 20
paper = True

pd.set_option('display.max_columns', 10)


def get_open_paper_positions():
    if paper:
        open_positions = paper_trading_client.get_all_positions()
    else:
        open_positions = trading_client.get_all_positions()
    for open_position in open_positions:
        if open_position.symbol == 'AVAXUSD':
            return float(open_position.qty)
    return 0


def simple_moving_avg(int_list):
    return statistics.mean(int_list)


def market_order(symbol, side):
    market_order_data = MarketOrderRequest(
        symbol=symbol,
        qty=1,
        side=side,
        time_in_force=TimeInForce.GTC
    )
    paper_trading_client.submit_order(order_data=market_order_data)


async def print_trade(t):
    new_row = {'open': t.open, 'close': t.close}
    field_names = ['open', 'close']
    with open('avax_data.csv', 'a') as avax_data:
        dict_object = csv.DictWriter(avax_data, fieldnames=field_names)
        dict_object.writerow(new_row)
        avax_data.close()
    signal_to_buy_or_sell = buy_or_sell()
    #open_positions = get_open_paper_positions()
    if signal_to_buy_or_sell:
        print('buy now!')
        with open('buy_or_sell.txt', 'w') as buy_or_sell_text:
            buy_or_sell_text.write('buy')
        buy_or_sell_text.close()
        #market_order("AVAX/USD", OrderSide.BUY)
    elif not signal_to_buy_or_sell:
        print('sell it all!')
        with open('buy_or_sell.txt', 'w') as buy_or_sell_text:
            buy_or_sell_text.write('sell')
        buy_or_sell_text.close()
        #paper_trading_client.close_all_positions(cancel_orders=True)


def buy_or_sell():
    bars = pandas.read_csv("avax_data.csv")
    if len(bars) > 20:
        last_ten_closes = bars.iloc[-20:, -1:]
        last_5_closes = bars.iloc[-10:, -1:]
        last_ten_closes_list = last_ten_closes.iloc[:, 0].to_list()
        last_five_closes_list = last_5_closes.iloc[:, 0].to_list()
        five_min_sma = simple_moving_avg(last_five_closes_list)
        ten_min_sma = simple_moving_avg(last_ten_closes_list)
        print(five_min_sma, ten_min_sma)
        return five_min_sma > ten_min_sma
    else:
        print("Not enough data, need to wait a few more minutes")
        return False


async def run_stream(trading_stream):
    await trading_stream._run_forever()


async def stream_data():
    stream = CryptoDataStream(ALPACA_API_KEY, ALPACA_SECRET)
    stream.subscribe_bars(print_trade, "AVAX/USD")
    asyncio.create_task(run_stream(stream))
    await asyncio.sleep(5)
    print('Waiting for event...')
    await asyncio.Event().wait()
    print('Event Occurred!')

asyncio.run(stream_data())
