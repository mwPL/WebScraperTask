import requests
from bs4 import BeautifulSoup
import os
import string

def convertedTitle(titleIn):
    excluded = string.punctuation
    stripped = titleIn.translate(titleIn.maketrans("", "", excluded))
    return stripped.translate(stripped.maketrans(" ", "_")) + ".txt"

url = "https://www.nature.com/nature/articles"
page = input()
arttype = input()
for i in range(int(page)):
    directory = "Page_" + str(i+1)
    os.mkdir(directory)
    os.chdir(os.path.join(os.getcwd(), directory))

    params = {'searchType': 'journalSearch', 'sort': 'PubDate', 'year': '2020', 'page': i+1}
    r = requests.get(url, params)
    soup = BeautifulSoup(r.content, 'html.parser')
    arts = soup.find_all("article")
    for i in arts:
        cat = i.find("span", class_="c-meta__type")
        if cat.text == arttype:
            title = i.find("a", class_="c-card__link u-link-inherit")
            filetitle = convertedTitle(title.text)
            myfile = open(filetitle, 'w', encoding='utf-8')
            newurl = "https://www.nature.com" + title["href"]
            rr = requests.get(newurl)
            soup2 = BeautifulSoup(rr.content, 'html.parser')
            body = soup2.find("div", class_="c-article-body").text.strip()
            myfile.write(body)
            myfile.close()
    # returning to main directory
    os.chdir(os.path.dirname(os.getcwd()))
print('Saved all articles')