import pandas as pd
from datetime import datetime
import os
import config
from price_prediction import calculate_ahr999
from model_fitting import fit_model
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def ensure_model_params():
    if not os.path.exists(config.PARAMS_FILE):
        print("Model parameters file not found. Running model fitting...")
        fit_model()
        if not os.path.exists(config.PARAMS_FILE):
            raise FileNotFoundError(f"Failed to create {config.PARAMS_FILE}. Please check the model_fitting.py script.")
    else:
        print("Using existing model parameters.")

def main():
    try:
        ensure_model_params()

        # 计算 AHR999
        ahr999, timestamp = calculate_ahr999()

        # 打印结果
        logging.info(f"AHR999: {ahr999:.4f}")
        logging.info(f"Timestamp: {timestamp}")

        # 生成新的数据行
        new_data = pd.DataFrame({
            'Date': [timestamp.date()],
            'Time': [timestamp.time()],
            'AHR999': [ahr999]
        })

        # 如果文件存在，读取现有数据并追加新数据；否则创建新文件
        if os.path.exists(config.AHR999_FILE):
            existing_data = pd.read_csv(config.AHR999_FILE, encoding='utf-8')
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        # 保存更新后的数据
        updated_data.to_csv(config.AHR999_FILE, index=False, encoding='utf-8')

        logging.info(f"AHR999 data appended to {config.AHR999_FILE}")

    except Exception as e:
        logging.error(f"计算AHR999时发生错误: {str(e)}")

if __name__ == "__main__":
    main()