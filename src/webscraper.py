import requests
import time
import math
import pandas as pd
from bs4 import BeautifulSoup

def get_url(keyword: str, number_of_items: int) -> list:
    """
    This function fetches the urls of the pages to be scraped

    Args:
        number_of_items (int): Number of items to scrape
        keywords (str): the specific item to be scraped

    Returns:
        urls (list): Urls of the pages to be scraped
        
    """
    
    base_url= f"https://www.ebay.ca/sch/i.html?_from=R40&_nkw={keyword}&_sacat=0"
    url_separator= "&_pgn="
    pages= math.ceil(number_of_items/ 63)
    urls= []
    for page_num in range(1, pages + 2):
            page_num= str(page_num)
            if page_num == '0' or page_num == '1':
                url = base_url
            else:
                url = base_url + url_separator + page_num
            urls.append(url)
    return urls

def request_page(url: str) -> requests.Response:
    """
    This function makes a request to the webpage to be scraped
    Args:
        url (str): Url of the page to be scraped

    Returns:
        page (requests.Response): Object containing the server's response to the HTTP request    
            
    """ 
    headers= {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"} 
    page= requests.get(url, headers= headers)
    if page.status_code != 200:
        print("Error processing request")
    return page


def create_soup(page: requests.Response):
    """
    This function parses the html
    Args:
        page (requests.Response): Object containing the server's response to the HTTP request 

    Returns:
        soup: bs4.BeautifulSoup object
           
    """
    soup= BeautifulSoup(page.text, 'html.parser')
    return soup



def find_items(soup, keyword):
    items= soup.find_all('li', {'class': "s-item"})[1:-1] #The first and the last items are excluded because information is missing
    item_list = []
    for item in items:
        title= item.find("h3", {"class": "s-item__title" }).text
        price= item.find_all("span", {"class": "s-item__price" })[0].text.strip('C $ ,').split('to')[0].replace(',', '')
        url_of_item= item.find("a", {"class": "s-item__link" })['href']
        url_of_image= item.find("img", {"class": "s-item__image-img" })['src']
        item_list.append({"category": keyword, "title": title, "price": price, "image_url": url_of_image, "links": url_of_item})
    return item_list



def create_dataframe(data_list: list) -> pd.DataFrame:
    """
    This function creates a dataframe from a list

    Args:
        data_list (str): list of values

    Returns:
        data (pd.DataFrame): a dataframe of input values 
    """
    data= pd.DataFrame(data_list)
    return data


def create_csv(data: pd.DataFrame, file_title: str) -> None:
    """
    This function converts a dataframe to a csv

    Args:
        data (pd.DataFrame): the dataframe to be converted to csv
        file_title (str): title of the output file

    Returns:
        None   
    """
    data.to_csv(f'{file_title}.csv', index= False)


def scrape_data (*keywords:str, number_of_items: int) -> pd.DataFrame:
    """
    This function scrapes the Ebay website and returns a dataframe of the listings. Multiple keywords
    can be passed as parameters

    Args:
        number_of_items (int): Number of items to scrape
        keywords (str): category of items

    Returns:
        data: A dataframe of all the items scraped, including their prices, links to images and urls
        
    """
    data_list= [] 
    for keyword in keywords:
        urls= get_url(keyword, number_of_items)
        for url in urls:
            page= request_page(url)
            soup= create_soup(page)
            items= find_items(soup, keyword)
            data_list.extend(items)
            # if len(data_list) >= number_of_items:
            #     break
            print ('Next page to be scraped and appended')
            time.sleep(4)
    data= create_dataframe(data_list)
    return data




