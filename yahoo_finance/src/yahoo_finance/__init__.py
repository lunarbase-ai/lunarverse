# SPDX-FileCopyrightText: Copyright © 2024 Idiap Research Institute <contact@idiap.ch>
#
# SPDX-FileContributor: Danilo Gusicuma <danilo.gusicuma@idiap.ch>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any, List

from lunarcore.component.lunar_component import LunarComponent
from lunarcore.component.component_group import ComponentGroup
from lunarcore.component.data_types import DataType
import yfinance as yf


class YahooFinanceAPI(
    LunarComponent,
    component_name="Yahoo Finance API",
    component_description="""Connects to Yahoo's public API (using Python package yfinance) and retrieves financial data about companies and their stocks.
    Input (List[str]): A list of strings of the tickers to the stocks to get data about.
    Output (Dict[str,Dict[str, Any]]): A dictionary mapping each inputted ticker (str) to the financial data about the corresponding stock in the form of a dictionary of indicators (str) mapped to their values (Any)""",
    input_types={"tickers": DataType.LIST},
    output_type=DataType.JSON,
    component_group=ComponentGroup.API_TOOLS,
):
    def __init__(self, **kwargs: Any):
        super().__init__(configuration=kwargs)

    def run(self, tickers: List[str]):
        _yf_tickers = yf.Tickers(tickers)
        output = dict()
        for tk_name, tk in _yf_tickers.tickers.items():
            try:
                _isin = tk.get_isin()
            except Exception as e:
                _isin = str(e)

            try:
                _major_holders = tk.get_major_holders(as_dict=True)

            except Exception as e:
                _major_holders = str(e)

            try:
                _mutualfund_holders = tk.get_mutualfund_holders(as_dict=True)
            except Exception as e:
                _mutualfund_holders = str(e)

            try:
                _insider_purchases = tk.get_insider_purchases(as_dict=True)
            except Exception as e:
                _insider_purchases = str(e)

            try:
                _insider_transactions = tk.get_insider_transactions(as_dict=True)
            except Exception as e:
                _insider_transactions = str(e)

            try:
                _insider_roster_holders = tk.get_insider_roster_holders(as_dict=True)
            except Exception as e:
                _insider_roster_holders = str(e)

            try:
                _dividends = tk.get_dividends().tolist()
            except Exception as e:
                _dividends = str(e)

            try:
                _capital_gains = tk.get_capital_gains().tolist()
            except Exception as e:
                _capital_gains = str(e)

            try:
                _splits = tk.get_splits().tolist()
            except Exception as e:
                _splits = str(e)

            try:
                _actions = tk.get_actions()
                _actions.index = _actions.index.map(str)
                _actions.columns = _actions.columns.map(str)
                _actions = _actions.to_dict()
            except Exception as e:
                _actions = str(e)

            try:
                _shares = tk.get_shares(as_dict=True)
            except Exception as e:
                _shares = str(e)

            try:
                _info = tk.get_info()
            except Exception as e:
                _info = str(e)

            try:
                _sustainability = tk.get_sustainability(as_dict=True)
            except Exception as e:
                _sustainability = str(e)

            try:
                _analyst_price_target = tk.get_analyst_price_target(as_dict=True)
            except Exception as e:
                _analyst_price_target = str(e)

            try:
                _rev_forecast = tk.get_rev_forecast(as_dict=True)
            except Exception as e:
                _rev_forecast = str(e)

            try:
                _calendar = tk.get_calendar()
            except Exception as e:
                _calendar = str(e)

            try:
                _recommendations = tk.get_recommendations(as_dict=True)
            except Exception as e:
                _recommendations = str(e)

            try:
                _upgrades_downgrades = tk.get_upgrades_downgrades()
                _upgrades_downgrades.index = _upgrades_downgrades.index.map(str)
                _upgrades_downgrades.columns = _upgrades_downgrades.columns.map(str)
                _upgrades_downgrades = _upgrades_downgrades.to_dict()
            except Exception as e:
                _upgrades_downgrades = str(e)

            try:
                _earnings = tk.get_earnings(as_dict=True)
            except Exception as e:
                _earnings = str(e)

            try:
                _income_stmt = tk.get_income_stmt()
                _income_stmt.index = _income_stmt.index.map(str)
                _income_stmt.columns = _income_stmt.columns.map(str)
                _income_stmt = _income_stmt.to_dict()
            except Exception as e:
                _income_stmt = str(e)

            try:
                _balance_sheet = tk.get_balance_sheet()
                _balance_sheet.index = _balance_sheet.index.map(str)
                _balance_sheet.columns = _balance_sheet.columns.map(str)
                _balance_sheet = _balance_sheet.to_dict()
            except Exception as e:
                _balance_sheet = str(e)

            try:
                _cash_flow = tk.get_cash_flow()
                _cash_flow.index = _cash_flow.index.map(str)
                _cash_flow.columns = _cash_flow.columns.map(str)
                _cash_flow = _cash_flow.to_dict()
            except Exception as e:
                _cash_flow = str(e)

            try:
                _options = tk._download_options()
            except Exception as e:
                _options = str(e)

            try:
                _news = tk.get_news()
            except Exception as e:
                _news = str(e)

            try:
                _trend_details = tk.get_trend_details(as_dict=True)
            except Exception as e:
                _trend_details = str(e)

            try:
                _earnings_trend = tk.get_earnings_trend(as_dict=True)
            except Exception as e:
                _earnings_trend = str(e)

            try:
                _earnings_dates = tk.get_earnings_dates(as_dict=True)
            except Exception as e:
                _earnings_dates = str(e)

            try:
                _earnings_forecasts = tk.get_earnings_forecast(as_dict=True)
            except Exception as e:
                _earnings_forecasts = str(e)

            output[tk_name] = {
                "isin": _isin,
                "major_holders": _major_holders,
                "mutualfund_holders": _mutualfund_holders,
                "insider_purchases": _insider_purchases,
                "insider_transactions": _insider_transactions,
                "insider_roster_holders": _insider_roster_holders,
                "dividends": _dividends,
                "capital_gains": _capital_gains,
                "splits": _splits,
                "actions": _actions,
                "shares": _shares,
                "info": _info,
                "sustainability": _sustainability,
                "analyst_price_target": _analyst_price_target,
                "rev_forecast": _rev_forecast,
                "calendar": _calendar,
                "recommendations": _recommendations,
                "upgrades_downgrades": _upgrades_downgrades,
                "earnings": _earnings,
                "income_stmt": _income_stmt,
                "balance_sheet": _balance_sheet,
                "cash_flow": _cash_flow,
                "options": _options,
                "news": _news,
                "trend_details": _trend_details,
                "earnings_trend": _earnings_trend,
                "earnings_dates": _earnings_dates,
                "earnings_forecasts": _earnings_forecasts,
            }

        return output
