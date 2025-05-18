import argparse

from constant import API_PORT, CLIENT_ID, LOCAL_IP
from ib_insync import IB, Stock, util


def retrieve_historical_stock_data(stock, currency, router="SMART"):

    ib = IB()

    ib.connect(LOCAL_IP, API_PORT, clientId=CLIENT_ID)

    contract = Stock(stock, router, currency)
    ib.qualifyContracts(contract)

    bars = ib.reqHistoricalData(
        contract,
        endDateTime="",
        durationStr="2 Y",
        barSizeSetting="1 day",
        whatToShow="TRADES",
        useRTH=False,
        formatDate=1,
    )
    df = util.df(bars)

    ib.disconnect()
    return df


def parse_args():
    # Create the argument parser
    parser = argparse.ArgumentParser(
        description="Example script that accepts stock, router, and currency as arguments."
    )

    # Add arguments
    parser.add_argument(
        "-s", "--stock", required=True, help="Value for stock (required)"
    )
    parser.add_argument(
        "-c", "--currency", required=True, help="Value for currency (required)"
    )
    parser.add_argument(
        "-r",
        "--router",
        default="SMART",
        help="Value for router (optional, default: 'SMART')",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    # Parse the arguments
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    data = retrieve_historical_stock_data(args.stock, args.currency, args.router)
    print(data)

# from ib_insync import *
# import pandas as pd
# import matplotlib.pyplot as plt

# ib = IB()
# ib.connect('127.0.0.1', 7497, clientId=1)

# # 获取 AAPL 合约
# contract = Stock('TSLA', 'SMART', 'USD')
# ib.qualifyContracts(contract)

# # 获取过去两年的每日历史数据
# bars = ib.reqHistoricalData(
#     contract,
#     endDateTime='',
#     durationStr='2 Y',
#     barSizeSetting='1 day',
#     whatToShow='TRADES',
#     useRTH=False,
#     formatDate=1
# )

# # 转换为 DataFrame
# df = util.df(bars)
# df['date'] = pd.to_datetime(df['date'])
# df.set_index('date', inplace=True)
# df['close'] = df['close']
# df['ma30'] = df['close'].rolling(window=30).mean()

# # 模拟定投逻辑（每60天一次）
# portfolio = []
# cash_invested = 0
# shares_held = 0

# for i in range(30, len(df), 60):
#     price = df['close'].iloc[i]
#     ma30 = df['ma30'].iloc[i]
#     date = df.index[i]

#     if pd.isna(ma30):
#         continue

#     ratio = price / ma30
#     if ratio < 0.95:
#         invest = 1000
#     elif ratio <= 1.05:
#         invest = 600
#     else:
#         invest = 300

#     quantity = invest // price
#     total_cost = quantity * price
#     cash_invested += total_cost
#     shares_held += quantity

#     portfolio.append({
#         'date': date,
#         'price': round(price, 2),
#         'ma30': round(ma30, 2),
#         'ratio': round(ratio, 3),
#         'invest': invest,
#         'buy_quantity': quantity,
#         'cost': round(total_cost, 2),
#         'total_cash': round(cash_invested, 2),
#         'total_shares': shares_held
#     })

# ib.disconnect()

# # 转换为 DataFrame
# portfolio_df = pd.DataFrame(portfolio)
# portfolio_df.set_index('date', inplace=True)

# # 最终持仓估值
# final_price = df['close'].iloc[-1]
# market_value = shares_held * final_price
# gain = market_value - cash_invested

# print(f"\n✅ 模拟结束：共投资 ${cash_invested:.2f}，当前市值 ${market_value:.2f}，盈亏 ${gain:.2f}")
# print("\n📋 投资记录预览：")
# print(portfolio_df.tail())

# # 可视化策略表现
# plt.figure(figsize=(10,5))
# plt.plot(df.index, df['close'], label='AAPL Close Price')
# plt.plot(df.index, df['ma30'], label='30-Day MA')
# plt.scatter(portfolio_df.index, portfolio_df['price'], color='red', label='Buy Points')
# plt.title('TSLA Enhanced DCA Strategy (2 Years)')
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()
