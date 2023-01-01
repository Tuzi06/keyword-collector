from selenium import webdriver
from selenium. webdriver.common.by import By
import time
import threading
import json
import urllib3
from bs4 import BeautifulSoup as bs

website = 'https://www.linkedin.com/jobs/search/?currentJobId=3362372256&f_TPR=r604800&geoId=103366113&keywords=Software%20Engineer&location=Vancouver%2C%20British%20Columbia%2C%20Canada&refresh=true'

def count(summary:str, wordbank:dict, i: int ):
    wordlist = summary.replace('\n', ' ').split(' ')
    for word in wordlist:
        if word not in wordbank:
            wordbank[word]=1
        else:
            wordbank[word]+=1
    print('finish counting %ith job summary ' %i)

def main():
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
    # option.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options = option)
    driver.get(website)

    # for _ in range(0,10):
    #    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #    time.sleep(2)
    # print('finish scrolling \n')

    hreflist = []
    wordbank = {}

    for i in range(1,26):
        xpath = '//*[@id="main-content"]/section[2]/ul/li[%i]/div/a'%i
        try:
            job = driver.find_element(By.XPATH,xpath)
            hreflist.append(job.get_attribute('href'))
        except:
            print('xpath has something wrong ')

    print('hreflist has ',len(hreflist),'job links')
    threads = []
    detail = webdriver.Chrome()
    i = j = 0
    faillist = []

    for href in hreflist:
        detail.get(href)
        # try:
        #     button = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/button[1]')
        #     # button.click()
        # except:
        #     print('button has problem')
        # finally:
        #     input('asdf')
        #     time.sleep(1)
        try:
            _ = detail.find_element(By.TAG_NAME,'ul')
            html = urllib3.PoolManager().request('get',href)
            praser = bs(html.data,'html.parser')

            div = praser.find('div',class_= 'show-more-less-html__markup show-more-less-html__markup--clamp-after-5')
            summary = 'set()'
            with open('content.txt','w') as file:
                file.write(div.prettify())
            for child in div.descendants:
                content = child.string
                if content is not None:
                    summary+=' '+content.get_text()
        except:
            try:
                summary = detail.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/div').text
                # print(summary)
                time.sleep(10)
                input('asfasdf')
            except:
                faillist.append(href)
                continue
        

        with open('./jobdata/job#%i.txt'%i,'w')as file:
            file.write(summary)
            i+=1
        # quit()
        # if i ==3:
        #     print(summary)
        #     input('asfasdf')
        #     quit()
        input('adsf')
        threads.append(threading.Thread(target= count, args= (summary,wordbank,j)))
        j+=1
        threads[-1].start()

    for thread in threads:
        thread.join()

    with open('./result/fail.json','w') as file:
        faillist = json.dumps(faillist, indent=4)
        file.write(faillist)
    print('finish counting \n')

    wordbank = dict(sorted(wordbank.items(), key= lambda x:x[1], reverse= True))
    print('finish sorted')

    wordbank = json.dumps(wordbank,indent= 4)
    with open('./result/bank.json','w') as file:
        file.write(wordbank)

if __name__ == '__main__':
    main()
