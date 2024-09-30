# Yahoo Finance API Component

## Overview

The **Yahoo Finance API** component connects to Yahoo's public API using the Python package `yfinance` and retrieves financial data about companies and their stocks. This component allows you to input a list of stock tickers and receive detailed financial information for each of those tickers.

## Description

This component fetches financial data for a given list of stock tickers from Yahoo Finance. The data retrieved includes various financial indicators and metrics related to the specified stocks.

### Inputs

- **Tickers (List[str])**: A list of strings representing the stock tickers for which you want to retrieve financial data.

### Outputs

- **Output (Dict[str, Dict[str, Any]])**: A dictionary where each key is a ticker string from the input list, and each value is another dictionary containing various financial indicators and their corresponding values for that ticker.

### Input Types

- **Tickers**: LIST - A list of stock ticker symbols (strings).

### Output Type

- **JSON**: The output is in JSON format, mapping each inputted ticker to its corresponding financial data.

## Configuration Parameters

This component does not require any additional configuration parameters.

## Usage

This component is designed to be simple and straightforward to use. You provide a list of stock tickers, and it returns a detailed financial profile for each ticker using data from Yahoo Finance. The financial data includes key indicators and values necessary for financial analysis and decision-making.