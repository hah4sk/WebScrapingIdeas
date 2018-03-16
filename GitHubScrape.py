from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

base_url = 'https://github.com/hah4sk'

#opening up connection, grabbing the page
uClient = uReq(base_url)
page_html = uClient.read()
#close the client
uClient.close()

filename = "RepoDump.txt"
f = open(filename, "w")


#html parsing
page_soup = soup(page_html,"html.parser")
containers = page_soup.findAll("li", {"class": "pinned-repo-item p-3 mb-3 border border-gray-dark rounded-1 public source"})
containers.__add__(page_soup.findAll("li", {"class": "pinned-repo-item p-3 mb-3 border border-gray-dark rounded-1 public fork"}))

name = page_soup.head.title.text
print(name)
index = name.find('·')
name = name[0:index-1]
print(name)
f.write(name + '\'s Repos\n')

for container in containers:
    repoTitle = container.span.span.a.span["title"]
    repoDescription = container.p.text
    f.write(repoTitle + '\n')
    if(repoDescription == ""):
       f.write("No Description Available\n")
    else:
        f.write(repoDescription + '\n')

    repo_url = base_url + '/' + repoTitle
    #opening up connection, grabbing the repo page
    uClient = uReq(repo_url)
    page_html = uClient.read()
    #close the Client
    uClient.close()

    #html parsing
    page_soup = soup(page_html, "html.parser")
    subContainers = page_soup.findAll("td", {"class": "content"})
    for subContainer in subContainers:
        itemTitle = subContainer.text
        #itemTitle = subContainer.findNextSiblings('td').td.span["title"]
        if(subContainer != subContainers[0]):
            f.write(itemTitle)
    f.write("########################\n")