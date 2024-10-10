import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import json
import config

def logistic_growth(t, r):
    return config.X_M / (1 + (config.X_M/config.X0 - 1) * np.exp(-r * t))

def fit_model():
    # 读取CSV文件
    df = pd.read_csv(config.DATA_FILE, index_col='time', parse_dates=True, encoding='utf-8')
    df['days'] = (df.index - df.index[0]).days
    df = df[df['close'] > 0]
    
    config.X0 = df['close'].iloc[0]

    # 拟合模型
    popt, _ = curve_fit(logistic_growth, df['days'], df['close'], p0=[config.INITIAL_R], bounds=(0, 0.5), maxfev=10000)
    r = popt[0]

    # 更新 config.py 中的 INITIAL_R 值
    config_df = pd.read_csv('config.py', sep='=', names=['key', 'value'], comment='#', encoding='utf-8')
    config_df.loc[config_df['key'].str.strip() == 'INITIAL_R', 'value'] = f" {r:.6f}  # Updated by model_fitting.py"
    config_df.to_csv('config.py', sep='=', index=False, header=False, encoding='utf-8')

    # 生成拟合曲线的数据点
    x_fit = np.linspace(df['days'].min(), df['days'].max(), 1000)
    y_fit = logistic_growth(x_fit, r)

    # 绘制图表
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['close'], label='Actual Data')
    plt.plot(df.index[0] + pd.to_timedelta(x_fit, unit='D'), y_fit, 'r-', label='Fitted Curve')
    plt.title('Bitcoin Closing Price - Logistic Growth Model')
    plt.xlabel('Date')
    plt.ylabel('Closing Price (USD)')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')
    plt.savefig('bitcoin_price_fitted_curve_logistic.png')
    plt.close()

    # 保存参数
    params = pd.DataFrame({
        'parameter': ['X0', 'X_M', 'r', 'last_fit_date'],
        'value': [config.X0, config.X_M, r, df.index[-1].strftime('%Y-%m-%d')]
    })
    params.to_json(config.PARAMS_FILE, orient='records')

    print(f"Model fitted. Parameters saved to {config.PARAMS_FILE}")
    print(f"Estimated growth rate (r): {r:.4f}")
    
    return df

if __name__ == "__main__":
    fit_model()