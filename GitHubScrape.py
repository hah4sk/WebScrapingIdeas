from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time


def getRepoDump(base_url, filename):
    page_soup = getSoup(base_url)
    containers = page_soup.findAll("div", {"class": "pinned-repo-item-content"})

    #create file
    f = open(filename, "w")

    #get title and write to file
    name = page_soup.head.title.text
    print(name)
    index = name.find('·')
    name = name[0:index - 1]
    print(name)
    f.write(name.upper() + '\'S REPOSITORIES\n')
    username = name[0:name.find(' ')]
    #print(username)

    #for each repo
    for container in containers:
        repoTitle = container.span.a.span["title"]
        repoDescription = container.p.text
        f.write("Repository Title: " + repoTitle + '\n')
        f.write("Repository Description: ")
        if repoDescription == "":
            f.write("No Description Available\n")
        else:
            f.write(repoDescription + '\n')

        f.write("Directories/Files: \n")
        repo_url = base_url + '/' + repoTitle
        # opening up connection, grabbing the repo page
        page_soup = getSoup(repo_url)
        subContainers = page_soup.findAll("td", {"class": "content"})
        for subContainer in subContainers:
            itemTitle = subContainer.text[1:]
            if subContainer != subContainers[0]:
                f.write(itemTitle)
                href = subContainer.span.a["href"]
                print(href)
                subdir_url = "https://github.com" + href
                scrapeSubDir(subdir_url, f, "-----")
        f.write("##########################################\n")


def scrapeSubDir(directory_url, f, indent):

    #get html parsed soup
    page_soup = getSoup(directory_url)
    containers = page_soup.findAll("td", {"class": "content"})

    for container in containers:
        itemtitle = container.text[1:]
        if container != containers[0]:
            f.write(indent + itemtitle)
            href = container.span.a["href"]
            print(href)
            scrapeSubDir("https://github.com" + href, f, indent+"-----")

def getSoup(url):
    # opening up connection, grabbing the page
    uClient = uReq(url)
    time.sleep(.500)
    page_html = uClient.read()
    # close the client
    uClient.close()
    # html parsing
    page_soup = soup(page_html, "html.parser")
    return page_soup
