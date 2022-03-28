#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd

from datetime import datetime, timedelta
import time
from random import random
import os
import json


# In[2]:


chromedriver = "/Applications/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver


# **Locations**
# 
# ny: https://www.indeed.com/jobs?q=data+scientist&rbl=New+York,+NY&jlid=45f6c4ded55c00bf&sort=date
# 
# seattle: https://www.indeed.com/jobs?q=data+scientist&rbl=Seattle,+WA&jlid=1e8a7dce52945215&sort=date
# 
# romote: https://www.indeed.com/jobs?q=data+scientist&rbl=Remote&jlid=aaa2b906602aa8f5&sort=date
# 
# sf: https://www.indeed.com/jobs?q=data+scientist&rbl=San+Francisco,+CA&jlid=6cf5e6d389fd6d6b&sort=date
# 
# boston: https://www.indeed.com/jobs?q=data+scientist&rbl=Boston,+MA&jlid=e167aeb8a259bcac&sort=date
# 
# chicago: https://www.indeed.com/jobs?q=data+scientist&rbl=Chicago,+IL&jlid=402d6ad50e16c894&sort=date
# 
# washington: https://www.indeed.com/jobs?q=data+scientist&rbl=Washington,+DC&jlid=c08ec92d8c031faa&sort=date
# 
# austin: https://www.indeed.com/jobs?q=data+scientist&rbl=Austin,+TX&jlid=d2a39b6d57d82344&sort=date
# 
# atlanta: https://www.indeed.com/jobs?q=data+scientist&rbl=Atlanta,+GA&jlid=966e6327a98f7e81&sort=date
# 
# la: https://www.indeed.com/jobs?q=data+scientist&rbl=Los+Angeles,+CA&jlid=d05a4fe50c5af0a8&sort=date
# 
# ca: https://www.indeed.com/jobs?q=data+scientist&rbl=California&jlid=544e90d8616c87c1&sort=date
# 
# san diego: https://www.indeed.com/jobs?q=data+scientist&rbl=San+Diego,+CA&jlid=15daff915f69f903&sort=date
# 
# arlington: https://www.indeed.com/jobs?q=data+scientist&rbl=Arlington,+VA&jlid=7dbc6e1cb5f59fed&sort=date
# 
# cambridge: https://www.indeed.com/jobs?q=data+scientist&rbl=Cambridge,+MA&jlid=28b85bba6e466386&sort=date
# 

# In[3]:


head = "https://www.indeed.com"
ny_ds = "https://www.indeed.com/jobs?q=data+scientist&rbl=New+York,+NY&jlid=45f6c4ded55c00bf&sort=date"


# In[4]:


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
    all_job_cards = soup.find('div', id='mosaic-provider-jobcards')
    return all_job_cards.find_all('a', href=True, id=True)

class Job_Card():
    def __init__(self, job_card):
        self.job = job_card
        self.summary = {}

    def get_job_title(self):
        try:
            self.summary['title'] = self.job.find('span', title = True).get_text().strip()
        except:
            self.summary['title'] = None

    def get_company(self):
        try:
            self.summary['company'] = self.job.find('span', class_='companyName').get_text().strip()
        except:
            self.summary['company'] = None

    def get_company_rating(self):
        try:
            self.summary['rating'] = self.job.find('span', class_='ratingsDisplay withRatingLink').get_text().strip()
        except:
            self.summary['rating'] = None

    def get_job_loc(self):
        try:
            self.summary['loc'] = self.job.find('div', class_='companyLocation').get_text().split('•')[0]
        except:
            self.summary['loc'] = None

    def get_job_remote(self):
        try:
            self.summary['remote'] = self.job.find('div', class_='companyLocation').get_text().split('•')[1]
        except:
            self.summary['remote'] = None

    def get_salary(self):
        try:
            self.summary['salary'] = self.job.find('span', class_='salary-snippet').get_text().strip()
        except:
            self.summary['salary'] = None

    def get_info_page(self):
        try:
            self.summary['info_page'] = head + self.job.attrs['href']
        except:
            self.summary['info_page'] = None

    def get_job_Description(self):
        info_soup = get_soup(self.summary['info_page'])
        try:
            self.summary['job_description'] = info_soup.find('div', id='jobDescriptionText').get_text()
        except:
            self.summary['job_description'] = None
#         else:
#             self.summary['job_description'] = '\n'.join([p for p in jd_all.descendants if isinstance(p, str)])



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
    dfs = get_multiple_pages_jd(ny_ds,20)
    df = pd.concat(dfs, ignore_index=True) 
    df.to_excel('ny_ds_job.xlsx', index=False)



