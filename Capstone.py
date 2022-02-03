from ast import increment_lineno
import matplotlib
import pandas as pd 
import numpy as np 
import requests 
from bs4 import BeautifulSoup
import matplotlib.pylab as plt 
import datetime


#Get Data From Source 
    #   What players to sample ?
    #   What's the criteria data has to meet to be evaluated 
        #Player Efiienvy before and after All-Star 
        #Limit to games played by at mininum minutes 
        #Use Kevin Durant, Steph Curry, Jrue Holiday, Tim Duncan
years = '' #Can possible do a for loop then set the fucntion of loop to years and see if that will work 
url = f"https://www.basketball-reference.com/players/d/duranke01/gamelog/{years}"

def get_data_to_csv(year):
    url = f"https://www.basketball-reference.com/players/d/duranke01/gamelog/{year}"
    results = requests.get(url)
    stats_08 = pd.read_html(url, header=0)
    data = stats_08[7]
    csv = data.to_csv(f'KDurant{year}.csv', index=False)
    return csv 
get_data_to_csv(2008)
get_data_to_csv(2009)
get_data_to_csv(2010)
get_data_to_csv(2011)

def get_data(year):
    url = f"https://www.basketball-reference.com/players/d/duranke01/gamelog/{year}"
    results = requests.get(url)
    stats_08 = pd.read_html(url, header=0)
    data = stats_08[7]
    data['Date'] = pd.to_datetime(data['Date'], errors='coerce')
    # data['MP'] = pd.DatetimeIndex
    # print(data.dtypes)
    data.drop(columns=['Unnamed: 5', 'Unnamed: 7','Age'], inplace=True)
    #NBA Player Eff == (Pts + Reb + Ast + Stl + Blk - Missed FG - Missed Ft - To) / GP or minutes for single game 
    #FGM * 85.910 + Stl(53.897) + 3PTM(51.757) + FTM (46.845) + Blks(39.190) + OFB(39.19) + Ast(34.677) + DRB(14.707) - F(20.091) - FT_Miss(20.091) - FG_Miss(39.190) - T0(53.897)
    # data['Date'] = pd.to_datetime(data)
    data['FG'] = pd.to_numeric(data['FG'],  errors='coerce')
    data['FGA'] = pd.to_numeric(data['FGA'],  errors='coerce')
    data['3P'] = pd.to_numeric(data['3P'],  errors='coerce')
    data['3PA'] = pd.to_numeric(data['3P'],  errors='coerce')
    data['FT'] = pd.to_numeric(data['FT'], errors='coerce')
    data['FTA'] = pd.to_numeric(data['FTA'], errors='coerce')
    data['TRB'] = pd.to_numeric(data['TRB'], errors='coerce')
    data['AST'] = pd.to_numeric(data['AST'], errors='coerce')
    data['STL'] = pd.to_numeric(data['STL'], errors='coerce')
    data['BLK'] = pd.to_numeric(data['BLK'], errors='coerce')
    data['TOV'] = pd.to_numeric(data['TOV'], errors='coerce')
    data['PTS'] = pd.to_numeric(data['PTS'], errors='coerce')
    data['PF'] =  pd.to_numeric(data['PF'],  errors='coerce')
    data['ORB'] = pd.to_numeric(data['ORB'],  errors='coerce')
    data['DRB'] = pd.to_numeric(data['DRB'],  errors='coerce')
    # # data[['FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PTS', 'PF', 'ORB', 'DRB']] 
    # print(data.dtypes)
    empty_rows = data[data['MP'] == 'MP'].index
    data.drop(empty_rows, inplace=True)
    data.set_index('Rk', drop=True, inplace=True)
    data.drop(columns=['3P%', 'FT%', 'GmSc', 'Tm', 'Opp'], inplace=True)
    #Create a new column within the data of field goals missed and free throws missed 
    FT_Miss = data['FTA'] - data['FT']
    FG_Miss = data['FGA'] - data['FG'] 
    data['FTM'] = FT_Miss
    data['FGM'] = FG_Miss
    return data
