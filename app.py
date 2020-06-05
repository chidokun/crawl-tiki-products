from bs4 import BeautifulSoup
import requests
import json
import csv

laptop_page_url = "https://tiki.vn/laptop/c8095?src=c.8095.hamburger_menu_fly_out_banner&_lc=&page={}"
product_url = "https://tiki.vn/api/v2/products/{}"

product_id_file = "./data/product-id.txt"
product_data_file = "./data/product.txt"


def crawl_product_id():
    product_list = []
    i = 1
    while (True):
        print("Crawl page: ", i)
        response = requests.get(laptop_page_url.format(i))
        parser = BeautifulSoup(response.text, 'html.parser')

        product_box = parser.findAll(class_="product-item")

        if (len(product_box) == 0):
            break

        for product in product_box:
            product_list.append(product.get("data-id"))

        i += 1

    return product_list, i

def save_product_id(product_list=[]):
    file = open(product_id_file, "w+")
    str = "\n".join(product_list)
    file.write(str)
    file.close()
    print("Save file: ", product_id_file)

def crawl_product(product_list=[]):
    product_detail_list = []
    for product_id in product_list:
        response = requests.get(product_url.format(product_id))
        product_detail_list.append(response.text)
        print("Crawl product: ", product_id, ": ", response.status_code)
    return product_detail_list

flatten_field = [ "badges", "inventory", "categories", "rating_summary", 
                      "brand", "seller_specifications", "current_seller", "other_sellers", 
                      "configurable_options",  "configurable_products", "specifications", "product_links",
                      "services_and_promotions", "promotions", "stock_item", "installment_info" ]

def adjust_product(product):
    e = json.loads(product)
    if not e.get("id", False):
        return None

    for field in flatten_field:
        if field in e:
            e[field] = json.dumps(e[field])

    return e

def save_raw_product(product_detail_list=[]):
    file = open(product_data_file, "w+")
    str = "\n".join(product_detail_list)
    file.write(str)
    file.close()
    print("Save file: ", product_data_file)










    

