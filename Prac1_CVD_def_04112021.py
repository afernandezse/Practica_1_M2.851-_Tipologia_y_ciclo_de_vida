#!/usr/bin/env python
# coding: utf-8



# Export python path

import sys
sys.path.insert(1, '/home/flatline/env/lib/python3.8/site-packages')


from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import re
import random
import pandas as pd
import multiprocessing as mp
import whois
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By




web = 'https://pubmed.ncbi.nlm.nih.gov/?term=TMPRSS2+erg&sort=date&size=200'




# My headers

user_agent_list = [
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36']


# Creation of web browser with selenium
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
# driver.get('https://pubmed.ncbi.nlm.nih.gov/?term=TMPRSS2+erg&sort=date&size=200')

# Cambio de User Agent

headers = {
        'User-Agent':random.choice(user_agent_list),
            'Referer': web,
            'Connection':'keep-alive',
            'Host':'www.ncbi.nlm.nih.gov'
            }




url = requests.get('https://pubmed.ncbi.nlm.nih.gov/?term=TMPRSS2+erg&sort=date&size=200')
url_soup = BeautifulSoup(url.text, 'lxml')

# Examine DOM structure
print(url_soup.prettify())




def get_page_no(searchWord):
    # Build search link
    url = 'https://www.ncbi.nlm.nih.gov/pubmed/?term=' + searchWord
    
    driver.implicitly_wait(1)
    
    # Get maximum page number from returned research result
    tempo_html = requests.get(url,  headers = headers)
    tempo_soup = BeautifulSoup(tempo_html.text, 'lxml')
    max_num = int(int((url_soup.find('span', {'class':'value'}).text))/200)+2
    return max_num
    # print(max_num)


pageNo=get_page_no("TMPRSS2+erg")




# login al site con mi cuenta de google
session = requests.Session()
session.post("https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?response_type=code&client_id=814640896269-sp2o5jfq9cnaqj6ejnnk5r4g17di8ef3.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Fauth.nih.gov%2Faffwebservices%2Fpublic%2Foauthtokenconsumer%2FoAuthLogin&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile%20https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email&state=2ad72bb8-02c2daad-35b22248-0bce592e-9eda855b-54&flowName=GeneralOAuthFlow", data=dict(
email="afernandezse@uoc.edu",
password=""
))




## pmid
## Works

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

results=[]

for no_pages in range(pageNo):
    
    r = session.get('https://pubmed.ncbi.nlm.nih.gov/?term=TMPRSS2%20erg&sort=date&size=200&page='+str(no_pages),
                     headers=headers)
    content = r.content
    soup = BeautifulSoup(content)
    results.append(soup)


pmid = []

for i in range(1, pageNo):
    id = [x.get_text() for x in results[i].find_all('span', {'class':'docsum-pmid'})]
    pmid.append(id)
    
from itertools import chain
    
pmid = list(chain(*pmid))
    
# len(pmid)

# print(pmid[914])




## Authors
## Works

collectAut = []

for i in range(pageNo):
                         
    collect = [x.get_text() for x in results[i].find_all('span', {'class':'docsum-authors full-authors'})]
    collectAut.append(collect)
        
    flat_authors = [item for sublist in collectAut for item in sublist]
    
#len(flat_authors)




## Title
## Works


collectTit = []

for i in range(no_pages +1):
                         
    collect = [x.get_text() for x in results[i].find_all('a', {'class':'docsum-title'})]
    collectTit.append(collect)
        
    flat_title = [item for sublist in collectTit for item in sublist]
    
    ## Remove \n and blank spaces at the beginning and the end
    form_title = []
    for x in flat_title:
            form_title.append(x.replace("\n",""))
            
    final_title = [x.strip(' ') for x in form_title]
    
# print(final_title)




## Long Journal citation
## Works

citation = []

for i in range(no_pages +1):
    
#    journal_cit = [x.get_text() for x in results[i].find_all(("full-journal-citation"))]
#    citation.append(journal_cit)
    
    journal_cit = [x.get_text() for x in results[i].find_all('span', {'class':'docsum-journal-citation full-journal-citation'})]
    citation.append(journal_cit)

    
    
from itertools import chain
    
citation = list(chain(*citation))
    


# print(citation)


# In[39]:


## Short Journal citation
## Works

citation_short = []

for i in range(no_pages +1):
    

    
    short_cit = [x.get_text() for x in results[i].find_all('span', {'class':'docsum-journal-citation short-journal-citation'})]
    citation_short.append(short_cit)

    
    
from itertools import chain
    
citation_short = list(chain(*citation_short))
    


# print(citation_short)




## Urls of all the papers
## Works

site ='https://pubmed.ncbi.nlm.nih.gov/'

web_url = [site + s for s in pmid]

    
print(web_url)




## Download images
## Works

from time import sleep


img_soup=[]
images_format = []

for id in pmid:
    driver.implicitly_wait(1)
    URL = ('https://pubmed.ncbi.nlm.nih.gov/'+str(id))
    try:
        response = requests.get(URL)
    except requests.exceptions.ConnectionError:
        r.status_code = "Connection refused"
            
    soup = BeautifulSoup(response.text, 'lxml')
    img_soup.append(soup)
    
images = []
image_src = []
images_png = []

for i in range(len(pmid)):
    img = [x for x in img_soup[i].find_all('img', src=True)]
    images.append(img)
    images_flat = [item for sublist in images for item in sublist]
    image_src = [x['src'] for x in images_flat]
    image_src = [x for x in image_src if x.endswith('.png')]
    images_png.append(image_src)
    
count=1
for image in images_png[2]:
    with open('plot_'+str(count)+'.png', 'wb') as f:
        res = requests.get(image)
        f.write(res.content)
    count = count+1





## Abstract
## Works

abstract = []

for i in range(len(pmid)):
    abst = [x for x in img_soup[i].findAll('div',{'class':'abstract-content selected'})]
    abstract.append(abst)




## Journal
## Works

journals = []

for i in range(len(pmid)):
    jour = [x.get_text() for x in img_soup[i].findAll('div',{'class':'journal-actions dropdown-block'})]
    journals.append(jour)
    




## DOI
## Works

doi = []

for i in range(len(pmid)):
    doi_number = [x.get_text() for x in img_soup[i].findAll('span',{'class':'citation-doi'})]
    doi.append(doi_number)


# In[82]:


## Pandas dataframe

df = pd.DataFrame(list(zip(flat_authors, pmid, final_title, citation, citation_short, web_url, doi, journals, abstract)),
               columns =['Authors', 'Pubmed id', 'Title', 'Long citation', 'Short citation','url', 'DOI', 'Journal', 'Abstract'])

## Creación de un archivo excel con los resultados

writer = pd.ExcelWriter('Practica1_afernandezse_def.xlsx')
df.to_excel(writer)
writer.save()
