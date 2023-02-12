import requests
from bs4 import BeautifulSoup

from constants import DETAIL_URL, HEADERS

def formatData(id):
    payload = {"oi":id}
    response = requests.request("POST", DETAIL_URL, headers=HEADERS, data=payload)
    soup = BeautifulSoup(response.content, "html.parser")
    
    element = soup.find(string="Requerimientos")
    parent_element = element.find_parent().find_parent()

    children = list(parent_element.children)


    # Tags
    tagsContainer = children[1].find("div")
    tagsContainer["class"] = "space-x-4 mb-4"
    
    for tagElement in tagsContainer.find_all("span"):
        tagElement["class"] = "cursor-pointer rounded-full py-1.5 px-4 text-xs font-bold bg-rose-600 hover:bg-opacity-70 bg-opacity-100 text-white"

    # Body
    bodyContainer = children[3]
    bodyContainer["class"] = "pr-8"

    # Requirements header
    requirementsHeader = soup.new_tag("h2")
    requirementsHeader["class"] = "font-bold text-lg mt-4 mb-2"
    requirementsHeader.string = "Requerimientos"

    # Requirements list
    requirementsList = children[7]
    requirementsList["class"] = "list-disc list-inside space-y-2"
    
    for requirement in requirementsList.find_all("li"):
        requirement["class"] = ""
    
    parsedHTML = soup.new_tag("div")
    parsedHTML.append(tagsContainer)
    parsedHTML.append(bodyContainer)
    parsedHTML.append(requirementsHeader)
    parsedHTML.append(requirementsList)

    parsedHTML["class"] = "sm:h-[280px] h-[520px] py-4 overflow-y-auto dark:text-zinc-400 text-zinc-700"

    detail = parsedHTML.text
    detailHTML = str(parsedHTML)

    return [detail, detailHTML]
    
    

