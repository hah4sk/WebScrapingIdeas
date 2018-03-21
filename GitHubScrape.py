from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time

def getRepoDump(base_url, filename):

    # opening up connection, grabbing the page
    uClient = uReq(base_url)
    time.sleep(.500)
    page_html = uClient.read()
    # close the client
    uClient.close()
    # html parsing
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("div", {"class": "pinned-repo-item-content"})

    #create file
    f = open(filename, "w")

    #get title and write to file
    name = page_soup.head.title.text
    print(name)
    index = name.find('·')
    name = name[0:index - 1]
    print(name)
    f.write(name + '\'s Repos\n')
    username = name[0:name.find(' ')]
    print(username)

    #for each repo
    for container in containers:
        repoTitle = container.span.a.span["title"]
        repoDescription = container.p.text
        f.write(repoTitle + '\n')
        if (repoDescription == ""):
            f.write("No Description Available\n")
        else:
            f.write(repoDescription + '\n')

        repo_url = base_url + '/' + repoTitle
        # opening up connection, grabbing the repo page
        uClient = uReq(repo_url)
        time.sleep(.500)
        page_html = uClient.read()
        # close the Client
        uClient.close()

        # html parsing
        page_soup = soup(page_html, "html.parser")
        subContainers = page_soup.findAll("td", {"class": "content"})
        for subContainer in subContainers:
            itemTitle = subContainer.text[1:]
            if (subContainer != subContainers[0]):
                f.write(itemTitle)
                href = subContainer.span.a["href"]
                print(href)
                subDir_url = "https://github.com" + href
                scrapeSubDir(subDir_url, f, "-----")
        f.write("##########################################\n")


def scrapeSubDir(directory_url, f, indent):

    # opening up connection, grabbing the repo page
    uClient = uReq(directory_url)
    time.sleep(.500)
    #uClient = uReq("https://github.com/hah4sk/DragonBall-Fighter-Game/tree/master/Backgrounds")
    page_html = uClient.read()
    # close the Client
    uClient.close()

    # html parsing
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("td", {"class": "content"})

    for container in containers:
        itemTitle = container.text[1:]
        if container != containers[0]:
            f.write(indent + itemTitle)
            href = container.span.a["href"]
            print(href)
            scrapeSubDir("https://github.com" + href, f, indent+"-----")
