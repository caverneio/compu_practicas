import requests

from bs4 import BeautifulSoup
from constants import URL, PAYLOAD, HEADERS,PAGE_START

from utils import checkLastPage
from mainxata import dbClient
from extractData import extractData


def update_data():
    page = PAGE_START
    while True:
        url = URL + "?p=" + str(page)
        response = requests.request("GET", url, headers=HEADERS, data=PAYLOAD)
        soup = BeautifulSoup(response.content, "html.parser")

        isLastPage = checkLastPage(soup.text)
        if isLastPage:
            break
        
        job_elements = soup.find_all("article", class_="box_offer")

        for job_element in job_elements:
            id = job_element["data-id"]
            print(f'Processing job {id}')
            data = extractData(id)
            
            if not data["isPracticas"]:
                continue
            
            record = dbClient.get_by_id('JobOffer', id=id)
            if record is not None:
                print(f'Job {id} already exists in database')
                continue
            
            
            del data["isPracticas"]
            
            dbClient.create('JobOffer', id=id, record=data)

            print(f'Job {id} added to database')
        
        print(f'Page {page} processed')
        page += 1

update_data()