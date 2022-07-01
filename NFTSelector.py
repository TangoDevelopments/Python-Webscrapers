#NFT Selector (Currently only deals with ethereum)
#Based on the user's amount of Ethereum they're willing to spend, this program will
#give a list of the top 3 best NFTs within the past 24 hours to invest in

from bs4 import BeautifulSoup
import requests
import time
from requests import Session

#Secrets.py will hold the API key for cmc
import secrets


#Coinmaketcap public api to get the current price of eth
#this can also be used to get the current price of other currencies,
#but this program only runs on ethereum for now
class CMC:
    #https://coinmarketcap.com/api/documentation/v1/
    def __init__(self, token):
        self.apiurl = 'https://pro-api.coinmarketcap.com'
        self.headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': token,}
        self.session = Session()
        self.session.headers.update(self.headers)
        
    def getPrice(self, symbol):
        url = self.apiurl + '/v1/cryptocurrency/quotes/latest'
        parameters = {'symbol': symbol}
        r = self.session.get(url, params=parameters)
        data = r.json()['data']
        return data
cmc = CMC(secrets.API_KEY)

currency1 = "ETH"
currency2 = "Ethereum"

print("\u001b[35mWelcome to the TangoDevelopments NFT Selector!\n")
time.sleep(0.5)

#Get the user's amount of ethereum
userQuantity = float(input(f"\u001b[37mPlease type how much {currency1} you would be willing to spend on NFTs:\n"))
print("------------------------\n")

#Get the current price of ethereum
price = round(cmc.getPrice(currency1)[currency1]['quote']['USD']['price'], 2)

print(f"The current price of {currency2} is ${price}")
print(f"\u001b[32mYou have: ${round(float(userQuantity * price), 2)} worth of {currency1} that you are willing to spend on NFTs")
print("\u001b[37m\n------------------------")

print("Finding the top 3 NFTs in the past 24 hours to invest in based on your budget...\n\n")

#Starter url needed to find the total number of pages on the website
url = f"https://coinmarketcap.com/nft/collections/?page={1}"
result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
totalPages = int(str(doc.find_all(class_ = "page")[-1]).split("page=")[1].split('"')[0])

#counter to keep track of how many matches we've gotten
counter = 1

#Going therough all pages on the site
#For each page, we scan through each NFT to see if it's a match
#Once we've gotten 3 matches, we can exit all of the loops
for page in range(1, totalPages + 1):
    #We only want the top 3 options
    if counter >= 4:
        break

    #Get info from new page
    newURL = f"https://coinmarketcap.com/nft/collections/?page={page}"
    newResult = requests.get(newURL)
    newDoc = BeautifulSoup(newResult.text, "html.parser")
    divList = newDoc.find_all("tr")

    #Iterating through each NFT on the given page
    for i in range(1, len(divList)):
        #We only want the top 3 options
        if counter >= 4:
            break

        curr = divList[i]

        #Get the name of the current NFT
        name = curr.find("span").string
        if not name:
            continue

        #Get the currency type of the NFT (ETH, SOL, BSC, etc)
        currencyType = str(divList[i].find(class_="logo")).split("</span>")[-2]

        #Get the floor price of the current NFT in string form: "___ ETH"
        displayedFloor = str(divList[i].find_all("td")[4]).split(">")[2].replace("<br/", "")

        #Checking if a link is available to assign to the variable
        if len(str(divList[i].find_all("td")[1]).split('" target')[0].split('href="')) <= 1:
            link = "Link unavailable"
        else:
            link = str(divList[i].find_all("td")[1]).split('" target')[0].split('href="')[1]

        #Some nfts do not have floors displayed and instead show "--". This will be problematic
        #when we want to turn the strign version of the floor into a float
        #Thus, this is the way I decided to check if a floor price exists for the nft
        stringFloorVal = displayedFloor.split(" ")[0]
        splitStringFloor = stringFloorVal.split(".")
        floorExists = True
        for elem in splitStringFloor:
            if not elem.isdigit():
                floorExists = False
                break

        #Checking floor, currencyType, and price to determine if it's a match
        if floorExists and (currencyType == currency2) and (float(stringFloorVal) <= userQuantity):
            # top3[name] = [displayedFloor, link]
            print(f"\u001b[33mRank {counter}:")
            print(f"\u001b[37mName: {name}")
            print(f"Floor Price: {displayedFloor}")
            print(f"Link: {link}")
            print("------------------------")
            counter += 1
if counter == 1:
    print("Unfortunately, we could not find any NFTs with your given budget")
    