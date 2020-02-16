import time
import csv
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import sys

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='../chromedriver.exe', options=chrome_options)

sportCode = "MFB" # football sports code
division = str(12) # 11 is FBS division, 12 is FCB division
url = 'https://stats.ncaa.org/team/inst_team_list?sport_code=MFB&division=11'
#https://stats.ncaa.org/team/inst_team_list?sport_code=MFB&division=12
# url = "https://stats.ncaa.org/team/inst_team_list?sport_code=" + sportCode + "&division=" + division # correct for this file


# data for seasons for football
dates = []
for startYear in range(2019,1800, -1):
  strStartYear = str(startYear)
  last2num = str(startYear % 100 + 1)
  if len(last2num) == 1:
    last2num = '0' + last2num
  dates.append(str(startYear) + '-' + str(last2num))

page = requests.get(url)
soup = BeautifulSoup(page.text, 'lxml')
tableColumns = soup.find_all('table', {'width': "100%"})

# web driver chrome options
options = Options()
options.headless = False # true if you don't want page render but runs faster
driver = webdriver.Chrome('../chromedriver.exe', options=options)  # Optional argument, if not specified will search path.
driver.get(url)

with open('../csv/conferencesWithYears/FCSWithYears.csv', 'w', newline='') as csvfile:
  fieldnames = ['schoolID', 'game_sport_year_ctl_id', 'org_id', 'schoolName', 'schoolStatsURL', 'rdStatsURL'] + dates
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

      driver.get('https://stats.ncaa.org/teams/' + schoolID)
      time.sleep(3)
      optionYears = driver.find_element_by_id('year_list').get_attribute('innerHTML')
      soup = BeautifulSoup(optionYears, 'lxml')
      yearValues = [] 
      yearDates = []

      for option in soup.find_all("option"):
        yearValues.append(int(option['value']))
        yearDates.append(option.text)

      rowData = [schoolID, teamYearID, orgID, schoolName, schoolStatsURL, rdStatsURL] + yearValues
      writer.writerow(rowData)

      i = i + 1
      print(i)
csvfile.close()
print("total teams code scraped: " + str(i))