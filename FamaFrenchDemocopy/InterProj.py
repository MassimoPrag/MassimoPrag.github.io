import pandas as pd
import math
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt

"""
Testing the assumptions of the Fama French model and whether they hold true in terms of our dataset
Equaion:

Factors:
F_SMB = small minus big, small caps have higher returns 
F_HML = Companies with higher book to price ratios have higher returns and vice verse 

Our data set:
Columns:  Ticker, Company Name, monthly_return, capm_beta, book_price, CAP, log_mktcap
About 1500 Equities
"""

df = pd.read_csv("cleaned_factset_data.csv") #Load data
df.drop('GPM', axis=1, inplace=True) #Remove GPM which is not a factor in our model
df["CAP"] = df.CAP.astype(float) 
df["log_mktcap"] = np.log(df["CAP"]) #reduce the impact of outliers caused by the few number of large cap companies, add a new column to df called log_mktcap and populate it with the log of each value in CAP.
df.dropna()
print(df)

#calculate the z-score of each of the numeric columns and put the results into new columns with 'zscore_' prepended to each original column name
index = 3
for col in df.columns[3:]:
    zscore_ = []
    mean = np.mean(df[col])
    sd = np.std(df[col])
    for row in df[col]:
        z = (row - mean) / sd
        zscore_.append(z)
    df.insert(index+1, f"zscore_{col}", pd.Series(zscore_))
    index += 2
    #df.insert(df[col]+1, df[f"zscore_{col}"], zscore_)

#Columns: Ticker, Company Name, monthly_return, capm_beta, zscore_capm_beta, book_price, zscore_book_price, CAP, zscore_CAP, log_mktcap, zscore_log_mktcap

"""Winsorize the data in the 'zscore' columns at the 1st and 99th percentiles. 
(Censor the outliers, set any values less than the 1st percentile to the value of the 1st percentile and any values greater than the 99th percentile to the value at the 99th percentile)."""

for col in df.columns[3::2]:
    zcol = f"zscore_{col}"
    df[col] = np.where(df[zcol] > 2.33, df[col].quantile(0.99),
                       np.where(df[zcol] < -2.33, df[col].quantile(0.01), df[col]))
df[zcol] = np.clip(df[zcol], -2.33, 2.33)#cap z columns themselves

df.dropna(inplace=True)
print(df)

# Using Z table, Remove Z > 2.33 or Z < -2.32
# column = np.where(for condition, return value, otherwise return)

"""
Run an ordinary least squares regression** using the standardized, winsorized data as explanatory variables and the monthly returns as the dependent.
"""
x = df[["zscore_capm_beta", "zscore_book_price", "zscore_log_mktcap"]]
y = df["monthly_return"]

x = sm.add_constant(x)
lin = sm.OLS(y,x).fit()

print(lin.summary())

"""
                        coef    std err          t      P>|t|      [0.025      0.975]
-------------------------------------------------------------------------------------
const                -0.8790      0.152     -5.794      0.000      -1.177      -0.581
zscore_capm_beta      0.4126      0.161      2.566      0.010       0.097       0.728
zscore_book_price    -1.4975      0.172     -8.725      0.000      -1.834      -1.161
zscore_log_mktcap    -0.1679      0.165     -1.015      0.310      -0.493       0.157
==============================================================================

Result, here we can see beta weightings for each of the factors just by looking at the coefficient row. 

Next step to usuing the model
Divide our portfolios into different bins
3 bins based on market cap, average monthly return for each, and difference between highest 3rd and lowest third
3 bins based on book to earnings, average monthly return for each, and difference between highest 3rd and lowest third
find market premium

multiply each by their respective betas found above and add together to find

Basically helps find portfolio return based on share of growth and value, high and low. 
"""
