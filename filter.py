from selenium import webdriver
from selenium. webdriver.common.by import By
import time
import json

Username = 'username2'
Password = 'password2'

def main():
    titles = ['senior','sr.' ,'staff' ,'devops' ,'principal','lead','coop']
    with open('data.json','r') as file:
        data = json.load(file)

    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    driver = webdriver.Chrome(options=option)

    driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3436527035&f_T=340%2C2732&f_TPR=r604800&geoId=100025096&keywords=data%20engineer&sortBy=R')
    driver.find_element(By.XPATH,'/html/body/div[1]/header/nav/div/a[2]').click()
    username = driver.find_element(By.XPATH,'//*[@id="username"]')
    username.send_keys(data[Username])

    password = driver.find_element(By.XPATH,'//*[@id="password"]')
    password.send_keys(data[Password])
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[3]/button').click()
    input('paused')

    page = 2
    jobdata= {}
    jobcount =0
    while page<=10:
        joblist = driver.find_element(By.XPATH,'//*[@id="main"]/div/section[1]/div/ul')
        jobs = joblist.find_elements(By.TAG_NAME,'li')
        for job in jobs:
            driver.execute_script('arguments[0].scrollIntoView()',job)
            # print(job.get_attribute('id'))
            # continue
            try:
                links = job.find_elements(By.TAG_NAME,'a')
                if(len(links)>0):
                    link = links[0].get_attribute('href')
                    txt = job.text
                    title = txt.split('\n')[0]
                    # print('title is', title)
                    jobcount+=1
            except:
                print('not found')
                continue
            if not any([x in title.lower() for x in titles]):
                jobdata[title] = link
        print(jobcount)

        try:
            buttons = driver.find_elements(By.TAG_NAME, 'button')
            found = False
            for button in buttons:
                if button.get_attribute('aria-label')=='Page '+str(page):
                    button.click()
                    print('clicked page ',page)
                    page+=1
                    found = True
                    time.sleep(2)
                    break
            if not found:
               break
        except:
            input('wrong')
            print('broken')
            break
    jobdata = json.dumps(jobdata,indent= 4)
    with open('./result/joblist.json','w') as file:
        file.write(jobdata)

    print('finished !!!!!!')

if __name__ == '__main__':
    main()