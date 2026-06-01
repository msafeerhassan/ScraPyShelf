from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import csv, time

baseURL = "https://books.toscrape.com/"
fileName = "results.csv"
with open(fileName, mode='w', newline='', encoding="utf-8") as csvFile:
    columnHeaders = ["Title", "Cost", "Availability", "Thumbnail Link", "Rating"]
    writer = csv.writer(csvFile)
    writer.writerow(columnHeaders)

def getBookTitles(soup):
    headings = soup.select('h3 a')
    titleList = []
    for title in headings:
        titleList.append(title.get('title'))
    
    return titleList

def getBookCosts(soup):
    prices = soup.find_all(class_="price_color")
    priceList = []
    for price in prices:
        priceList.append(price.get_text())
    newPriceList = []
    for i in priceList:
        newPrice = i.replace("Â", "")
        newPriceList.append(newPrice)
    
    return newPriceList

def getStockAvailability(soup):
    stockAvailability = soup.find_all(class_="instock availability")
    stockAvailabilityList = []
    for availability in stockAvailability:
        status = availability.get_text()
        if status.strip() == "In stock":
            stockAvailabilityList.append("Available")
        else:
            stockAvailabilityList.append("Unavailable")
    
    return stockAvailabilityList

def getImageLink(soup):
    imageLinks = soup.find_all(class_="thumbnail")
    imageLinksList = []
    for link in imageLinks:
        src = link.get('src')
        if src:
            wholeUrl = urljoin("https://books.toscrape.com/", src)
            imageLinksList.append(wholeUrl)
    
    return imageLinksList

def getBookRating(soup):
    bookRatings = soup.find_all('p', class_="star-rating")
    bookRatingsList = []
    for rating in bookRatings:
        allClasses = rating.get('class', [])
        for otherClass in allClasses:
            if otherClass != "star-rating":
                if otherClass == 'One':
                    string = '1 out of 5'
                elif otherClass == "Two":
                    string = '2 out of 5'
                elif otherClass == "Three":
                    string = "3 out of 5"
                elif otherClass == "Four":
                    string = "4 out of 5"
                elif otherClass == "Five":
                    string = "5 out of 5"
                else:
                    string = None
                
                bookRatingsList.append(string)
    
    return bookRatingsList

def saveResults(soup):
    bookTitles = getBookTitles(soup)
    bookCosts = getBookCosts(soup)
    stockAvailability = getStockAvailability(soup)
    thumbnailLinks = getImageLink(soup)
    bookRatings = getBookRating(soup)

    fileName = 'results.csv'

    with open(fileName, mode='a', newline='', encoding="utf-8") as csvFile:
        writer = csv.writer(csvFile)
        for i in range(20):
            writer.writerow([
                bookTitles[i],
                bookCosts[i],
                stockAvailability[i],
                thumbnailLinks[i],
                bookRatings[i]
            ])


while True:
    pagesRequired = int(input("Enter the number of Pages to Scrap (Maximum 50): "))
    if pagesRequired >= 1 and pagesRequired <= 50:
        break
    else:
        print("Please enter correct value!")
        pass


currentURL = "https://books.toscrape.com/catalogue/page-1.html"
pageCount = 1

while currentURL:
    print(f"Scraping Page {pageCount}: {currentURL}")
    try:
        response = requests.get(currentURL)
        if response.status_code != 200:
            print(f"Failed to fetch page {pageCount}")
            break

        soup = BeautifulSoup(response.text, "html.parser")

        saveResults(soup)
        if pageCount == pagesRequired:
            print("Scrapping Done!")
            break
        else:
            pass
        
        nextPage = soup.select_one('li.next a')

        if nextPage and nextPage.has_attr('href'):
            currentURL = urljoin(currentURL, nextPage['href'])
            pageCount += 1
        else:
            print("Scrapping Complete!")
            time.sleep(3)
            currentURL = None
    except Exception as e:
        print(f"Error Occured on Page {pageCount}: {e}")
        break