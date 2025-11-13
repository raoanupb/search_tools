"""
Stock Market Research Examples

Demonstrates how to use the stock market search tools for financial research,
including Yahoo Finance, Alpha Vantage, and Financial News.
"""

import os
from datetime import datetime, timedelta


def demo_yahoo_finance():
    """Demonstrate Yahoo Finance search capabilities."""
    print("=" * 80)
    print("YAHOO FINANCE - STOCK MARKET DATA")
    print("=" * 80)

    try:
        from search_tools import YahooFinanceSearch
    except ImportError:
        print("YahooFinanceSearch not available. Install yfinance: pip install yfinance")
        return

    yf = YahooFinanceSearch()

    # Get quote for a stock
    print("\nGetting quote for Apple (AAPL)...")
    quote = yf.get_quote("AAPL")

    print(f"\n{quote['name']} ({quote['symbol']})")
    print(f"Price: ${quote['current_price']}")
    print(f"Change: ${quote['change']} ({quote['change_percent']:+.2f}%)")
    print(f"Volume: {quote['volume']:,}")
    print(f"Market Cap: ${quote['market_cap']:,}")

    # Get company info
    print("\nGetting company information...")
    info = yf.get_company_info("AAPL")

    print(f"\nCompany: {info['name']}")
    print(f"Sector: {info['sector']}")
    print(f"Industry: {info['industry']}")
    print(f"Employees: {info['employees']:,}")
    print(f"P/E Ratio: {info['pe_ratio']}")
    print(f"Dividend Yield: {info['dividend_yield']}")
    print(f"52-Week Range: ${info['52_week_low']} - ${info['52_week_high']}")

    # Get historical data
    print("\nGetting historical data (last 5 trading days)...")
    history = yf.get_historical_data("AAPL", period="5d")

    for day in history:
        print(f"{day['date']}: Open ${day['open']}, Close ${day['close']}, Volume {day['volume']:,}")

    # Compare stocks
    print("\nComparing tech stocks...")
    comparison = yf.compare_stocks(['AAPL', 'MSFT', 'GOOGL'])

    print(f"\n{'Symbol':<10} {'Price':<12} {'Change %':<12} {'P/E Ratio':<12} {'Market Cap':<15}")
    print("-" * 65)
    for stock in comparison:
        market_cap_b = stock['market_cap'] / 1e9 if stock['market_cap'] else 0
        print(f"{stock['symbol']:<10} ${stock['current_price']:<11.2f} "
              f"{stock['change_percent']:>+10.2f}% "
              f"{stock['pe_ratio'] if stock['pe_ratio'] else 'N/A':<12} "
              f"${market_cap_b:.1f}B")


def demo_alpha_vantage():
    """Demonstrate Alpha Vantage search capabilities."""
    print("\n" + "=" * 80)
    print("ALPHA VANTAGE - ADVANCED FINANCIAL DATA")
    print("=" * 80)

    from search_tools import AlphaVantageSearch

    # Check for API key
    api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        print("\n⚠ No Alpha Vantage API key found in environment variable ALPHA_VANTAGE_API_KEY")
        print("Get a free API key at: https://www.alphavantage.co/support/#api-key")
        print("Set it with: export ALPHA_VANTAGE_API_KEY='your-key'")
        return

    av = AlphaVantageSearch(api_key=api_key)

    # Search for symbols
    print("\nSearching for 'Microsoft'...")
    results = av.search_symbols("Microsoft")

    print("\nMatching symbols:")
    for match in results[:5]:
        print(f"  {match['symbol']}: {match['name']} ({match['region']}) - Match: {match['match_score']}")

    # Get quote
    print("\nGetting quote for MSFT...")
    quote = av.get_quote("MSFT")

    print(f"\n{quote['symbol']}")
    print(f"Price: ${quote['price']}")
    print(f"Change: ${quote['change']} ({quote['change_percent']}%)")
    print(f"Volume: {quote['volume']:,}")
    print(f"Latest Trading Day: {quote['latest_trading_day']}")

    # Get company overview
    print("\nGetting company overview...")
    overview = av.get_company_overview("MSFT")

    print(f"\n{overview['name']}")
    print(f"Sector: {overview['sector']}")
    print(f"Industry: {overview['industry']}")
    print(f"Market Cap: ${overview['market_cap']:,}" if overview['market_cap'] else "N/A")
    print(f"P/E Ratio: {overview['pe_ratio']}")
    print(f"EPS: ${overview['eps']}")
    print(f"Profit Margin: {overview['profit_margin']}")
    print(f"ROE: {overview['return_on_equity']}")

    # Get earnings
    print("\nGetting earnings data...")
    earnings = av.get_earnings("MSFT")

    print("\nRecent quarterly earnings:")
    for q in earnings['quarterly'][:4]:
        surprise = q['surprise_percentage']
        surprise_str = f" ({surprise:+.1f}% surprise)" if surprise else ""
        print(f"  {q['fiscal_quarter']}: EPS ${q['reported_eps']}{surprise_str}")

    # Get news sentiment
    print("\nGetting news sentiment...")
    news = av.get_news_sentiment(tickers="MSFT", limit=5)

    print("\nRecent news:")
    for article in news:
        sentiment_emoji = {"Positive": "📈", "Negative": "📉", "Neutral": "➡️"}.get(article['sentiment'], "")
        print(f"\n{sentiment_emoji} {article['title']}")
        print(f"   Source: {article['source']} | Sentiment: {article['sentiment']} ({article['sentiment_score']:.3f})")
        print(f"   Published: {article['time_published']}")


