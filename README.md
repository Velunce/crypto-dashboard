# Crypto Trading Bot

This project is a cryptocurrency trading bot that utilizes the Binance API for data retrieval and trading operations. It implements various strategies, including the AHR999 indicator, for Bitcoin price analysis and potential trading decisions.

## Features

- Connects to Binance API for real-time and historical data
- Retrieves and processes Bitcoin market data
- Implements the AHR999 indicator for market analysis
- Generates price predictions using custom models
- Creates visualizations of Bitcoin price trends
- Supports automated trading strategies (to be implemented)

## Project Structure

- `fetchData.py`: Functions for fetching data from Binance
- `price_prediction.py`: Implements price prediction models and AHR999 calculations
- `fetch_historical_data.py`: Retrieves and processes historical Bitcoin data
- `model_fitting.py`: Fits prediction models to historical data
- `config.py`: Configuration settings for the bot (not tracked in git for security)
- `requirements.txt`: List of project dependencies

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/crypto-trading-bot.git
   cd crypto-trading-bot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Binance API key and secret in a `.env` file:
   ```bash
   BINANCE_API_KEY=your_api_key
   BINANCE_API_SECRET=your_api_secret
   ```

## Usage

1. Fetch historical data:
   ```bash
   python fetch_historical_data.py
   ```

2. Run the price prediction model:
   ```bash
   python price_prediction.py
   ```

3. Fit the model to new data:
   ```bash
   python model_fitting.py
   ```

## Data Visualization

The bot generates price charts and saves them as PNG files for analysis. You can find these in the project directory after running the relevant scripts.

## Configuration

Edit the `config.py` file to adjust bot settings such as trading pairs, intervals, and strategies. Note that this file is not tracked in git to protect sensitive information.

## Dependencies

Main dependencies include:
- python-binance
- python-dotenv
- pandas
- matplotlib
- numpy
- requests

For a full list, see `requirements.txt`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This bot is for educational purposes only. Use at your own risk. Cryptocurrency trading carries a high level of risk and may not be suitable for all investors.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

If you have any questions or suggestions, please open an issue or contact the project maintainer.