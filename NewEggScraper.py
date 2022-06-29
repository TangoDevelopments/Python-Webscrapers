#This is a python program used to find all of the NewEgg search results of a desired keyword(s) sorted by price

from ast import Lambda
from bs4 import BeautifulSoup
import requests
import re

product = input("Please enter the product you would like to search for on NewEgg: ")
formattedProduct = product.replace(" ", "+")

#grabbing html from the user's desired webpage
url = f"https://www.newegg.com/p/pl?d={formattedProduct}&N=4131"
page = requests.get(url).text
doc = BeautifulSoup(page, "html.parser")


#We want to get the total number of pages on the site for this specific product
pageText = doc.find(class_ = "list-tool-pagination-text").strong
pages = int(str(pageText).split("/")[-2].split(">")[-1][:-1])

desiredPages = int(input(f"There are {pages} pages for this search input. How many pages of results would you like to scan? "))

if desiredPages > pages:
    desiredPages = pages

itemsFound = {}

for page in range(1, desiredPages + 1):

    #Display to show the scan progress
    print(f"Scan {int(page/(desiredPages) * 100)}% complete", end="\r")

    #Getting all of the info for each specific page
    url = f"https://www.newegg.com/p/pl?d={product}&N=4131&page={page}"
    page = requests.get(url).text
    doc = BeautifulSoup(page, "html.parser")
    div = doc.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")

    #Getting hits from a multiple word search can be a bit difficult due to formatting conflicts
    #So I made an initial 2d list which will hold lists of search hits for each word of the search input
    #For example: "logitech keyboard" will search for the results of "logitech," add them to the 2d list
    #then search for "Keyboard," and add those results to the list. (Ordering doesn't matter because everything is sorted
    #by price in the end anyways)
    keyWord2DList = []
    productKeywords = product.split()
    for keyword in productKeywords:
        keyWord2DList.append(div.find_all(text = re.compile(keyword.capitalize())))

    #Flatten the 2d array
    items = []
    for list in keyWord2DList:
        for elem in list:
            items.append(elem)

    #Loop to get info from all of the items we hit
    for item in items:
        #Getting the link for each item
        parent = item.parent
        if parent.name != "a":
            continue
        link = parent["href"]

        #Getting the price for each item
        nextParent = item.find_parent(class_="item-container")
        price = nextParent.find(class_="price-current").strong
        #Making sure we're not operating on a NoneType
        if price:
            price = price.string
            itemsFound[item] = {"Price": int(price.replace(",", "")), "Link": link}

#Sorts the items into a tuple based on price
sortedItems = sorted(itemsFound.items(), key = lambda x: x[1]['Price'])


#Prints out the sorted tuple
for item in sortedItems:
    print(item[0])
    print(f"${item[1]['Price']}")
    print(item[1]['Link'])
    print("------------------------------------")