from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

with open('fail.json','r') as file:
    data = json.load(file)

option = webdriver.ChromeOptions()
# option.add_argument('headless')
driver = webdriver.Chrome(options= option)

for i in range(len(data)):
    driver.get(data[i])

    try:
        summary = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/div' )
        # with open('test.txt','w') as file:
        #     file.write(summary.text)
        print('pass #',i)
        time.sleep(5)
        # input('fadfff')
    except:
        print('failed at %ith html : %s'%(i+1,data[i]))
        if input('asdfasd ') =='p':
            quit()

print('finished !!!!!!')

