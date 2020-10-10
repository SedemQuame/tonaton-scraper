"""
Author: Sedem Quame Amekpewu
Date: Friday, 11th sept. 2020
Description: Script for getting information from tonaton servers.
"""
import requests, json, os.path, db_connector
from os import path
from bs4 import BeautifulSoup

CATEGORY_JSON = f'json/categories.json'
DB_NAME = f'data.db'

# open categories.json file
# copy dictionary containing links.
# pop active link into either faulty or visited array.
categories = None
with open(CATEGORY_JSON, f'r') as readData:
    categories = json.load(readData)

# count = 0
db_local = db_connector.LocalDBStore(DB_NAME)
db_local.createConnection()
db_local.createDbTable('products')
category_shallow_copy = categories
for category in categories:

    # will hold a batch of links popped from visited and appended to unvisited links
    # unvisitedToVisitedLinksBatchTransition = []
    # count = 0

    # visitedLinkCounter = 0
    for URL in category["paginatedLinks"]["unvisited"]:
        try:
            # parse response text to beautiful soup, for parsing into an object.
            response = requests.get(URL, timeout=45)
            bs = BeautifulSoup(response.text, 'lxml')

            # get information container of interest.
            jsonData = (bs.find_all(f'script')[1].string).replace("window.initialData = ", "")
            ads = json.loads(jsonData)["serp"]["ads"]["data"]["ads"]

            # insert ad links to database
            for ad in ads:
                db.insertProductsInToDbTable('products', category["name"], 'unvisited', f'https://tonaton.com/en/ad/{ad["slug"]}')
            del ads
        except Exception as e:
            print(e)

