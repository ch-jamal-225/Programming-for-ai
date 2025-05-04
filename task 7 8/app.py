from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your Alpha Vantage API key
API_KEY = '5MJUDM1LQL44BHJ6'

def get_stock_data(symbol):
    """Fetch real-time stock data."""
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    print("API Response:", data)  # Debug: Print API response
    time_series = data.get('Time Series (5min)', {})
    latest_time = next(iter(time_series), None)
    
    if latest_time:
        latest_data = time_series[latest_time]
        return {
            'symbol': symbol,
            'open': latest_data['1. open'],
            'high': latest_data['2. high'],
            'low': latest_data['3. low'],
            'close': latest_data['4. close'],
            'volume': latest_data['5. volume'],
            'last_updated': latest_time
        }
    return None

def get_historical_data(symbol):
    """Fetch historical stock data."""
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json()
    print("Historical API Response:", data)  # Debug: Print historical API response
    time_series = data.get('Time Series (Daily)', {})
    historical_data = []
    
    for date, values in time_series.items():
        historical_data.append({
            'date': date,
            'close': values['4. close']
        })
    
    # Limit to the last 30 days for better chart readability
    return historical_data[:30]

@app.route('/', methods=['GET', 'POST'])
def index():
    stock_data = None
    historical_data = None
    if request.method == 'POST':
        symbol = request.form['symbol']
        print("Symbol Entered:", symbol)  # Debug: Print symbol entered by user
        stock_data = get_stock_data(symbol)
        historical_data = get_historical_data(symbol)
        print("Stock Data:", stock_data)  # Debug: Print stock data
        print("Historical Data:", historical_data)  # Debug: Print historical data
    return render_template('index.html', stock_data=stock_data, historical_data=historical_data)

if __name__ == '__main__':
    app.run(debug=True)