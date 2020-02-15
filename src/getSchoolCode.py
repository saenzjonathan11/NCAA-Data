
import time
import csv
import requests
from bs4 import BeautifulSoup
import sys


sportCode = "MFB" # football sports code
division = str(11) # 11 is FBS division, 12 is FCB division
# url = "https://stats.ncaa.org/team/inst_team_list?sport_code=" + sportCode + "&division=" + division # correct for this file
url = 'https://stats.ncaa.org/team/inst_team_list?sport_code=MFB&division=11'
#https://stats.ncaa.org/team/inst_team_list?sport_code=MFB&division=12
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
tableColumns = soup.find_all('table', {'width': "100%"})
# print(page.text)
# test = soup.find(id="year_list")
# print(test)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# web driver chrome options
options = Options()
# options.add_argument('--log-level=3')
options.headless = False # true if you don't want page render but runs faster
driver = webdriver.Chrome('chromedriver.exe', options=options)  # Optional argument, if not specified will search path.
driver.get(url)

with open('test3.html', 'wb') as f:
    f.write(driver.page_source.encode('utf-8'))
f.close()

with open("test2.html", 'w') as f:
    f.write(page.text)
f.close()
# with open('../csv/FBS.csv', 'w', newline='') as csvfile:
#   fieldnames = ['schoolID', 'game_sport_year_ctl_id', 'org_id', 'schoolName', 'schoolStatsURL', 'rdStatsURL']
#   writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
#   writer.writerow(fieldnames)
#   i = 0
#   for column in tableColumns:
#     tdTags = column.find_all('td')
#     for tdTag in tdTags:
#       schoolName = tdTag.find('a').text
#       # print(tdTag)
#       schoolStatsURL = "https://stats.ncaa.org" + tdTag.find('a').get('href')
#       urlPathSeg = schoolStatsURL.split('/')
#       teamYearID = urlPathSeg[len(urlPathSeg)-1] 
#       orgID = urlPathSeg[len(urlPathSeg)-2]
#       rdStatsURL = requests.get(schoolStatsURL).url
#       rdPathSeg = rdStatsURL.split('/')
#       schoolID = rdPathSeg[len(rdPathSeg)-1]

#       writer.writerow([schoolID, teamYearID, orgID, schoolName, schoolStatsURL, rdStatsURL])
#       i = i + 1
#       print(i)
#     sys.exit()
# csvfile.close()