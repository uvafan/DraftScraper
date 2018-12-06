from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd

def main():
    df = pd.DataFrame(columns=['Name','Lefty','Majors','Year','Pick'])
    for year in range(1995,2011):
        for roun in range(1,16):
            url = 'http://thebaseballcube.com/draft/research.asp?Q=Y&Y1={}&Y2={}&R={}&R1==&Ovl=&Ovl1==&P=Drafted&Player=&HC=&Status=&Signed=&School=&CTeam=&dteam=&bats=&throws=&CLS=&Bonus=&Bonus2=%3E=&RegionD=&RegionB=&CLev=&STO=%3E=&ST=&dPos=&cPos=&HL2==&HL1=&YA=&Place=&Exp=0&Scout='.format(year,year,roun)
            df = loadPage(url,df,str(year))
    df.to_csv('pitchers.csv',index=False)
    #by drafted position, primary position
    #whether or not they made majors

def loadPage(url,df,year):
    html = urlopen(url)
    soup = BeautifulSoup(html)
    for tr in soup.findAll('tr'):
        data = [td.getText() for td in tr.findAll('td')]
        if data[0] != year or data[21] != 'Yes':
            continue
        dpos = data[8]
        if dpos.split('-')[0] not in {'P','LHP','RHP'}:
            continue
        pick = data[2]
        name = data[5]
        lefty = 1 if data[12].split('-')[1] == 'L' else 0
        majors = 1 if data[13]=='MLB' else 0
        df = df.append({'Name':name,'Lefty':lefty,'Majors':majors,'Year':year,'Pick':pick},ignore_index=True)
    return df

main()
