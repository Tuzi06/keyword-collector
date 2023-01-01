from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
from bs4 import BeautifulSoup as bs
import urllib3

# with open('fail.json','r') as file:
#     data = json.load(file)

data = 'https://ca.linkedin.com/jobs/view/software-development-engineer-at-microsoft-3388589463?refId=O3PDzC%2FftwITaGhEOf4xxA%3D%3D&trackingId=2zOWXEcJbsGwX2MEmQzz0Q%3D%3D&position=2&pageNum=0&trk=public_jobs_jserp-result_search-card'
# data ='https://ca.linkedin.com/jobs/view/software-engineer-iwork-at-apple-3280913405?refId=SfAcDSgmNOC5kwFmnfSV%2Bg%3D%3D&trackingId=M9tTCZujIN165m22veStjw%3D%3D&position=3&pageNum=0&trk=public_jobs_jserp-result_search-card'
option = webdriver.ChromeOptions()
# option.add_argument('headless')
driver = webdriver.Chrome(options= option)

# for i in range(len(data)):
#     driver.get(data[i])
    
#     try:
#         summary = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/div' )
#         with open('test.txt','w') as file:
#             file.write(summary.text)
#         print('pass #',i)
#         time.sleep(10)

#     except:
#         print('failed at %ith html : %s'%(i+1,data[i]))
#         if input('asdfasd ') =='p':
#             quit()

driver.get(data)

html = urllib3.PoolManager().request('get',data)
praser = bs(html.data,'html.parser')

div = praser.find('div',class_= 'show-more-less-html__markup show-more-less-html__markup--clamp-after-5')
summary = set()
with open('content.txt','w') as file:
    file.write(div.prettify())
for child in div.descendants:
    content = child.string
    if content is not None:
        summary.add((content.get_text()))
print(summary)
print('finished !!!!!!')

