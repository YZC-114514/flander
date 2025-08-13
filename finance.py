import yfinance as yf

def get_currency(note1, note2, value):
    try:
        # 确保货币代码为大写（例如 usd -> USD）
        ticker_symbol = f"{note1.upper()}{note2.upper()}=X"
        ticker = yf.Ticker(ticker_symbol)
        
        # 检查货币对是否有效（如果 info 为空，说明货币代码错误）
        if not ticker.info:
            return "错误：无效的货币代码，请输入类似 USD/JPY 的格式"
        
        # 优先从实时信息获取汇率（部分货币对可能没有 currentPrice）
        rate = ticker.info.get('currentPrice')
        
        # 如果实时价格不存在，改用历史数据
        if rate is None:
            historical_data = ticker.history(period="1d")
            if historical_data.empty:
                return "错误：无法获取汇率数据（可能市场未开盘）"
            rate = historical_data["Open"].iloc[0]  # 使用 .iloc[0] 避免索引错误
        
        total = float(value) * rate
        return f"{value} {note1} = {total:.4f} {note2}（汇率: {rate:.4f})"
    
    except Exception as e:
        return f"错误：{str(e)}"


def get_currentprice_stock(stock):
    return yf.Ticker(stock).history(period='1d')





