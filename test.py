import yfinance as yf
import ta
import warnings
warnings.filterwarnings('ignore')

stock = yf.Ticker("RELIANCE.NS")
data = stock.history(period="6mo")

data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()
data['DMA_200'] = data['Close'].rolling(window=200).mean()

latest = data.iloc[-1]
print(f"Reliance Price : {latest['Close']:.2f}")
print(f"RSI            : {latest['RSI']:.2f}")
print(f"200 DMA        : {latest['DMA_200']:.2f}")
print("Data working perfectly!")