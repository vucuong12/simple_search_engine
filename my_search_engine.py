
import requests
from urllib.parse import urljoin
import operator
from flask import Flask, render_template, request

def getWordsFromHtmlPage(htmlPage):
  words = htmlPage.split(" ")
  return words

# A function to download a page
# input: a link to the page (url)
# output: a string representing the page. If the input is invalid (not a html page), the output is None.
def downloadPage(url):
  resp = requests.get(url)
  if resp.ok:
    contentType = resp.headers['content-type']
    if (resp.status_code == 200 and 'text/html' in contentType):
      return resp.text
  return None


def findNextLink(page, findFrom):
  signalPosition = page.find('<a href="', findFrom)
  if (signalPosition == -1):
    return None, 0
  # Find position of the first quote from signalPosition
  firstQuotePos = page.find('"', signalPosition)
  # Find position of the second quote from (firstQuotePos + 1)
  secondQuotePos = page.find('"', firstQuotePos + 1) #1 is length of one double quote
  
  # Select substring between two double quotes.
  nextLink = page[firstQuotePos + 1 : secondQuotePos]
  return nextLink, secondQuotePos

# This function takes page as an input.
# It should output a list of links on the page.
def getAllLinks(page, baseLink):
  # Create an empty list in the beginning.
  links = []
  startFrom = 0
  keepFinding = True
  while (keepFinding):
    nextLink, secondQuotePos = findNextLink(page, startFrom)
    if (nextLink == None):  # Cannot find any other link.
      keepFinding = False  
    else:
      if nextLink.startswith('/'): # A relative link starts with "/" 
        nextLink = urljoin(baseLink, nextLink)   # convert the relative link to a full link.
      if (nextLink.startswith("http")):
        links.append(nextLink)
      startFrom = secondQuotePos
  return links


# firstLink: the first link to crawl
# maxPages: maximum pages to crawl (we are not crawling the whole internet)
def crawlWebsites(firstLink, maxPages):
  
  # 1. Create a list of web page to cral (a list of friends to visit)
  toCrawl = []
  # 2. Add the first link to crawl (Add the first friend to visit)
  toCrawl.append(firstLink)
  
  numCrawled = 0
  
  index = {}
  graph = {}
  # 3. Run from the left to the right of the toCrawl list (friend list)
  while (numCrawled < len(toCrawl) and numCrawled < maxPages):

    # 4. Get the page address (get the friend's name)
    link = toCrawl[numCrawled]

    print ("Start crawling ", link)
    # 5. Crawl the page (visit the friend)
    htmlPage = downloadPage(link)
    words = getWordsFromHtmlPage(htmlPage)
    for word in words:
      if (word in index):
        if (not link in index[word]):
          index[word].append(link)
      else:
        index[word] = [link]
    
    # 6. If the friend does exist.
    if (htmlPage != None):
      
      # 7. Get all links (get a list of other friends)
      allLinks = getAllLinks(htmlPage, link)
      graph[link] = allLinks

      # 8. Only get links that have not seen before (make sures the recommended friends are totally new)
      for link in allLinks:
        if (not link in toCrawl):
          toCrawl.append(link)
      print (len(toCrawl))
    
    # 9. Crawl the next page (visit the next friend).
    numCrawled += 1
  return index, graph

def searchOneWord(word, index):
  word = word.strip()
  if (not (word in index)):
    return []
  return index[word]
  
def searchTwoWords(word1, word2, index):
  if (not (word1 in index) or not (word2 in index)):
    return []
  linkList = []
  for link in index[word1]:
    if (link in index[word2]):
      linkList.append(link)
  return linkList

def getInLinks(graph, page):
  linkList = []
  for link in graph:
    if (page in graph[link] and page != link):
      linkList.append(link)
  return linkList
      
# Computer ranks at step 2,3,4,...

#Input: a graph representing the relationship among our crawled pages.
#Output: a dictionary (ranks). For example, ranks["http://dantri.com.vn"] = 0.7, ranks["http://kenh14.net"] = 0.6
def computePageRanks(graph):
  d = 0.85 # damping factor
  numSteps = 10

  preRanks = {}
  numPages = len(graph)
  
  # Computer ranks at step 0 (copied and pasted from exercise page_rank1.py)
  for page in graph:
    preRanks[page] = 1/numPages
    
  # Your task: Compute ranks at the subsequent steps (step 2, step 3, ...)
  for step in range(1, numSteps + 1): # step = 1..10
    currentRanks = {}
    # Calculate the ranks of all pages based on the formula mentioned in class.
    # Write your code below this line.
    for page in graph:
      newRank = (1 - d) / numPages
      inLinks = getInLinks(graph, page)
      for p in inLinks:
        newRank += d * (1/len(graph[p])) * preRanks[p]
      currentRanks[page] = newRank
    
    
    preRanks = currentRanks
    
  return preRanks

def search(query, index):
  query = query.strip()
  words = query.split(" ")
  words = [word for word in words if word != ""]
  if (len(words) > 2):
    return []
  if (len(words) == 1):
    return searchOneWord(words[0], index)
  return searchTwoWords(words[0], words[1], index)

def sortResultLinks(resultLinks, ranks):
  links = []

  for page in ranks:
    if (page[0] in resultLinks):
      links.append(page)

  return links


index, graph = crawlWebsites("https://blog.codinghorror.com/", 10)
ranks = computePageRanks(graph)
ranks = sorted(ranks.items(), key=operator.itemgetter(1), reverse=True)





app = Flask(__name__)

@app.route("/")
def createQuay1():
  return render_template("search.html")


@app.route("/searchword")
def createQuay2():
  query = request.args.get("query")
  resultLinks = search(query, index)
  resultLinks = sortResultLinks(resultLinks, ranks)
  print (resultLinks)
  return render_template("result.html", resultLinks = resultLinks, query = query)

app.run()