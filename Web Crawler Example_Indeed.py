#!/usr/bin/env python
# coding: utf-8

# ## Learn from shared videos

# ### Request

# In[1]:


import requests
from bs4 import BeautifulSoup


# In[2]:


wp = requests.get("https://towardsdatascience.com/robots.txt")
robot_check = wp.text


# In[3]:


test = BeautifulSoup(robot_check, 'html.parser')
print(test.text)


# In[4]:


response = requests.get('https://en.wikipedia.org/wiki/Data_science')
print(response)


# In[5]:


webpage = response.text
print(webpage)


# ### BeautifulSoup

# In[6]:


soup = BeautifulSoup(webpage, 'html.parser')


# In[7]:


print(soup.prettify())


# In[8]:


paragraph = soup.find_all('p')


# In[9]:


paragraph


# In[10]:


soup.find_all('p', attrs={"class": True})


# In[11]:


data = {"title":[], "href":[]}
for link in soup.find_all('a', attrs={"title":True}):
    data["title"].append(link["title"])
    data["href"].append(link["href"])


# In[12]:


import pandas as pd
df = pd.DataFrame(data)


# In[13]:


df


# ### Selenium

# #### Install chromedriver and input

# In[14]:


from selenium.webdriver.chrome.service import Service


# In[15]:


get_ipython().system(' ls /Users/tinaguo/Downloads/')


# In[16]:


service = Service('/Users/tinaguo/Downloads/chromedriver')
service.start()


# #### Define drive

# In[17]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# In[18]:


driver = webdriver.Remote(service.service_url)


# #### Get webpages

# In[19]:


driver.get('http://www.indeed.com/')


# #### Input position

# In[20]:


elem = driver.find_element_by_id('text-input-what')
elem.clear()
elem.send_keys('data scientist')


# #### Return

# In[21]:


elem.send_keys(Keys.RETURN)


# #### Get current link

# In[22]:


print(driver.current_url)


# #### Quit Driver

# In[23]:


# driver.quit()


# ## Indeed Data Scrapy, example from BaiLin

# In[24]:


import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from datetime import datetime, timedelta
import time
from random import random
import os
import json

head = "https:indeed.com"
ca_ds = "https://www.indeed.com/jobs?q=data+scientist&sort=date"

def get_soup(url):
    t = 1 + 2 * random()
    time.sleep(t)
    try:
        page = requests.get(url, headers={'User-Agent': 'Resistance is futile'})
    except:
        return None
    else:
        return BeautifulSoup(page.text, 'lxml')


def find_job_cards(soup):
    return soup.find_all('div', class_="jobsearch-SerpJobCard unifiedRow row result")

class Job_Card():
    def __init__(self, job_card):
        self.job = job_card
        self.summary = {}


    def get_job_title(self):
        try:
            self.summary['title'] = self.job.find('h2', class_='title').a.get_text().strip()
        except:
            self.summary['title'] = None

    def get_company(self):
        try:
            self.summary['company'] = self.job.find('span', class_='company').get_text().strip()
        except:
            self.summary['company'] = None

    def get_company_rating(self):
        try:
            self.summary['rating'] = self.job.find('span', class_='ratingsDisplay').get_text().strip()
        except:
            self.summary['rating'] = None

    def get_job_loc(self):
        try:
            self.summary['loc'] = self.job.find('div', class_='recJobLoc').get('data-rc-loc')
        except:
            self.summary['loc'] = None

    def get_job_remote(self):
        try:
            self.summary['remote'] = self.job.find('span', class_='remote').get_text().strip()
        except:
            self.summary['remote'] = None

    def get_salary(self):
        try:
            self.summary['salary'] = self.job.find('span', class_='salaryText').get_text().strip()
        except:
            self.summary['salary'] = None

    def get_info_page(self):
        try:
            self.summary['info_page'] = head + self.job.find('h2', class_='title').a.get('href')
        except:
            self.summary['info_page'] = None

    def get_job_Description(self):
        info_soup = get_soup(self.summary['info_page'])
        try:
            jd_all = info_soup.find('div', id='jobDescriptionText')
        except:
            self.summary['job_description'] = None
        else:
            self.summary['job_description'] = '\n'.join([p for p in jd_all.descendants if isinstance(p, str)])


def get_newest_jd(url):
    soup = get_soup(url)
    job_cards = find_job_cards(soup)
    job_sum = []
    for job_card in job_cards:
        job = Job_Card(job_card)
        job.get_job_title()
        job.get_company()
        job.get_company_rating()
        job.get_job_loc()
        job.get_job_remote()
        job.get_salary()
        job.get_info_page()
        job.get_job_Description()
        job_sum.append(job.summary)

    return pd.DataFrame(job_sum)

