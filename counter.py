from selenium import webdriver
from selenium. webdriver.common.by import By
import time
import threading
import json

def count(summary:str, wordbank:dict, i: int ):
    wordlist = summary.replace('\n', ' ').split(' ')
    for word in wordlist:
        if word not in wordbank:
            wordbank[word]=1
        else:
            wordbank[word]+=1
    print('finish counting %ith job summary ' %i)

def main():
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
    
    page =2
    linklist = []
    while page<=10:
        joblist = driver.find_element(By.XPATH,'//*[@id="main"]/div/section[1]/div/ul')
        jobs = joblist.find_elements(By.TAG_NAME,'li')
        for job in jobs:
            driver.execute_script('arguments[0].scrollIntoView()',job)
            try:
                links = job.find_elements(By.TAG_NAME,'a')
                if(len(links)>0):
                    linklist.append(links[0].get_attribute('href'))
            except:
                print('not found')
                continue
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
    print('finish fetching')
    print('length: ',len(linklist))
    threads = []    
    i=j=0
    faillist = []
    wordbank= {}

    for href in linklist:
        driver.get(href)
        input('paused')
        continue

        summary = ''
        try:
            lilist = []
            article = driver.find_element(By.TAG_NAME,'article')
            ullist = article.find_elements(By.TAG_NAME,'ul')
            for ul in ullist:
                lilist+=ul.find_elements(By.TAG_NAME,'li')
            
            print(len(lilist))
            for li in lilist:
                try:
                    text = li.get_attribute('innerHTML')
                    text = text.replace('<br>','')
                    text = text.replace('</br>','')

                    summary += ' '+text
                except:
                    print('?????')
                    continue
            # input('found li tag paused')
            summary += article.text

        except:
            try:
                # summary = driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/div/section[1]/div/div/section/div').text
                summary = driver.find_element(By.TAG_NAME,'article').text
                print(type(summary))
            except:
                print('failed')
                faillist.append(href)
                input('paused')
                time.sleep(10)
                continue

        time.sleep(10)
        with open('./jobdata/job#%i.txt'%i,'w')as file:
            file.write(summary)
            i+=1
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


def preload(path):
    # with open('text.txt','r') as file:
    #     vocab = file.read()
    #     return vocab

    with open(path,'r') as file:
        vocab = json.load(file)
        return vocab

def select(vocab1,vocab2,wordbank):
    bank = {}
    for word in wordbank:
        if word.lower() in vocab1 and word.lower()not in vocab2:
            if word.lower() not in bank:
                bank[word.lower()] = wordbank[word]
            else:
                bank[word.lower()] += wordbank[word]
    return bank

if __name__ == '__main__':
    main()

    # with open('./result/bank.json','r') as file:
    #     wordbank = json.load(file)
    # with open('./corpus/csavl-s.json','r') as file:
    #     vocab1 = json.load(file)
    # with open('./corpus/text.txt','r') as file:
    #     vocab2 = file.read()
    # with open('./result/banks.json','w') as file:
    #     bank = select(vocab1,vocab2,wordbank)
    #     bank = json.dumps(bank,indent= 4)
    #     file.write(bank)