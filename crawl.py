import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

def getHtml(url):
    # Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}
    try:
        response = requests.get(url,timeout=40,headers=headers)
        response.raise_for_status()

        response.encoding = response.apparent_encoding

        return response.text
    except:
        import traceback
        traceback.print_exc()

with open('data.txt','r') as f:
    data=f.read().splitlines()
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:57.0) Gecko/20100101 Firefox/57.0'}

browser = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

urlBase='https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&searchField=Search_All&matchBoolean=true&queryText="DOI":'

for i in range(len(data)):
    doi=data[i]
    url=urlBase+doi
    browser.get(url)
    time.sleep(5)
    link_list=browser.find_element_by_xpath("//*[@data-artnum]")
    if link_list=='':
        print('Failed to download the {}-th paper'.format(i))
        continue
    arcNum=link_list.get_attribute('data-artnum')
    pdfUrl='http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber='+arcNum
    soup = BeautifulSoup(getHtml(pdfUrl), 'html.parser')
    result = soup.body.find_all('iframe')
    print(arcNum,result)
    if result==[]:
        print('Failed to download the {}-th paper with article number {}'.format(i,arcNum))
        continue
    downloadUrl = result[-1].attrs['src'].split('?')[0]
    response = requests.get(downloadUrl, timeout=80, headers=headers)
    fname = str(ind)+'_'+downloadUrl[-12:]
    ind+=1

    with open(fname,'ab+') as f:
        print('start download file ',fname)
        f.write(response.content)
