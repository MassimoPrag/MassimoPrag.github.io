import pandas as pd
import plotly.graph_objects as go
import numpy as np

def mapCode(df, src, targ): #df - Source, Target Values
#call to function which stacks collumns and transforms df into standard 2 column data frame
#Map labels in src and targ colums to integers 

    # Get the distinct labels 3df
    df[src] = df[src].astype(str)
    df[targ] = df[targ].astype(str)

    # Get the distinct labels
    label_list = pd.concat([df[src], df[targ]]).unique()

    # Create a label->code mapping
    codes = range(len(label_list))
    lc_map = dict(zip(label_list, codes))

    # Substitute codes for labels in the dataframe
    df = df.replace({src: lc_map, targ: lc_map})

    return df, label_list


def make_sankey(df, src, targ, **kwargs):
    #takes a data frame , souce, and target rows 
    #args is for the stacking 
    threeDF = pd.DataFrame()        
    threeDF  = df.groupby([src, targ]).size().reset_index(name = 'value')
    threeDF.columns = [src,targ,"value"]
    threeDF['value'] = pd.to_numeric(threeDF['value'])
    threeDF = threeDF[threeDF['value'] > 30]

    threeDF, labels = mapCode(threeDF, src, targ)
    link = {'source': threeDF[src], 'target': threeDF[targ], 'value': threeDF["value"]}
    thickness = kwargs.get("thickness", 50) # 50 is the presumed default value
    pad = kwargs.get("pad", 50)


    node = {'label': labels, 'thickness': thickness, 'pad': pad}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()

def make_multi_sankey(df, *args, **kwargs):
    #args is for the stacking 
    threedf = pd.DataFrame()
    #for i in range(len(args)-1):
       # tempdf = df
    for i in range(len(args)-1):
        tempDf = df[[args[i],args[i+1]]]
        tempDf["count"] = 1
        tempDf.columns = ['source','target','count']
        threedf = pd.concat([threedf,tempDf])    
    threedf = threedf.groupby(['source','target']).agg({'count':'sum'}).reset_index()
    threedf = threedf[threedf['count'] > 30]
    threedf, labels = mapCode(threedf, "source", "target")

    link = {'source': threedf['source'], 'target': threedf['target'], 'value': threedf['count']}
    
    thickness = kwargs.get("thickness", 50) # 50 is the presumed default value
    pad = kwargs.get("pad", 50)


    node = {'label': labels, 'thickness': thickness, 'pad': pad}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()



"""
use the map code to convert catagorical data to numerical, then map code is used in make sanky, then use the group by in the sankey to come up with the df of three 
link = {'source': df[src], 'target': df[targ], 'value': values}
instead do link = {'source': df[src], 'target': df[targ], 'value': df[values]}


"""