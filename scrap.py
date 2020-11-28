# import Libraries
import requests
import re
from bs4 import BeautifulSoup
import json


def make_request():
    """
    returns BeautifulSoup object containing the data scraped from specified URL
    """
    # specify the url we want to scrape from
    url = "https://www.norauto.fr/t/pneu/w-205-h-55-r-16/ete-s.html/1/"
    # make request
    page = requests.get(url)
    # convert page into a BeautifulSoup Object
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_unordered_lists(soup):
    """
    returns all <ul> tags having the specified class in a BeautifulSoup Object
    """
    # get all <ul> by tagname and class that contain all products
    unordered_lists = soup.find_all('ul',
                                    class_="ws-product-list-items ws-product-list ref-product-summary-view-search-2")
    return unordered_lists


def get_list_items(unordered_lists):
    """
    returns all <li> tags from <ul> tags having the specified class
    """
    products = []
    # get all <li> from selected <ul> by tagname and class
    for product_list in unordered_lists:
        products.extend(product_list.find_all('li', class_="product_list ws-product-list-item"))
    return products


def get_product_dimensions(product):
    """
    returns the dimensions of a precified product
    """
    # get product info (width/ratio diameter)
    dimensions = product.find('h3', class_="text-content text-gray-second font-weight-normal mb-0").get_text()
    return dimensions


def create_product_name(product, dimensions):
    """
    returns the product_name in a the format Produit Dimensions
    """
    # get product name
    name_list = product.find('a', class_="text-gray").get_text().split()
    # concat name_list & width_ratio_diameter_list in order to get full product name
    dimensions_list = dimensions.split()
    # delete Pneu if exists in the dimensions string
    if "Pneu" in dimensions_list: dimensions_list.remove("Pneu")
    product_full_name_list = name_list + dimensions_list
    # convert product name string list to string
    product_name = ' '.join([str(elem) for elem in product_full_name_list])
    return product_name


def create_keyword(dimensions):
    """
    returns the keyword from dimensions with a specified format 3numbers/2numbers 1Char2numbers
    """
    dimensions = dimensions.replace("\u00A0", " ")
    result = re.search("\d{3}/\d{2}\s[A-Z]\d{2}", dimensions)
    return result.group(0)


def get_product_url(product):
    """
    returns the url of a specified product
    """
    product_url = product.find('a', class_="text-gray")['href']
    return product_url


def get_product_price(product):
    """
    returns the price in a float round 2 format
    """
    # get product price tag
    product_price_tag_content = product.find('span',
                                             class_="ws-amount kor-product-sale-price-value price ws-sale-price").get_text()
    # get only digits from product price tag content
    product_price_list = re.findall('\d+', product_price_tag_content)
    # convert product_price_list to float and apply a round 2
    product_price = round(float(product_price_list[0] + '.' + product_price_list[1]), 2)
    return product_price


def create_json_file(dict, filename):
    """
    creates a JSON file with a specific filename from a specified dictionnary
    """
    with open(filename, "w") as task:
        json.dump(dict, task, indent=4, separators=(", ", ": "), sort_keys=True)


def main():
    soup = make_request()
    uls = get_unordered_lists(soup)
    lis = get_list_items(uls)
    # list of dictionnaries of the product's name, price and url
    products_task_1 = []
    # list of dictionnaries of the product's rank, url and keyword
    products_task_2 = []
    for index, product in enumerate(lis):
        dimensions = get_product_dimensions(product)
        product_name = create_product_name(product, dimensions)
        keyword = create_keyword(dimensions)
        product_url = get_product_url(product)
        product_price = get_product_price(product)
        # append product object to products_task_1
        products_task_1.append(
            {
                'name': product_name,
                'url': product_url,
                'price': product_price
            })

        # append product object to products_task_2
        products_task_2.append(
            {
                'rank': index + 1,
                'url': product_url,
                'keyword': keyword
            })
    create_json_file(products_task_1, "output/task_1.json")
    create_json_file(products_task_2, "output/task_2.json")


if __name__ == "__main__":
    main()