def demo_financial_news():
    """Demonstrate Financial News search capabilities."""
    print("\n" + "=" * 80)
    print("FINANCIAL NEWS SEARCH")
    print("=" * 80)

    from search_tools import FinancialNewsSearch

    # Check for API key
    newsapi_key = os.environ.get('NEWSAPI_KEY')
    if not newsapi_key:
        print("\n⚠ No NewsAPI key found in environment variable NEWSAPI_KEY")
        print("Get a free API key at: https://newsapi.org/register")
        print("Set it with: export NEWSAPI_KEY='your-key'")
        return

    news = FinancialNewsSearch(newsapi_key=newsapi_key)

    # Get top business headlines
    print("\nGetting top business headlines...")
    headlines = news.get_top_headlines(category="business", page_size=5)

    print("\nTop Business Headlines:")
    for i, article in enumerate(headlines, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   Published: {article['published_at']}")

    # Search company news
    print("\nSearching for Apple news (last 7 days)...")
    apple_news = news.search_company_news("Apple Inc", days=7, page_size=5)

    print("\nApple News:")
    for i, article in enumerate(apple_news, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']}")
        print(f"   {article['description'][:100]}...")

    # Search market news
    print("\nSearching for stock market news (last 24 hours)...")
    market_news = news.search_market_news("stock market", days=1, page_size=5)

    print("\nMarket News:")
    for i, article in enumerate(market_news, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']}")

    # Search crypto news
    print("\nSearching for Bitcoin news...")
    crypto_news = news.search_crypto_news("Bitcoin", days=3, page_size=3)

    print("\nCryptocurrency News:")
    for i, article in enumerate(crypto_news, 1):
        print(f"\n{i}. {article['title']}")
        print(f"   Source: {article['source']}")


def demo_stock_analysis():
    """Demonstrate comprehensive stock analysis combining multiple tools."""
    print("\n" + "=" * 80)
    print("COMPREHENSIVE STOCK ANALYSIS")
    print("=" * 80)

    try:
        from search_tools import YahooFinanceSearch, FinancialNewsSearch
    except ImportError as e:
        print(f"Error importing tools: {e}")
        return

    symbol = "TSLA"
    print(f"\nAnalyzing {symbol}...\n")

    # Yahoo Finance data
    print("📊 Market Data (Yahoo Finance)")
    print("-" * 80)

    yf = YahooFinanceSearch()

    quote = yf.get_quote(symbol)
    print(f"Current Price: ${quote['current_price']} ({quote['change_percent']:+.2f}%)")
    print(f"Volume: {quote['volume']:,}")

    info = yf.get_company_info(symbol)
    print(f"P/E Ratio: {info['pe_ratio']}")
    print(f"Market Cap: ${info['market_cap']:,}" if info['market_cap'] else "N/A")
    print(f"Sector: {info['sector']}")

    # Get recommendations
    recs = yf.get_recommendations(symbol)
    if recs:
        print(f"\nLatest Analyst Recommendation:")
        latest = recs[-1]
        print(f"  {latest['date']}: {latest['firm']} - {latest['to_grade']}")

    # News
    newsapi_key = os.environ.get('NEWSAPI_KEY')
    if newsapi_key:
        print(f"\n📰 Recent News")
        print("-" * 80)

        news = FinancialNewsSearch(newsapi_key=newsapi_key)
        company_news = news.search_company_news(symbol, days=3, page_size=3)

        for i, article in enumerate(company_news, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   {article['source']} - {article['published_at'][:10]}")

    # Historical performance
    print(f"\n📈 Recent Performance")
    print("-" * 80)

    history = yf.get_historical_data(symbol, period="5d")
    print(f"\n{'Date':<12} {'Open':<10} {'Close':<10} {'Change':<10}")
    print("-" * 45)

    for day in history:
        change = day['close'] - day['open']
        change_pct = (change / day['open']) * 100
        print(f"{day['date']:<12} ${day['open']:<9.2f} ${day['close']:<9.2f} {change_pct:>+9.2f}%")


def main():
    """Run all stock market demos."""
    print("\n")
    print("*" * 80)
    print("STOCK MARKET RESEARCH TOOLS DEMONSTRATION")
    print("*" * 80)
    print("\nThis script demonstrates stock market research capabilities.")
    print("\nOptional API keys for enhanced functionality:")
    print("  ALPHA_VANTAGE_API_KEY - Get at https://www.alphavantage.co/support/#api-key")
    print("  NEWSAPI_KEY - Get at https://newsapi.org/register")
    print("\n")

    try:
        # Run demos
        demo_yahoo_finance()
        demo_alpha_vantage()
        demo_financial_news()
        demo_stock_analysis()

        print("\n" + "=" * 80)
        print("DEMO COMPLETE")
        print("=" * 80)
        print("\nFor more information, see the README.md file.")

    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
