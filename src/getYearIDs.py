from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import csv
import time

chrome_options = Options()
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content") 
chrome_options.add_argument('--headless')
chrome_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome('../chromedriver.exe', options=chrome_options)
 
driver.get('https://stats.ncaa.org/teams/478092')
time.sleep(3)
optionYears = driver.find_element_by_id('year_list').get_attribute('innerHTML')
soup = BeautifulSoup(optionYears, 'lxml')
yearValues = [] 
yearDates = []
for option in soup.find_all("option"):
  yearValues.append(option['value'])
  yearDates.append(option.text)

with open('../csv/years/test.csv', 'w', newline='') as csvfile:
  writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
  writer.writerow(yearDates)
  writer.writerow(yearValues)

driver.close()