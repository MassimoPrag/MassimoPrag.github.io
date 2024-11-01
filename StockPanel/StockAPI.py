import pandas as pd
import math
import numpy as np

#This can work for any stock when given a csv including columns open, close, high, love and volume. 
#Our data set for WYNN specifically gives daily values between 2002 and 2024
#StockAPI and StockExplorer are extremply modular and can take info of any stock with same data hence why both files and functions do not include the name WYNN

#Future improvements, use yfinance library or other API and have user imput a ticker
class StockInfos:    

    def __init__(self):
        self.FinalStockInfo = pd.DataFrame()
    
    def loadstock(self, item):
        """
        Loads the stock data into a data frame and converts the strings from 'date' to datetime

        Args:
            self
            item (str): csv file
        
        Returns:
            self.FinalStockInfo = data frame of csv data 
        """
        self.FinalStockInfo = pd.read_csv(item,parse_dates=["date"])
        return self.FinalStockInfo

    def getMA(self, length):
        """
        Creates a new column to FinalStockInfo which calulates the average stock price within a certain length of time also known as moving average. Used to smooth out stock prices. 

        Args:
            self
            item (int): takes an integer whcih we use to choose the length of the moving average
        
        Returns:
            self.FinalStockInfo = now with the moving average of specified length in new column 
        """
        if length > 0:
            self.FinalStockInfo['Moving_Average'] = self.FinalStockInfo['close'].rolling(window=length).mean()
        else:
            raise ValueError("Window length must be an integer greater than 0.")
        return self.FinalStockInfo

    def getVWAP(self):
        """
        Creates a new column to FinalSotckInfo which calculates the volume weighted average price which creates a daily average price and is wieghted by the days volume. 

        Args:
            self
        
        Returns:
            FinalStockInfo = Returns the origional data frame with a VWAP column appended 
        """
        
        typical = (self.FinalStockInfo['high'] + self.FinalStockInfo['low'] + self.FinalStockInfo['close']) / 3
        self.FinalStockInfo['VWAP'] = (typical * self.FinalStockInfo['volume']).cumsum() / self.FinalStockInfo['volume'].cumsum()
        return self.FinalStockInfo
   
    def get_column(self, column_name):
        """
        Gets a column from the FinalStockInfo dataframe. Used to make it easeir to acess values from the dataframe outside of the API file. 

        Args:
            self
            column_name (str): a string of the column name we want the values of. 
        
        Returns:
            FinalStockInfo[column_name] = Returns the column of the values we want. 
        """
        return self.FinalStockInfo[column_name]
    

def main():
    stock = StockInfos()
    stock.loadstock("WYNN_stock_data.csv")
    print(stock.getVWAP())
    #print(stock.getMA(10))


if __name__ == '__main__':
    main()

# Using the special variable 
# __name__

    