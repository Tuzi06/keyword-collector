from selenium import webdriver
from selenium. webdriver.common.by import By
import time
import threading
import json

website = 'https://www.linkedin.com/jobs/search/?currentJobId=3362372256&f_TPR=r604800&geoId=103366113&keywords=Software%20Engineer&location=Vancouver%2C%20British%20Columbia%2C%20Canada&refresh=true'

def count(summary:str,wordbank:dict):
    wordlist = summary.replace('\n', ' ').split(' ')
    for word in wordlist:
        if word not in wordbank:
            wordbank[word]=1
        else:
            wordbank[word]+=1

def main():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    # option.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options= option)
    driver.get(website)

    # for _ in range(0,10):
    #    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #    time.sleep(2)
    # print('finish scrolling')

    hreflist = []
    wordbank = {}
    for i in range(1,26):
        xpath = '//*[@id="main-content"]/section[2]/ul/li[%i]/div/a'%i
        # print(xpath)
        job = driver.find_element(By.XPATH,xpath)
        hreflist.append(job.get_attribute('href'))
    # print(len(hreflist))
    # quit()    
    threads = []
    detail = webdriver.Chrome(options= option)
    i = 0
    faillist = []
    for href in hreflist:
        detail.get(href)
        try:
            try:
                summary = detail.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[4]/article/div').text
            except:
                summary = detail.find_element(By.XPATH,'/html/body/div[5]/div[3]/div/div[1]/div[1]/div/div[2]/article/div').text
        except:
            faillist.append(href)
            continue
        
        with open('./jobdata/job#%i.txt'%i,'w')as file:
            file.write(summary)
            i+=1

        threads.append(threading.Thread(target= count, args = (summary,wordbank)))
        threads[-1].start()
    for thread in threads:
        thread.join()
    with open('fail.txt','w') as file:
        faillist = json.dumps(faillist, indent= 4)
        file.write(faillist)
    print('finish counting')

    wordbank = dict(sorted(wordbank.items(),key = lambda x:x[1],reverse=True))
    print('finish sorted')
    wordbank = json.dumps(wordbank,indent=4)
    with open('bank.json','w') as file:
        file.write(wordbank)

if __name__ == '__main__':
    main()
