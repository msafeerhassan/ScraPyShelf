from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

url = "https://books.toscrape.com/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

def getBookTitles():
    headings = soup.select('h3 a')
    titleList = []
    for title in headings:
        titleList.append(title.get('title'))
    
    return titleList

def getBookCosts():
    prices = soup.find_all(class_="price_color")
    priceList = []
    for price in prices:
        priceList.append(price.get_text())
    newPriceList = []
    for i in priceList:
        newPrice = i.replace("Â", "")
        newPriceList.append(newPrice)
    return newPriceList

def getStockAvailability():
    stockAvailability = soup.find_all(class_="instock availability")
    stockAvailabilityList = []
    for availability in stockAvailability:
        status = availability.get_text()
        if status.strip() == "In stock":
            stockAvailabilityList.append(True)
        else:
            stockAvailabilityList.append(False)
    
    print(stockAvailabilityList)

def getImageLink():
    imageLinks = soup.find_all(class_="thumbnail")
    imageLinksList = []
    for link in imageLinks:
        src = link.get('src')
        if src:
            wholeUrl = urljoin("https://books.toscrape.com/", src)
            imageLinksList.append(wholeUrl)
    
    print(imageLinksList)

def getBookRating():
    bookRatings = soup.find_all('p', class_="star-rating")
    bookRatingsList = []
    for rating in bookRatings:
        allClasses = rating.get('class', [])
        for otherClass in allClasses:
            if otherClass != "star-rating":
                if otherClass == 'One':
                    string = '1/5'
                elif otherClass == "Two":
                    string = '2/5'
                elif otherClass == "Three":
                    string = "3/5"
                elif otherClass == "Four":
                    string = "4/5"
                elif otherClass == "Five":
                    string = "5/5"
                else:
                    string = None
                
                bookRatingsList.append(string)
    print(bookRatingsList)


getBookRating()