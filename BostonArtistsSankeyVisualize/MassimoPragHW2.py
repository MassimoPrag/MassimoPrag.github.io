"""
Massimo Prag
DS3500
HW2 MCA Chicago
"""
import pandas as pd
import numpy as np
import math 
import Sank as sk

artists = pd.read_json("artists.json")

#Convert year to decade. v Below v
artists["Decade"] = artists.loc[artists['BeginDate'] % 10 != 0, 'BeginDate'] = artists['BeginDate'] - (artists['BeginDate']%10) # will take all of the 

#clean the data, lowercase, and drop rows with empty data
artists["Gender"] = artists["Gender"].str.lower()
artists["Nationality"] = artists["Nationality"].str.lower()
artists.dropna()

#create our df with nationality, gender and decade
subinfos = artists[["Nationality","Gender","Decade"]] 
subinfos = subinfos[subinfos.Decade != 0]#3

#keep above 
print(subinfos)

#5
sk.make_sankey(subinfos,'Nationality','Decade')
#6
sk.make_sankey(subinfos,'Nationality','Gender')
#7
sk.make_sankey(subinfos,'Gender','Decade')
#8
sk.make_multi_sankey(subinfos,"Nationality", "Gender", "Decade")

