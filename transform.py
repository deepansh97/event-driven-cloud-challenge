import pandas as pd

def transform_data(dfNYT, dfJH, Loaded_data, max_date ):
    
    dfNYT['date'] = pd.to_datetime(dfNYT['date'],format='%Y-%m-%d')
    dfJH=dfJH[dfJH['Country/Region']=='US'][['Date','Recovered']]
    dfJH['Date'] = pd.to_datetime(dfJH['Date'],format='%Y-%m-%d')
    dfJH.rename(columns={'Date':'date'},inplace=True)
    dfJH['Recovered'] = dfJH['Recovered'].astype('int64')

    if Loaded_data==False:
        dfNYT=dfNYT[dfNYT['date'] > max_date]
        dfJH=dfJH[dfJH['date'] > max_date]
    fdata=pd.merge(dfNYT,dfJH,on='date',how='inner')
    fdata['date'] = pd.to_datetime(fdata['date'],format='%Y-%m-%d')
    return fdata

'''if __name__ =='__main__':
    jh = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')
    nyt = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')
    print(transform_data(nyt,jh, True, None ))'''
