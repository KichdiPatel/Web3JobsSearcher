from bs4 import BeautifulSoup
import csv
import pandas as pd
import requests

def getJobs(pageNum):
    #url = f"https://web3.career/research-jobs?page={pageNum}" # Research Jobs
    url = f"https://web3.career/intern-jobs?page={pageNum}"
    html = requests.get(url)
    s = BeautifulSoup(html.content, 'html.parser')

    jobs = []

    table = s.find('table', class_='table table-borderless')
    wrapper = table.find_all('div',class_="mb-auto align-middle job-title-mobile")
    # Find all h2 elements within the table

    for job in wrapper:
        title = job.find('h2', class_='fs-6 fs-md-5 fw-bold my-primary')
        link_wrapper = job.find('a', {'data-turbo-frame': 'job', 'data-turbo-action': 'advance'})
        job_link = "https://web3.career" + link_wrapper.get('href')
        jobs.append((title.text, job_link))
    
    return jobs

def filterJobs():
    prevFirstJob = ""
    pageCount = 1

    df = pd.read_csv('jobs.csv')

    while(True):
        jobList = getJobs(pageCount)

        if prevFirstJob == jobList[0][0]:
            break
        
        prevFirstJob = jobList[0][0]

        for job in jobList:
            if("security" in job[0].lower() or "audit" in job[0].lower()): # ADJUST KEYWORD TO SEARCH FOR HERE

                new_row = {'job name': job[0], 'link': job[1]}
                df.loc[len(df)] = new_row
                df = df.drop_duplicates()
                df.to_csv('jobs.csv', index=False)
        
        print("Just Read Page ", pageCount, "...")
        pageCount += 1
    

filterJobs()

