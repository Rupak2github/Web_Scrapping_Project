from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Function to extract product title
def get_title(soup):
    try:
        # Outer tag object
        title = soup.find('span', attrs={"class":'B_NuCI'})

        #Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("div", attrs={"class":'_30jeq3'}).text.strip()
    except AttributeError:
        price = ""
    return price

if __name__ == '__main__':

    # Headers for request
    HEADERS = ({"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36", "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"})

    # The webpage URL
    URL = "https://www.flipkart.com/search?q=ps5&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links as List of Tag Objects
    links = soup.find_all("a", attrs={'class':'s1Q9rs'})

    # Store the links
    links_list = []

    # Loop for extracting links from Tag objects
    for link in links:
        links_list.append(link.get('href'))

    d = {"title":[], "price":[]}

    # Loop for extracting product details from each link
    for link in links_list:
        new_webpage = requests.get("https://www.flipkart.com" + link, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))

    flipkart_df = pd.DataFrame.from_dict(d)
    flipkart_df['title'].replace('',np.nan, inplace=True)
    flipkart_df = flipkart_df.dropna(subset=['title'])
    flipkart_df.to_csv("flipkart.csv", header=True, index=False)


