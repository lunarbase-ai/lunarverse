from unittest.mock import patch, MagicMock
from yahoo_finance import YahooFinanceAPI


class TestYahooFinanceAPI:
    @patch('yahoo_finance.yf.Tickers')
    def test_run(self, mock_tickers):
        mock_ticker_instance = MagicMock()
        mock_tickers.return_value = mock_ticker_instance


        mock_ticker = MagicMock()
        mock_ticker.get_isin.return_value = "mock_isin"
        mock_ticker.get_major_holders.return_value = {"mock_major_holders": "value"}
        mock_ticker.get_mutualfund_holders.return_value = {"mock_mutualfund_holders": "value"}
        mock_ticker.get_insider_purchases.return_value = {"mock_insider_purchases": "value"}
        mock_ticker.get_insider_transactions.return_value = {"mock_insider_transactions": "value"}
        mock_ticker.get_insider_roster_holders.return_value = {"mock_insider_roster_holders": "value"}
        mock_ticker.get_dividends.return_value.tolist.return_value = ["mock_dividends"]
        mock_ticker.get_capital_gains.return_value.tolist.return_value = ["mock_capital_gains"]
        mock_ticker.get_splits.return_value.tolist.return_value = ["mock_splits"]
        mock_ticker.get_actions.return_value.to_dict.return_value = {"mock_actions": "value"}
        mock_ticker.get_shares.return_value = {"mock_shares": "value"}
        mock_ticker.get_info.return_value = {"mock_info": "value"}
        mock_ticker.get_sustainability.return_value = {"mock_sustainability": "value"}
        mock_ticker.get_analyst_price_target.return_value = {"mock_analyst_price_target": "value"}
        mock_ticker.get_rev_forecast.return_value = {"mock_rev_forecast": "value"}
        mock_ticker.get_calendar.return_value = {"mock_calendar": "value"}
        mock_ticker.get_recommendations.return_value = {"mock_recommendations": "value"}
        mock_ticker.get_upgrades_downgrades.return_value.to_dict.return_value = {"mock_upgrades_downgrades": "value"}
        mock_ticker.get_earnings.return_value = {"mock_earnings": "value"}
        mock_ticker.get_income_stmt.return_value.to_dict.return_value = {"mock_income_stmt": "value"}
        mock_ticker.get_balance_sheet.return_value.to_dict.return_value = {"mock_balance_sheet": "value"}
        mock_ticker.get_cash_flow.return_value.to_dict.return_value = {"mock_cash_flow": "value"}
        mock_ticker._download_options.return_value = "mock_options"
        mock_ticker.get_news.return_value = "mock_news"
        mock_ticker.get_trend_details.return_value = {"mock_trend_details": "value"}
        mock_ticker.get_earnings_trend.return_value = {"mock_earnings_trend": "value"}
        mock_ticker.get_earnings_dates.return_value = {"mock_earnings_dates": "value"}
        mock_ticker.get_earnings_forecast.return_value = {"mock_earnings_forecasts": "value"}

        mock_ticker_instance.tickers = {"mock_ticker": mock_ticker}

        api = YahooFinanceAPI()
        result = api.run(["mock_ticker"])

        expected_output = {
            "mock_ticker": {
                "isin": "mock_isin",
                "major_holders": {"mock_major_holders": "value"},
                "mutualfund_holders": {"mock_mutualfund_holders": "value"},
                "insider_purchases": {"mock_insider_purchases": "value"},
                "insider_transactions": {"mock_insider_transactions": "value"},
                "insider_roster_holders": {"mock_insider_roster_holders": "value"},
                "dividends": ["mock_dividends"],
                "capital_gains": ["mock_capital_gains"],
                "splits": ["mock_splits"],
                "actions": {"mock_actions": "value"},
                "shares": {"mock_shares": "value"},
                "info": {"mock_info": "value"},
                "sustainability": {"mock_sustainability": "value"},
                "analyst_price_target": {"mock_analyst_price_target": "value"},
                "rev_forecast": {"mock_rev_forecast": "value"},
                "calendar": {"mock_calendar": "value"},
                "recommendations": {"mock_recommendations": "value"},
                "upgrades_downgrades": {"mock_upgrades_downgrades": "value"},
                "earnings": {"mock_earnings": "value"},
                "income_stmt": {"mock_income_stmt": "value"},
                "balance_sheet": {"mock_balance_sheet": "value"},
                "cash_flow": {"mock_cash_flow": "value"},
                "options": "mock_options",
                "news": "mock_news",
                "trend_details": {"mock_trend_details": "value"},
                "earnings_trend": {"mock_earnings_trend": "value"},
                "earnings_dates": {"mock_earnings_dates": "value"},
                "earnings_forecasts": {"mock_earnings_forecasts": "value"},
            }
        }

        assert result == expected_output