def get_multiple_pages_jd(start_url, n):
    jobs_page1 = get_newest_jd(start_url)
    jobs_all = [jobs_page1]
    for i in range(1, n):
        tail = f'&start={i}0'
        url = start_url + tail
        jobs_all.append(get_newest_jd(url))
    
    return jobs_all

if __name__ == "__main__":
    dfs = get_multiple_pages_jd(ca_ds, 8)
    df = pd.concat(dfs, ignore_index=True) 
    df.to_excel('indeed_ds_job.xlsx', index=False)
    


# In[ ]:


# Example from class

from urllib2 import Request, urlopen
from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import random
import os
import json


head = "https://www.indeed.com/"

chromedriver = "/Applications/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

job_titles = ["data+scientist"]

def get_soup(url):
    """
    This function get the beautifulsoup object of a webpage.

    Args:
        url (str): the link string of webpage

    Returns:
        soup (obj): beautifulsoup object
    """
    request = Request(url, headers={'User-Agent': 'Resistance is futile'})
    response = urlopen(request)
    return BeautifulSoup(response, "html.parser")

def get_jobs_of_title(job_title):
    """
    Args:
        job_title (str): example: 'data+scientist'

    Returns:
    """

    #needed to be changed
    num_pages = 1 #number of pages to scrape
    page_gap_min = 3 #min sleep time between pages
    page_gap_max = 5 #max sleep time between pages
    job_per_page = 50 #number of jobs in one page
    job_gap_min = 5 #min sleep time between jobs
    job_gap_max = 6 #max sleep time between jobs

    for i in range(num_pages): 
        #sleep between each call
        gap = random.uniform(page_gap_min,page_gap_max) 
        time.sleep(gap)

        #each page contains 50 jobs
        tail = "jobs?q={0}&sort=date&limit={1}".format(job_title,job_per_page)
        if i>0:
            tail += "&start={0}".format(i*job_per_page)

        #get link to joblist page
        url = head+tail 
         
        #get links to webpages of jobs on the joblist
        job_page_links = get_job_links_from_page(url)

        for job_page_link in job_page_links:
            gap = random.uniform(job_gap_min,job_gap_max) 
            time.sleep(gap)
            data = get_info_from_job_page(job_page_link)

            print(json.dumps(data))

def get_job_links_from_page(url):
    """
    This function gets the links of the jobs on the joblist page.

    Args:
        url (str): link to joblist page

    Returns:
        job_page_links (list): list of links to the webpages of the jobs
    """

    job_page_links = []
    soup = get_soup(url)
    for item in soup.find_all("a", href=True):
        if '/rc/clk?jk=' in str(item) and 'fccid=' in str(item):
            link = item['href'].split("clk?")[1]
            job_page_links.append(head+'viewjob?'+link)
    return job_page_links

def get_info_from_job_page(url):
    """
    This function get all the useful info from the job webpage.

    Args:
        url (str): link to job webpage

    Returns:
        data (dict): dictionary with keywords: 
                     time_stamp, original_link, job_title, location, company, description
    """
    soup = get_soup(url)
    data = {}
    time_str = soup.find('div',class_='result-link-bar').find('span').getText()

    try:
        data["time_stamp"] = get_timestamp(time_str).strftime("%d-%m-%Y %H:%M")
        data["job_title"] = soup.find('b', class_='jobtitle').getText()
        data["location"] = soup.find('span', class_='location').getText()
        data["company"] = soup.find('span', class_='company').getText()
        data["description"] = soup.find('td',class_='snip').find('div').getText()

        re_link = soup.find('a',class_='sl ws_label')['href'].split("&from=")[0]
        re_link = head[:-1]+re_link
        data["original_link"] = get_original_link(re_link)
    except:
        pass
    return data

def get_timestamp(time_str):
    """
    Calculate the timestamp from the time string.
    
    Args:
        time_str (str): time string, like '2 hours ago'

    Returns:
        time_stamp (obj): timestamp object
    """
    if 'hour' in time_str:
        lag = int(time_str.split('hour')[0])
        delta = timedelta(hours=lag)
        now = datetime.utcnow().replace(second=0,minute=0)
        return now-delta
    else:
        return -1

def get_original_link(url):
    """
    Get the original link of the job description.
    
    Args:
        url (str): the link in Indeed database

    Returns:
        url (str): the original link to the job description
    """
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    time.sleep(2)
    original_url = driver.current_url
    driver.quit()
    return original_url


if __name__ == "__main__":
    get_jobs_of_title("data+scientist")

