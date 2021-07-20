import pandas as pd
from math import ceil
import json
import re

# Pandas Way to extract the drop downs from the database    
def getDropDowns(filePath):
    df = pd.read_csv(filePath,encoding="ISO-8859-1")
    # Get All Banks in CSV    
    uniqueBanks = list(df['Company'].unique())
    # Get All Periods in File
    unqiuePeriod = pd.to_datetime(df['Date received']).dt.to_period('Q').unique()
    orderedUnqiuePeriod = list(pd.Series(sorted(unqiuePeriod)).astype('str').values)        
    return uniqueBanks , orderedUnqiuePeriod

# getMeData is a function that uses pandas and gets me the data in JSON format
# from the data file located in data\files folder.
def getMeData(percent,bank,period,filePath):
    
    mapPercent = {'100%':1,'75%':0.75,'50%':0.5,'25%':0.25,'All':1}    
    df = pd.read_csv(filePath,encoding="ISO-8859-1")
    
    df['periods'] =  pd.to_datetime(df['Date received']).dt.to_period('Q')
    rows          = ceil(len(df) * mapPercent[percent])
    temp_df       = df[:rows]
    temp_data     = None

    if bank == 'All':
        if period == 'All':
            temp_data = temp_df['Company'].value_counts()[:10]
        else:
            temp_data = temp_df[temp_df['periods'] == period]['Company'].value_counts()[:10]
    else:
        temp_data = temp_df[temp_df['Company']==bank]
        if period == 'All':
            temp_data = temp_data['Company'].value_counts()
        else:
            temp_data = temp_data[temp_data['periods'] == period]['Company'].value_counts() 

    banks      = list(temp_data.to_dict().keys())
    complaints = list(temp_data.to_dict().values())
    data = json.dumps({
        'banks' : banks,
        'complaints' : complaints
    })
    return data


# Pandas ways to get me world cloud data
# it takes an array of feedback information
# to extract the occurrence of the keyword in the model
def getMeWordCloudData(data):

    ser = pd.Series(data)
    dic = {}
    for line in  ser:
        words = line.split()
        for word in words:
            dic[word] = dic.get(word,0) + 1
    dic_series = pd.Series(dic).sort_values(ascending=False)
    df = pd.DataFrame(dic_series).reset_index().rename({'index':'word',0:'number'},axis=1)
    # Looks up for valid keyword typically in this database its of length more than
    # and equal to 4. Gets me top 100 values    
    df = df[df['word'].apply(len) >= 4].\
                    set_index('word').\
                    squeeze().sort_values(ascending=False)[:120]  
    array = []    
    for i in range(len(df)):
        row = df.iloc[[i]].to_dict()
        for k, v in row.items():
            # another extensive cleansing process to filter out words 
            # that are of no conceren to the management            
            no_list = ['this','that','they','which','XXX','have','should',
                       'with','these','since','being','their','then','there','were']
            if any(x in k for x in no_list) or k=='a' or k=='an':
                continue
            # makes data in a format such that it can be easily
            # processed and charted via jqCloud             
            array.append({'text':k,'weight':v})         
    return array
    
# The Follwoing is my routine to compute Sentiment of each feedback in the model
# this function accepts an array of feebacks in strings
# it returns a new array which contains an array of feedback info along with its Sentiment Type 
# computed.
def computeSentiment(array):
    arrayWithSentiment = []    
    for feedback in array:        
        check = re.findall(r'fraud|theft|stonewall|angry|filing|bad|lie|liar|steal'\
                            +r'|crime|close|stole|sadly|errors|bankrupt|bullied|have not heard|'\
                            +r'hot water|incorrect|horrible|FELONY|misleading|toxic|tricked'\
                            +r'|reprehensible|filed|criminal',feedback,flags=re.IGNORECASE)    
        if check:
            arrayWithSent.append([feedback,'Negative'])            
        else:
            arrayWithSent.append([feedback,'Positive'])
    return arrayWithSentiment
