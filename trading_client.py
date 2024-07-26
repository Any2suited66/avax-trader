from alpaca.trading.client import TradingClient
from api_config import PAPER_ALPACA_KEY, PAPER_ALPACA_SECRET, ALPACA_API_KEY, ALPACA_SECRET


paper_trading_client = TradingClient(api_key=PAPER_ALPACA_KEY, secret_key=PAPER_ALPACA_SECRET, paper=True)

trading_client = TradingClient(api_key=ALPACA_API_KEY, secret_key=ALPACA_SECRET, paper=False)
