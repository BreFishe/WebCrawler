import requests
from bs4 import BeautifulSoup

recursivelist = set()
url = "https://johnnyworms.ca"
actual_length = 0

def non_external_basic_spider(length):
    global actual_length
    actual_length = length
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    for link in soup.findAll('a'):
        if link.get('href').find("http", 0, len(str(link))) == 0:
            recursivelist.add(str(link.get('href')))
        else:
            recursivelist.add(url + str(link.get('href')))

    # recursive list makes it so multiples of the same link don't show up

    for links in recursivelist:

        print("Root: " + str(links))
        non_external_recursive_search(links, 0)

    for links in recursivelist:
        print(str(links))
    print("Finished")

def external_basic_spider(length):
    global actual_length
    actual_length = length
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")

    for link in soup.findAll('a'):
        if link.get('href').find("http", 0, len(str(link))) == 0:
            recursivelist.add(str(link.get('href')))
        else:
            recursivelist.add(url + str(link.get('href')))

    # recursive list makes it so multiples of the same link don't show up

    for links in recursivelist:
        print("Root: " + str(links))
        external_recursive_search(links, 0)

    for links in recursivelist:
        print(str(links))
    print("Finished")


def non_external_recursive_search(link, tracker):
    global recursivelist
    global url
    external_site = set()
    used_href = set()

    if actual_length<=tracker:
        print("ending")
        quit()

    tracker +=1
    print("trying " + str(link))

    try:
        if str(link) == ("None"):
                print("Nothing")

        else:
            #Start of Recursive search
            source_code = requests.get(link)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "html.parser")
            temprecursivelist = set()
            for alink in soup.findAll('a'):
                if alink.get('href').find("http", 0, len(str(alink))) == 0:     #tests to see if the site is external or not
                    external_site.add(str(alink.get('href')))                   #Idea for tomorrow just add this whole code bit but change this one line
                    print("External Site")
                else:
                    templist = set()
                    if len(used_href) == 0:                                     #This line tests if used_href is emtpy and if it is just adds the first one
                        temprecursivelist.add(url + (str(alink.get('href'))))
                        used_href.add(str(alink.get('href')))
                    else:
                        for href in used_href:
                            #print(href)                                        #Testing for using hrefs
                            #print(str(alink.get('href')))                      #tests to see if href has been used on this branch so far
                            if href == str(alink.get('href')):
                                print("Used Href")
                            else:
                                temprecursivelist.add(url + (str(alink.get('href'))))
                                templist.add(str(alink.get('href')))
                                print("New Href")
                    used_href = used_href | templist

            temprecursivelist = temprecursivelist - recursivelist               #This edits my list so I don't search repeated sites
            recursivelist = recursivelist | temprecursivelist | external_site

            for link in temprecursivelist:
                #length=-1
                print("Recursive tracker " + str(tracker) + "\n")
                print(link + "\n")
                non_external_recursive_search(link,tracker)
            # else:
            #     return length
    except:
        print("error on " + str(link))
        recursivelist.discard(str(link))
        print("This could possibly mean that the page is empty or that there is an issue with the link \n")

def take_text(link):
    url = link
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    print(soup.text)



def external_recursive_search(link, tracker): #monster algorhitm
    global recursivelist
    external_site = set()
    global url
    used_href = set()
    if actual_length<=tracker:
        print("quitting")
        quit()

    tracker +=1
    print("trying " + str(link))
    try:
        if str(link) == ("None"):
                print("here")

        else:
            print("in the recursive search")
            source_code = requests.get(link)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "html.parser")
            temprecursivelist = set()
            for alink in soup.findAll('a'):
                if alink.get('href').find("http", 0,len(str(alink))) == 0:      # tests to see if the site is external or not
                    external_site.add(str(alink.get('href')))               # Idea for tomorrow just add this whole code bit but change this one line
                    print("External Site")
                else:
                    templist = set()
                    if len(used_href) == 0:                                     # This line tests if used_href is emtpy and if it is just adds the first one
                        temprecursivelist.add(url + (str(alink.get('href'))))
                        used_href.add(str(alink.get('href')))
                    else:
                        for href in used_href:
                            # print(href)                                       #Testing for using hrefs
                            # print(str(alink.get('href')))                     #tests to see if href has been used on this branch so far
                            if href == str(alink.get('href')):
                                print("Used Href")
                            else:
                                temprecursivelist.add(url + (str(alink.get('href'))))
                                templist.add(str(alink.get('href')))
                                print("New Href")
                    used_href = used_href | templist

            temprecursivelist = temprecursivelist - recursivelist
            recursivelist = recursivelist | temprecursivelist

            print("if nothing prints no new links \n")
            for link in temprecursivelist:

                print("now I'm searching")
                print("Recursive tracker " + str(tracker))
                print(link + "\n")
                external_recursive_search(link,tracker)
            for link in external_site:
                external_site_recursive_search(link,tracker)
    except:
        print("error on " + str(link))
        recursivelist.discard(str(link))
        print("This could possibly mean that the page is empty or that there is an issue with the link \n")


def external_site_recursive_search(link, tracker): #monster algorhitm
    global recursivelist
    new_url = link[0:find_nth(link,"/",3)]
    external_site = set()
    print("this is the link of the child: " + str(link))
    print("edited link: " + link[0:find_nth(link,"/",3)])

    used_href = set()
    if actual_length<=tracker:
        print("quitting")
        quit()

    tracker +=1
    print("trying " + str(link))
    try:
        if str(link) == ("None"):
                print("Nothing here")

        else:
            print("in the recursive search")
            source_code = requests.get(link)
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "html.parser")
            temprecursivelist = set()
            for alink in soup.findAll('a'):
                if alink.get('href').find("http", 0,len(str(alink))) == 0:      # tests to see if the site is external or not
                    external_site.add(str(alink.get('href')))               # Idea for tomorrow just add this whole code bit but change this one line
                    print("External Site")
                else:
                    templist = set()
                    if len(used_href) == 0:                                     # This line tests if used_href is emtpy and if it is just adds the first one
                        temprecursivelist.add(new_url + (str(alink.get('href'))))
                        used_href.add(str(alink.get('href')))
                    else:
                        for href in used_href:
                            # print(href)                                       #Testing for using hrefs
                            # print(str(alink.get('href')))                     #tests to see if href has been used on this branch so far
                            if href == str(alink.get('href')):
                                print("Used Href")
                            else:
                                temprecursivelist.add(new_url + (str(alink.get('href'))))
                                templist.add(str(alink.get('href')))
                                print("New Href")
                    used_href = used_href | templist

            temprecursivelist = temprecursivelist - recursivelist
            recursivelist = recursivelist | temprecursivelist

            print("if nothing prints no new links \n")
            for link in temprecursivelist:

                print("now I'm searching")
                print("Recursive tracker " + str(tracker))
                print(link + "\n")
                external_site_recursive_search(link,tracker)
    except:
        print("error on " + str(link))
        recursivelist.discard(str(link))
        print("This could possibly mean that the page is empty or that there is an issue with the link \n")

def find_nth(word, character, index):
    start = word.find(character)
    while start >= 0 and index > 1:
        start = word.find(character, start+len(character))
        index -= 1
    return start


#print(external_site_edit("https://twitter.com/johnnyworms/", 2))
#non_external_basic_spider(5)
external_basic_spider(2)