print(get_data(2008))
get_data(2009)
get_data(2010)
get_data(2011)
# year = ['2007', '2008', '2009', '2010']
# for x in year:
#     if x == '2007':
#         break=
#     else 

data = get_data(2008)
data09 = get_data(2009)
data10 = get_data(2010)
data11 = get_data(2011)


# #NBA Player Eff == (Pts + Reb + Ast + Stl + Blk - Missed FG - Missed Ft - To) / GP or minutes for single game 
# #FGM * 85.910 + Stl(53.897) + 3PTM(51.757) + FTM (46.845) + Blks(39.190) + OFB(39.19) + Ast(34.677) + DRB(14.707) - F(20.091) - FT_Miss(20.091) - FG_Miss(39.190) - T0(53.897)


EFF = ((((data['FG']*85.910)+ (data['STL']*53.897) + (data['3P']*51.757) + (data['FT']*46.845)+ (data['BLK']*39.190) + (data['ORB']*39.19) + (data['AST']*34.677) + (data['DRB']*14.707)) - ((data['PF']*20.091) - (data['FTM']*20.091) - (data['FGM']*39.190) - (data['TOV']*53.897)))) / 72
raw_eff = ((((data['FG'])+ (data['STL']) + (data['3P']) + (data['FT'])+ (data['BLK']) + (data['ORB']) + (data['AST']) + (data['DRB'])) - ((data['PF']) - (data['FTM']) - (data['FGM']) - (data['TOV']))))/ 72 

#Minutes Control 
less_than_30min = data[data['MP'] < '30:00'].sort_values(['MP'], ascending=True)
more_than_30min = data[data['MP'] > '30:00'].sort_values(['MP'], ascending=True)

#Drop Access Columns Like Percentages 
# data.drop(columns=['3P%', 'FT%', 'GmSc', 'Tm', 'Opp'], inplace=True)
# print(data)

total_stats = {"2007-08":{'FG': '', 'FGA': '', '3P': '', '3PA': '', 'FT': '', 'FTA': '', 'TRB': '', 'AST': '', 'STL': '', 'BLK': '', 'TOV': '', 'PTS': '', 'PF': '', 'ORB': '', 'DRB': ''}, 
               "2008-09":{'FG': '', 'FGA': '', '3P': '', '3PA': '', 'FT': '', 'FTA': '', 'TRB': '', 'AST': '', 'STL': '', 'BLK': '', 'TOV': '', 'PTS': '', 'PF': '', 'ORB': '', 'DRB': ''},
               "2009-10":{'FG': '', 'FGA': '', '3P': '', '3PA': '', 'FT': '', 'FTA': '', 'TRB': '', 'AST': '', 'STL': '', 'BLK': '', 'TOV': '', 'PTS': '', 'PF': '', 'ORB': '', 'DRB': ''},
               "2010-11":{'FG': '', 'FGA': '', '3P': '', '3PA': '', 'FT': '', 'FTA': '', 'TRB': '', 'AST': '', 'STL': '', 'BLK': '', 'TOV': '', 'PTS': '', 'PF': '', 'ORB': '', 'DRB': ''}}
pre = {"2007-08":{'FG': '', 'FGA': '', '3P': '', '3PA': '', 'FT': '', 'FTA': '', 'TRB': '', 'AST': '', 'STL': '', 'BLK': '', 'TOV': '', 'PTS': '', 'PF': '', 'ORB': '', 'DRB': ''},
        "2008-09":{'FG': '', 'FGA': '', '3P': '', '3PA': '', 'FT': '', 'FTA': '', 'TRB': '', 'AST': '', 'STL': '', 'BLK': '', 'TOV': '', 'PTS': '', 'PF': '', 'ORB': '', 'DRB': ''},
        "2009-10":{'FG': '', 'FGA': '', '3P': '', '3PA': '', 'FT': '', 'FTA': '', 'TRB': '', 'AST': '', 'STL': '', 'BLK': '', 'TOV': '', 'PTS': '', 'PF': '', 'ORB': '', 'DRB': ''},
        "2010-11":{'FG': '', 'FGA': '', '3P': '', '3PA': '', 'FT': '', 'FTA': '', 'TRB': '', 'AST': '', 'STL': '', 'BLK': '', 'TOV': '', 'PTS': '', 'PF': '', 'ORB': '', 'DRB': ''}}
