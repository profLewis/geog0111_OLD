import requests
from bs4 import BeautifulSoup
import pandas as pd
'''
Pull data table from http://www.aoml.noaa.gov/hrd/tcfaq/E11.html
on hurricanes in the Atlantic
'''

url = 'http://www.aoml.noaa.gov/hrd/tcfaq/E11.html'
r = requests.get(url)
soup = BeautifulSoup(r.text)
table = soup.find("table")

table_body = table.find('tbody')

rows = table_body.find_all('tr')
data = []
for row in rows:
    cols = row.find_all('td')
    if len(cols) == 5:
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele])
df = pd.DataFrame(data[1:-2],columns=data[0])
df.to_csv('NOAA.csv')
