import pandas as pd
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


# Set English font
plt.rcParams['font.sans-serif'] = ['Arial']  # Use Arial font for text
plt.rcParams['axes.unicode_minus'] = False  # Display minus sign correctly

def fetch_historical_data():
    # 使用histoday端点获取每日数据
    url = "https://min-api.cryptocompare.com/data/v2/histoday"
    params = {
        'fsym': 'BTC',  # from symbol
        'tsym': 'USD',  # to symbol
        'allData': 'true'  # request all available data
    }
    
    response = requests.get(url, params=params)
    data = response.json()['Data']['Data']
    
    # 将数据转换为DataFrame
    df = pd.DataFrame(data)
    
    # 将时间戳转换为日期
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # 设置日期为索引
    df.set_index('time', inplace=True)
    
    return df

# 获取数据
df = fetch_historical_data()

# 打印数据范围
print(f"数据范围: 从 {df.index.min()} 到 {df.index.max()}")
print(f"总共 {len(df)} 天的数据")

# 显示前几行数据
print(df.head())

# 保存为CSV文件
csv_filename = 'bitcoin_historical_data.csv'
df.to_csv(csv_filename)
print(f"数据已保存到 {csv_filename}")

# 绘制收盘价走势图
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['close'])
plt.title('Bitcoin Historical Closing Price')
plt.xlabel('Date')
plt.ylabel('Closing Price (USD)')
plt.grid(True)

# 保存图表
plt.savefig('bitcoin_price_chart.png')
print("Price Chart Saved as bitcoin_price_chart.png")

# 显示图表（如果你在支持图形界面的环境中运行）
plt.show()