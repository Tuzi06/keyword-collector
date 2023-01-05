from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
from bs4 import BeautifulSoup as bs
import urllib3


# # with open('fail.json','r') as file:
# #     data = json.load(file)

# data = 'https://ca.linkedin.com/jobs/view/software-development-engineer-at-microsoft-3388589463?refId=O3PDzC%2FftwITaGhEOf4xxA%3D%3D&trackingId=2zOWXEcJbsGwX2MEmQzz0Q%3D%3D&position=2&pageNum=0&trk=public_jobs_jserp-result_search-card'
# # data ='https://ca.linkedin.com/jobs/view/software-engineer-iwork-at-apple-3280913405?refId=SfAcDSgmNOC5kwFmnfSV%2Bg%3D%3D&trackingId=M9tTCZujIN165m22veStjw%3D%3D&position=3&pageNum=0&trk=public_jobs_jserp-result_search-card'
# option = webdriver.ChromeOptions()
# # option.add_argument('headless')
# driver = webdriver.Chrome(options= option)

# # for i in range(len(data)):
# #     driver.get(data[i])
    
# #     try:
# #         summary = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/div' )
# #         with open('test.txt','w') as file:
# #             file.write(summary.text)
# #         print('pass #',i)
# #         time.sleep(10)

# #     except:
# #         print('failed at %ith html : %s'%(i+1,data[i]))
# #         if input('asdfasd ') =='p':
# #             quit()

# driver.get(data)

# html = urllib3.PoolManager().request('get',data)
# praser = bs(html.data,'html.parser')

# div = praser.find('div',class_= 'show-more-less-html__markup show-more-less-html__markup--clamp-after-5')
# summary = set()
# with open('content.txt','w') as file:
#     file.write(div.prettify())
# for child in div.descendants:
#     content = child.string
#     if content is not None:
#         summary.add((content.get_text()))
# print(summary)


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

page = 2
jobdata= {}
while page<=10:
    joblist = driver.find_element(By.XPATH,'//*[@id="main"]/div/section[1]/div/ul')
    jobs = joblist.find_elements(By.TAG_NAME,'li')
    for job in jobs:
        driver.execute_script('arguments[0].scrollIntoView()',job)
        print(job.get_attribute('id'))
        # continue
        try:
            links = job.find_elements(By.TAG_NAME,'a')
            if(len(links)>0):
                link = links[0].get_attribute('href')
                txt = job.text
                title = txt.split('\n')[0]
                print('title is', title)
        except:
            print('not found')
            continue
        if 'Senior' not in title and 'Sr.' not in title and 'Staff' not in title and 'DevOps' not in title and 'Principal' not in title:
            jobdata[title] = link

    try:
        buttons = driver.find_elements(By.TAG_NAME, 'button')
        for button in buttons:
            if button.get_attribute('aria-label')=='Page '+str(page):
                button.click()
                page+=1
                time.sleep(2)
                break
    except:
        print('broken')
        break
jobdata = json.dumps(jobdata,indent= 4)
with open('./result/joblist.json','w') as file:
    file.write(jobdata)

print(jobdata)
print('finished !!!!!!')

