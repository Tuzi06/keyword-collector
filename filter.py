from selenium import webdriver
from selenium. webdriver.common.by import By
import time
import json

def main():
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    driver = webdriver.Chrome(options= option)
    driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3314904279&distance=25&f_TPR=r604800&geoId=103366113&keywords=software%20engineer&sortBy=DD')

    for _ in range(0,10):
       driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
       time.sleep(2)
    print('finish scrolling')
    hreflist = {}
    for i in range(1,175):
        xpath = '//*[@id="main-content"]/section[2]/ul/li[%i]/div/a'%i
        
        try:
            job = driver.find_element(By.XPATH,xpath)
            title = job.text
        except:
            continue

        if 'Senior' not in title and 'Sr.' not in title and 'Staff' not in title and 'DevOps' not in title and 'Principal' not in title:
            hreflist[title] = job.get_attribute('href')

    hreflist = json.dumps(hreflist,indent= 4)
    with open('./result/joblist.json','w') as file:
        file.write(hreflist)

if __name__ == '__main__':
    main()