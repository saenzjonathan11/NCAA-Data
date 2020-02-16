import time
import csv
import requests
from bs4 import BeautifulSoup
import sys

sportCode = "MFB" # football sports code
division = str(11) # 11 is FBS division, 12 is FCB division
url = 'https://stats.ncaa.org/team/inst_team_list?sport_code=MFB&division=11'
#https://stats.ncaa.org/team/inst_team_list?sport_code=MFB&division=12
# url = "https://stats.ncaa.org/team/inst_team_list?sport_code=" + sportCode + "&division=" + division # correct for this file
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
tableColumns = soup.find_all('table', {'width': "100%"})

with open('../csv/conferences/FBS.csv', 'w', newline='') as csvfile:
  fieldnames = ['schoolID', 'game_sport_year_ctl_id', 'org_id', 'schoolName', 'schoolStatsURL', 'rdStatsURL']
  writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
  writer.writerow(fieldnames)
  i = 0
  for column in tableColumns:
    tdTags = column.find_all('td')
    for tdTag in tdTags:
      schoolName = tdTag.find('a').text
      schoolStatsURL = "https://stats.ncaa.org" + tdTag.find('a').get('href')
      urlPathSeg = schoolStatsURL.split('/')
      teamYearID = urlPathSeg[len(urlPathSeg)-1] 
      orgID = urlPathSeg[len(urlPathSeg)-2]
      rdStatsURL = requests.get(schoolStatsURL).url
      rdPathSeg = rdStatsURL.split('/')
      schoolID = rdPathSeg[len(rdPathSeg)-1]

      writer.writerow([schoolID, teamYearID, orgID, schoolName, schoolStatsURL, rdStatsURL])
      i = i + 1
    sys.exit()
csvfile.close()
print("total teams code scraped: " + str(i))