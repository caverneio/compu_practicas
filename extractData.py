import requests
from bs4 import BeautifulSoup
from unidecode import unidecode

# https://pypi.org/project/summa
from summa.keywords import keywords

from constants import DETAIL_URL, HEADERS
from checkKeywords import checkKeywords
from utils import parsePublicationDate

def extractData(id):
    payload = {"oi":id}
    response = requests.request("POST", DETAIL_URL, headers=HEADERS, data=payload)
    soup = BeautifulSoup(response.content, "html.parser")
    
    publishedAt = soup.find("p", {"class": "fc_aux fs13"}).text
    publishedAt = parsePublicationDate(publishedAt)

    title = soup.find("p", {"class": "title_offer fs21 fwB lh1_2"}).text
    
    detailElement = soup.find("div", {"class": "header_detail"})

    clElement = detailElement.find("div").find("div")
    company = clElement.find("a").text if clElement.find("a") is not None else None
    location = clElement.find_all("span")[-1].text

    logo= detailElement.find("div", {"class": "logo_company"}).find("a").find("img")["src"]
    if logo.startswith("//"):
        logo = None
        
    element = soup.find(string="Requerimientos")
    parent_element = element.find_parent().find_parent()

    children = list(parent_element.children)


    # Tags
    tagsContainer = children[1].find("div")
    
    tags = []
    for tagElement in tagsContainer.find_all("span"):
        tags.append(tagElement.text)
    
    salary = None # 3000.00
    practicas_flag = False
    part_time = None # False

    for tag in tags:
        if "S/." in tag:
            salary = float(tag.split(" ")[1].replace(".", "").replace(",", "."))
        elif "Prácticas" in tag:
            practicas_flag = True
        elif "parcial" in tag:
            part_time = True

    

    # Body
    bodyHTML = list(children[3].children)
    body = ""
    for element in bodyHTML:
        if element.name == "br":
            body += '\n'
        else:
            body += element.replace("\n", "").replace("\t", "").replace("\r", "").strip()

    # Keywords
    kw = set(keywords(body, language='spanish',deaccent=True, ratio=1).split("\n"))


    title_normalized = unidecode(title.lower())
    for word in title_normalized.split(" "):
        if len(word) > 2:
            kw.add(word)
    
    kw = list(kw)

    # Requirements list
    requirementsList = children[7]

    requirements = []
    for requirement in requirementsList.find_all("li"):
        requirements.append(requirement.text)
    
    education_level = None
    min_experience = 0
    travel = None
    relocate = None
    idioms = None
    conocimientos = None

    for requirement in requirements:
        if "Educación mínima" in requirement:
            education_level = requirement.split(":")[1].strip()
        elif "de experiencia" in requirement: # 2 años de experiencia / Menos de x años de experiencia
            if "Menos de" in requirement:
                min_experience = int(requirement.split(" ")[2])/2
            else:
                min_experience = int(requirement.split(" ")[0])

        elif "Disponibilidad de viajar" in requirement:
            travel = requirement.split(":")[1].strip() == "Si"
        elif "Disponibilidad de cambio de residencia" in requirement:
            relocate = requirement.split(":")[1].strip() == "Si"
        elif "Idiomas" in requirement:
            idioms = requirement.split(":")[1].strip().split(",")
            idioms = [idiom.strip() for idiom in idioms]
        elif "Conocimientos" in requirement:
            conocimientos = requirement.split(":")[1].strip().split(",")
            conocimientos = [conocimiento.strip() for conocimiento in conocimientos]

    isPracticas = (min_experience <= 2) & (checkKeywords(kw) | practicas_flag)
    
    min_experience = None if min_experience == 0 else min_experience
    
    return {
        "title": title,
        "company": company,
        "location": location,
        "logo": logo,
        "salary": salary,
        "body": body,
        "part_time": part_time,
        "education_level": education_level,
        "min_experience": min_experience,
        "travel": travel,
        "relocate": relocate,
        "idioms": idioms,
        "conocimientos": conocimientos,
        "isPracticas": isPracticas,
        "publishedAt": publishedAt,
    }