import requests
import time
import math
import pandas as pd
from bs4 import BeautifulSoup

def get_data(*keywords: str, number_of_items: int) -> pd.DataFrame:
    """
    This function scrapes the Ebay website and returns a dataframe of records

    Args:
        number_of_items (int): Number of items to scrape
        keywords (str): category of items

    Returns:
        data: A dataframe of all the items scraped, including their prices, links to images and urls
        
    """
    item_list= []
    for keyword in keywords:
        base_url= f"https://www.ebay.ca/sch/i.html?_from=R40&_nkw={keyword}&_sacat=0"
        keyword= keyword
        url_separator= "&_pgn="
        pages= math.ceil(number_of_items/ 63)
        for page_num in range(1, pages + 2):
            page_num= str(page_num)
            if page_num == '0' or page_num == '1':
                url = base_url
            else:
                url = base_url + url_separator + page_num
                headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"} 
                page= requests.get(url, headers= headers)
                soup= BeautifulSoup(page.text, 'html.parser')
                items= soup.find_all('li', {'class': "s-item"})[1:-1] #The first and the last items are excluded because information is missing
                for item in items:
                    title= item.find("h3", {"class": "s-item__title" }).text
                    price= item.find_all("span", {"class": "s-item__price" })[0].text.strip('C $ ,').split('to')[0].replace(',', '')
                    url_of_item= item.find("a", {"class": "s-item__link" })['href']
                    url_of_image= item.find("img", {"class": "s-item__image-img" })['src']
                    item_list.append({"category": keyword, "title": title, "price": price, "image_url": url_of_image, "links": url_of_item})
            time.sleep(5)
            print('page', page_num, 'scraped')
    data= pd.DataFrame(item_list)
    return data



data= get_data('ps4', 'iphone', 'camera', number_of_items= 3600)
data.to_csv('products.csv', index= False)