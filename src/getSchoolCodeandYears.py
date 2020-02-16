import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sys

sportCode = "MFB" # football sports code
division = str(12) # 11 is FBS division, 12 is FCB division
url = "https://stats.ncaa.org/team/inst_team_list?sport_code=" + sportCode + "&division=" + division

# dates for the seasons for football from 2019-20 to 1869-70
dates = []
for startYear in range(2019,1868, -1):
  strStartYear = str(startYear)
  last2num = str(startYear % 100 + 1)
  if len(last2num) == 1:
    last2num = '0' + last2num
  dates.append(str(startYear) + '-' + str(last2num))

# get 3 columns with all teams page url in "division" conference
page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
tableColumns = soup.find_all('table', {'width': "100%"})

# web driver chrome options
options = Options()
options.headless = False # true if you don't want page render but runs faster
driver = webdriver.Chrome('../chromedriver.exe', options=options)  # Optional argument, if not specified will search path.
driver.get(url)

with open('../csv/conferencesWithYears/FCSWithYears.csv', 'w', newline='') as csvfile:
  # add header to csv
  fieldnames = ['schoolID', 'game_sport_year_ctl_id', 'org_id', 'schoolName', 'schoolStatsURL', 'rdStatsURL'] + dates
  writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
  writer.writerow(fieldnames)

  # parse urls and get id value for all the perious seasons for each team
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

      driver.get('https://stats.ncaa.org/teams/' + schoolID)
      time.sleep(2.5)
      optionYears = driver.find_element_by_id('year_list').get_attribute('innerHTML')
      soup = BeautifulSoup(optionYears, 'lxml')
      yearValues = [] 
      yearDates = []

      for option in soup.find_all("option"):
        yearValues.append(int(option['value']))
        yearDates.append(option.text)

      rowData = [schoolID, teamYearID, orgID, schoolName, schoolStatsURL, rdStatsURL] + yearValues
      writer.writerow(rowData)
csvfile.close()
driver.close()