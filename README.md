# StockPrice
Analysis of daily stock price data

## Analysis of stock price data

This code reads in all stock price files from a directory.  Each file in the directory contains daily stock price data from 2007-2017.  The main objective of the code is to read in the data into different structures that can be used for analysis.  In particular, the analysis examines:
	1. The average close, open, high, low, and volume amounts for the stocks over the time period examined.
	2. The most traded stocks on any given day (based on volume amounts)
	3. The dates with the highest trading volume over the 2007-2017 time period of data.
	4. The stock that was the most profitable on the highest trading volume date.
	
The code contained in this repository was designed for usage on a standard windows computer.
	
## Average stock prices and trading volumes over 2007-2017

For the most part the average open, close, high and low values hover around 22-23 dollars over the entire time period.  This indicates that there is a lot of volatility in the stock market making the straight averages of different prices to be relatively similar.  Indeed if we look at the differences between open and closing prices and high and low prices they are both nearly 0.  The average volume traded over the time period is around 1124000.

## Highest volume trading dates

The highest volume trading dates were in 2007 and 2008 during the global financial crises.  This makes sense given there was extensive trading volatility during this time period and people were both selling and buying in the hopes of mitigating losses and buying stocks that were seen as relatively cheaper.  The date with the highest trading volume was January 23, 2008.  The volume traded on this date was 1.6 billion or nearly 1600 times the amount traded on average over the observed time period.

![alt text]([url/images/HighVolumeDays.png] "High Volume")


## Most profitable stocks

During the date with the highest trading volume.  The stock that had the greatest one-day profit was which had a profit gain of 38%.  Even the 10th highest stock had a profit gain of 17%.  algt = allegiant travel; dominion resources = electricity, artw = art way manufacturing, bnt = bon ton stores, bnso = bonso electronics, yt = unknown?, vco = wine producer, avh = avianca holdings (airline industry).  The stocks with the highest growth were surprisingly across a range of sectors and are a combination of domestic and heavily exporting companies.

![alt text]([url/images/HighGrowthStocks.png] "High Growth")

## Future analysis

1. Identify stocks that are best to short during the start of the time period.
2. Identify stocks with the highest after hour trading (e.g. biggest gap between close price on current day, and open price next day)
3. Come up with data to forecast stock prices using outside data.
4. Identify the day to buy a stock given the current price today.
5. Identify average price changes on days with high trading volume.