post = {"2007-08":{'FG': '', 'FGA': '', '3P': '', '3PA': '', 'FT': '', 'FTA': '', 'TRB': '', 'AST': '', 'STL': '', 'BLK': '', 'TOV': '', 'PTS': '', 'PF': '', 'ORB': '', 'DRB': '' },
        "2008-09":{'FG': '', 'FGA': '', '3P': '', '3PA': '', 'FT': '', 'FTA': '', 'TRB': '', 'AST': '', 'STL': '', 'BLK': '', 'TOV': '', 'PTS': '', 'PF': '', 'ORB': '', 'DRB': ''},
        "2009-10":{'FG': '', 'FGA': '', '3P': '', '3PA': '', 'FT': '', 'FTA': '', 'TRB': '', 'AST': '', 'STL': '', 'BLK': '', 'TOV': '', 'PTS': '', 'PF': '', 'ORB': '', 'DRB': ''},
        "2010-11":{'FG': '', 'FGA': '', '3P': '', '3PA': '', 'FT': '', 'FTA': '', 'TRB': '', 'AST': '', 'STL': '', 'BLK': '', 'TOV': '', 'PTS': '', 'PF': '', 'ORB': '', 'DRB': ''}}
# after = data[data['Date'] > '2008-02-16']
# before = data[data['Date'] < '2008-02-16']

def stat_header(header):
    #header = [] unhasbale s
    for x in data:
        x = data[header].sum()
        total_stats[header] = x
        return f"{header} : {x}"   
        # if time <= data['Date'] > '2008-02-16':
        #     post_all_star = data[data['Date'] > '2008-02-16']
        #     y = post_all_star[header].sum()
        #     post[header].append(y)
        #     return f"{header} : {y}" 
        # elif time >= data['Date'] < '2008-02-16':
        #     pre_allstar_game = data[data['Date'] < '2008-02-16']
        #     z = pre_allstar_game[header].sum()
        #     pre[header].append(z) 
        #     return f"{header} : {z}" 
        # else:
        #     return 'Not Working Properly'
        #This part is considered ambigous, could try numpy to see what it would do 
print(stat_header('FG'))
print(total_stats['FG'])


#Points Before and After The All Star Game
# # Can i create a function that would loop through all the headers and get the sum of those as well 
def header_sum_post(header, algame, season):
    post_all_star = data[data['Date'] > algame]
    post_All_PTS = post_all_star[header].sum()
    post[season][header] = post_All_PTS
    return f"After All Star Break: {post_All_PTS}"
header_sum_post('FG', '2008-02-16', '2007-08')
header_sum_post('FGA', '2008-02-16', '2007-08')
header_sum_post('3P', '2008-02-16', '2007-08')
header_sum_post('FT', '2008-02-16', '2007-08')
header_sum_post('FTA', '2008-02-16', '2007-08')
header_sum_post('TRB', '2008-02-16', '2007-08')
header_sum_post('AST', '2008-02-16', '2007-08')
header_sum_post('STL', '2008-02-16', '2007-08')
header_sum_post('BLK', '2008-02-16', '2007-08')
header_sum_post('TOV', '2008-02-16', '2007-08')
header_sum_post('PTS', '2008-02-16', '2007-08')
header_sum_post('PF', '2008-02-16', '2007-08')
header_sum_post('ORB', '2008-02-16', '2007-08')
header_sum_post('DRB', '2008-02-16', '2007-08')
header_sum_post('3PA', '2008-02-16', '2007-08')
header_sum_post('3PA', '2008-02-16', '2007-08')
print(post['2007-08'])

