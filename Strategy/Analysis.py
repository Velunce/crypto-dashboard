import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_drawdowns(prices):
    cumulative_max = prices.cummax()
    drawdowns = (prices - cumulative_max) / cumulative_max
    return drawdowns

def calculate_max_drawdown_2024(df):
    df_2024 = df[df.index.year == 2024]
    drawdowns = calculate_drawdowns(df_2024['close'])
    max_drawdown = drawdowns.min()
    max_drawdown_date = drawdowns.idxmin()
    max_drawdown_price = df_2024.loc[max_drawdown_date, 'close']
    peak_date = df_2024['close'][:max_drawdown_date].idxmax()
    peak_price = df_2024.loc[peak_date, 'close']
    
    return {
        'max_drawdown': max_drawdown,
        'max_drawdown_date': max_drawdown_date,
        'max_drawdown_price': max_drawdown_price,
        'peak_date': peak_date,
        'peak_price': peak_price
    }

def simulate_trading_strategy(df):
    df_2024 = df[df.index.year == 2024]
    
    buy_sell_points = []
    last_peak = df_2024['close'].iloc[0]
    in_position = False
    buy_price = 0

    for date, row in df_2024.iterrows():
        if not in_position:
            if row['close'] <= last_peak * 0.85:
                buy_price = row['close']
                buy_sell_points.append((date, 'Buy', buy_price))
                in_position = True
        else:
            if row['close'] >= buy_price * 1.15:
                sell_price = row['close']
                buy_sell_points.append((date, 'Sell', sell_price))
                in_position = False

        if row['close'] > last_peak:
            last_peak = row['close']

    return buy_sell_points

def analyze_drawdowns_after_buy(df, buy_sell_points):
    drawdown_analysis = []
    for i, (buy_date, action, buy_price) in enumerate(buy_sell_points):
        if action == 'Buy':
            # 找到下一个卖出点或者数据结束
            next_sell_date = df.index[-1]
            if i + 1 < len(buy_sell_points):
                next_sell_date = buy_sell_points[i+1][0]
            
            # 分析这段时间内的价格变动
            period_df = df.loc[buy_date:next_sell_date]
            
            # 计算相对于买入价格的回撤
            drawdowns = (period_df['close'] - buy_price) / buy_price
            max_drawdown = drawdowns.min()
            max_drawdown_date = drawdowns.idxmin()
            max_drawdown_price = period_df.loc[max_drawdown_date, 'close']
            
            drawdown_analysis.append({
                'buy_date': buy_date,
                'buy_price': buy_price,
                'max_drawdown': max_drawdown,
                'max_drawdown_date': max_drawdown_date,
                'max_drawdown_price': max_drawdown_price
            })
    
    return drawdown_analysis

def clean_data(df):
    # 检查并修正异常值
    df['close'] = df[['open', 'high', 'low', 'close']].mean(axis=1)
    
    # 确保 close 价格在当天的最低和最高价之间
    df['close'] = df['close'].clip(lower=df['low'], upper=df['high'])
    
    return df

def calculate_current_drawdown(df):
    # 获取最新日期
    latest_date = df.index.max()
    current_price = df.loc[latest_date, 'close']

    # 从最新日期向前查找峰值
    peak_price = current_price
    peak_date = latest_date
    found_peak = False

    for date, price in df['close'].sort_index(ascending=False).items():
        if price > peak_price:
            peak_price = price
            peak_date = date
        elif found_peak and (peak_price - price) / peak_price <= 0.15:
            # 如果已经找到峰值，且回撤不超过15%，继续寻找
            continue
        elif found_peak:
            # 如果已经找到峰值，且回撤超过15%，停止寻找
            break
        elif (peak_price - price) / peak_price > 0.15:
            # 找到第一个回撤超过15%的点，标记为找到峰值
            found_peak = True

    # 计算回撤
    drawdown = (current_price - peak_price) / peak_price
    
    return {
        'current_date': latest_date,
        'current_price': current_price,
        'peak_date': peak_date,
        'peak_price': peak_price,
        'drawdown': drawdown
    }

def perform_analysis():
    df = pd.read_csv('Strategy/bitcoin_historical_data.csv')
    df['time'] = pd.to_datetime(df['time'])
    df.set_index('time', inplace=True)

    # 数据清洗
    df = clean_data(df)

    # 打印数据的时间范围
    print("\n数据时间范围：")
    print(f"开始日期: {df.index.min()}")
    print(f"结束日期: {df.index.max()}")

    # 打印最后几行数据
    print("\n最后几行数据：")
    print(df.tail())

    # 检查是否有 2024 年的数据
    df_2024 = df[df.index.year == 2024]
    if df_2024.empty:
        print("\n警告：数据集中没有 2024 年的数据")
    else:
        # 如果有 2024 年的数据，继续之前的分析
        max_drawdown_2024 = calculate_max_drawdown_2024(df)
        print("\n2024年最大回撤分析：")
        print(f"最大回撤: {max_drawdown_2024['max_drawdown']:.2%}")
        print(f"最大回撤日期: {max_drawdown_2024['max_drawdown_date'].date()}, 价格: ${max_drawdown_2024['max_drawdown_price']:.2f}")
        print(f"峰值日期: {max_drawdown_2024['peak_date'].date()}, 价格: ${max_drawdown_2024['peak_price']:.2f}")

        buy_sell_points = simulate_trading_strategy(df)
        print("\n2024年交易策略模拟结果：")
        for date, action, price in buy_sell_points:
            print(f"{date.date()}: {action} at ${price:.2f}")

        drawdown_analysis = analyze_drawdowns_after_buy(df, buy_sell_points)
        print("\n买入后的最大浮亏分析：")
        for analysis in drawdown_analysis:
            print(f"买入日期: {analysis['buy_date'].date()}, 买入价格: ${analysis['buy_price']:.2f}")
            print(f"最大浮亏: {analysis['max_drawdown']:.2%}")
            print(f"最大浮亏日期: {analysis['max_drawdown_date'].date()}, 价格: ${analysis['max_drawdown_price']:.2f}")
            print()

    # 计算当前回撤
    current_drawdown = calculate_current_drawdown(df)
    
    print("\n当前价格相对于上一个峰值的回撤：")
    print(f"当前日期: {current_drawdown['current_date'].date()}")
    print(f"当前价格: ${current_drawdown['current_price']:.2f}")
    print(f"上一个峰值日期: {current_drawdown['peak_date'].date()}")
    print(f"上一个峰值价格: ${current_drawdown['peak_price']:.2f}")
    print(f"当前回撤: {current_drawdown['drawdown']:.2%}")

if __name__ == "__main__":
    perform_analysis()