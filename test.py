from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
from bs4 import BeautifulSoup as bs
import urllib3

with open('data.json','r') as file:
        data = json.load(file)

option = webdriver.ChromeOptions()
# option.add_argument('headless')
driver = webdriver.Chrome(options=option)

driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3419565601&distance=25&f_F=eng&f_I=6%2C4&f_JT=F&f_TPR=r604800&geoId=103366113&keywords=Software%20Engineer%20NOT%20Salesperson%20NOT%20General%20NOT%20General%20Services%20NOT%20General%20NOT%20General&location=Vancouver%2C%20British%20Columbia%2C%20Canada&refresh=true&sortBy=R')
driver.find_element(By.XPATH,'/html/body/div[1]/header/nav/div/a[2]').click()
username = driver.find_element(By.XPATH,'//*[@id="username"]')
username.send_keys(data['username'])
password = driver.find_element(By.XPATH,'//*[@id="password"]')
password.send_keys(data['password'])
time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[3]/button').click()
input('paused')

driver.get("https://www.linkedin.com/jobs/view/3424440617/?eBP=JOB_SEARCH_ORGANIC&recommendedFlavor=SCHOOL_RECRUIT&refId=4ylAE17poRt1GYcP%2BnnzOA%3D%3D&trackingId=c7oaaEhL1ZbTEa4zoPzMCQ%3D%3D&trk=flagship3_search_srp_jobs")

try:
    skills = driver.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[1]/div/div/div[1]/div[2]/ul/div/button').click()
    time.sleep(2)
    ullist = driver.find_elements(By.TAG_NAME,'ul')
    # for ul in ullist:
    #     print(ul.get_attribute('class'))
    #     continue
    
    res =[]
    sklist = ullist[0].find_elements(By.TAG_NAME,'li')
    for skill in sklist:
        res.append(skill.text.replace('\nAdd',''))
    print(res)
    
except:
    quit()
input('finish')


#job-details-skill-match-status-list