def player_eff_post(header):
    eff40 = raw_eff * 40 
    data['EFF/40'] = eff40.round(decimals=0)
    data['EFF/40'] = pd.to_numeric(data['EFF/40'], errors='coerce')
    post_all_star = data[data['Date'] > '2008-02-16']
    post_All_PTS = post_all_star[header].mean()
    post[header] = post_All_PTS
    return f"After All Star Break: {post_All_PTS}"
print(player_eff_post('EFF/40'))

def header_sum_pre(header, algame, season):
    pre_allstar_game = data[data['Date'] < '2008-02-16']
    pre_allstar_PTS = pre_allstar_game[header].sum()
    pre[season][header]= pre_allstar_PTS
    return f"Before All Star Break: {pre_allstar_PTS}"
header_sum_pre('FG','2008-02-16', '2007-08')
header_sum_pre('FGA','2008-02-16', '2007-08')
header_sum_pre('3P','2008-02-16','2007-08')
header_sum_pre('FT','2008-02-16', '2007-08')
header_sum_pre('FTA','2008-02-16', '2007-08')
header_sum_pre('TRB','2008-02-16', '2007-08')
header_sum_pre('AST','2008-02-16', '2007-08')
header_sum_pre('STL','2008-02-16', '2007-08')
header_sum_pre('BLK','2008-02-16','2007-08')
header_sum_pre('TOV','2008-02-16','2007-08')
header_sum_pre('PTS','2008-02-16', '2007-08')
header_sum_pre('PF','2008-02-16', '2007-08')
header_sum_pre('ORB','2008-02-16', '2007-08')
header_sum_pre('DRB','2008-02-16','2007-08')
header_sum_pre('3PA','2008-02-16', '2007-08')
header_sum_pre('3PA','2008-02-16', '2007-08')
print(pre['2007-08'])
def player_eff_pre(header): 
    # Create a paramter (date) that will filter multiple charts by hte date of the all star game 
    #Enter the all-star game date in the format allowed, make if statement to prevent wrong input 
    eff40 = raw_eff * 40 
    data['EFF/40'] = eff40.round(decimals=0)
    data['EFF/40'] = pd.to_numeric(data['EFF/40'], errors='coerce')
    pre_allstar_game = data[data['Date'] < '2008-02-16']
    pre_allstar_PTS = pre_allstar_game[header].mean()
    pre[header] = pre_allstar_PTS
    return f"Before All Star Break: {pre_allstar_PTS}"
print(player_eff_pre('EFF/40'))
            # season = ['2007-08', '2008-09', '2009-10']
            # for x in season:
            #     All = x
            #     print(x)

# print(data.describe())
# print(data)
print(f"Player Effiencey: {data['EFF/40'].mean()}")

#NBA Player Eff == (Pts + Reb + Ast + Stl + Blk - Missed FG - Missed Ft - To) / GP or minutes for single game 
#FG * 85.910 + STL(53.897) + 3P(51.757) + FT (46.845) + BLK(39.190) + ORB(39.19) + AST(34.677) + DRB(14.707) - PF(20.091) - FT_Miss(20.091) - FG_Miss(39.190) - T0(53.897)
#ANOTHER CHART COULD BE THE AVG EFFINCENCY PER GAME BEFORE AND AFTER AND TRY TO MAKE REGRESSION MODEL BASED ON THAT 





# data_header = data[['FG', 'FGA', '3P', '3PA', 'FT', 'FTA', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PTS', 'PF', 'ORB', 'DRB']] 
# def try_loop():
#     for x in data_header:
#        print(x)
#Cool site to scrape is statmuse.com



