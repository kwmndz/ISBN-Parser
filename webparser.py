from bs4 import BeautifulSoup
import requests
import csv
import random
import time

with open("keys.txt", 'r') as keys:
    key = keys.readline().strip()
    key2 = keys.readline().strip()
    
KEY = key  #For website credentials
KEY2 = key2
FILE_PATH = "./ISBNlogs/isbn_log.txt" # Input log file gotten from barcode scanner app(all ISBN's)
OUT_PATH = "./Naval_Books.csv" # Output for data 
FAIL_PATH = "./failed/failed.csv"  # Outpute for ISBN's with data that couldnt be found


def getRandUserAgent(file, num):
    with open(file, 'r', encoding= 'utf-8') as f:
        lines = f.readlines()

    return lines[num].strip()


def run(isbn):
    try:
        # First website for ISBN data 
        # For the price mainly
        
        url = f"https://www.bookfinder.com/search/?isbn={isbn}&mode=isbn&st=sr&ac=qr"
        
        # To keep the "Human Checks" from popping up 
        userAgent = getRandUserAgent("UserAgents.txt", random.randint(0,999))
        headers = {
            "User-Agent": userAgent
        }
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        viewport_tag = soup.find("meta", attrs={"name": "viewport"})

        # Modify the viewport content
        if viewport_tag:
            viewport_tag["content"] = "width=100, initial-scale=1.3"

        # Convert the modified HTML back to string
        modified_html = str(viewport_tag)

        # Send the modified HTML to the server
        response = requests.post(url, data=modified_html)

        time.sleep(0.4)
        
        # Try to get data for the price new
        product_div = soup.find('tr', class_='results-table-first-LogoRow has-data')
        if product_div:
            product_div = product_div.find_all("td", "results-table-center")[2]
            price_new = product_div.find('a').text.strip()
            price_new = float(price_new.replace("$",""))

        time.sleep(0.4)
        
        # Check to see if it has data needed (price used)
        try:
            product_div = soup.find_all('tr', class_='results-table-first-LogoRow has-data')[1]
            if product_div:
                product_div = product_div.find_all("td", "results-table-center")[2]
                price_used = product_div.find('a').text.strip()
                price_used = float(price_used.replace("$",""))
        except:
            price_used = price_new
            price_new = 0.00

    # if has no price data set them to 0 
    except Exception as e:
        print(str(e),isbn) # print exception for debuggin purposes
        price_new = 0.00
        price_used = 0.00

    try:
        # Second website mainly for finding catagorizing data for the books
        
        h = {'Authorization': KEY}
        response = requests.get(f"https://api.pro.isbndb.com/book/{isbn}", headers=h)
        data = response.json()
        book_info = data.get("book")
        title = book_info.get("title_long")
        author = book_info.get("authors")[0]
        publish_date = book_info.get("date_published")
        msrp = book_info.get("msrp")

        return {
            "ISBN": isbn,
            "Title": title,
            "Author": author,
            "Date Published": publish_date,
            "MSRP": msrp,
            "New": price_new,
            "Used": price_used
        }
    except:
        return {
            "ISBN": isbn,
            "Title": "N/A",
            "Author": "N/A",
            "Date Published": "N/A",
            "MSRP": "N/A",
            "New": price_new,
            "Used": price_used
        }


if __name__ == '__main__': 

    file_path = FILE_PATH
    # Save all logged ISBN's to a lists
    with open(file_path, 'r') as file:
        lines = file.readlines()
    bk_info = [] # intialize the list of dictionaries
    failed = [] # Intialize the list of ISBN's with data that couldnt be found
    for line in lines:
        isbn = line.strip()
        # Make sure an actual ISBN was acquired ISBN-10 or ISBN-13 acceptable
        if len(isbn) != 10 and len(isbn) != 13: 
            continue
        
        # Clean up raw str data to be used
        if "-" in isbn:
            isbn = isbn.replace("-","")
        if "x" in isbn:
            isbn = isbn.replace("x","5")
        if "X" in isbn:
            isbn = isbn.replace("X", "5")
        if " " in isbn:
            isbn = isbn.replace(" ", "")
        
        # Make sure it is only numbers
        try: 
            int(isbn)
        except ValueError:
            continue
        
        # run the search on the list of isbns
        temp = run(isbn) 
        if temp["Title"] == "N/A": # If data couldnt be found make it a fail
           print("fail", isbn)
           failed.append(temp)
        else: # otherwise add it to the book info (data type is a dict)
           bk_info.append(temp)
    
    # Write to csv files 
    with open(OUT_PATH, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['ISBN', 'Title', 'Author', 'Date Published', "MSRP", "New", "Used"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(bk_info)

    with open(FAIL_PATH, 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['ISBN', 'Title', 'Author', 'Date Published', "MSRP", "New", "Used"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(failed)

    print(f"Book information has been written # AWESOME!
