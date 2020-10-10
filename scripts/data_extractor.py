"""
Author: Sedem Quame Amekpewu
Date: Friday, 11th sept. 2020
Description: Script for getting information from tonaton servers.
"""
import requests, json, os.path, db_connector
from os import path
from bs4 import BeautifulSoup
import pymongo

CATEGORY_JSON = f'json/categories.json'
DB_NAME = f'data.db'

# getting env variables
CLIENT = pymongo.MongoClient("mongodb+srv://aggregator_admin:bnGPi7uOtYBKwajc@tonaton.kudrx.mongodb.net/aggregator_admin?retryWrites=true&w=majority")
db_remote = CLIENT.test
db_local = db_connector.LocalDBStore(DB_NAME)
db_local.createConnection()
categories = None

with open(CATEGORY_JSON, f'r') as readData:
    categories = json.load(readData)

for category in categories:
    data = db_local.selectPagesOfData(category["name"], category["name"])
    for row in data:
        try:
            response = requests.get(row[0], timeout=45)

            # parse response text to beautiful soup, for parsing into an object.
            bs = BeautifulSoup(response.text, 'lxml')

            # get information container of interest.
            jsonData = (bs.find_all(f'script')[1].string).replace("window.initialData = ", "")
            adDetail = json.loads(jsonData)["adDetail"]["data"]["ad"]

            productDetail = {
                "slug": adDetail["slug"],
                "title": adDetail["title"],
                "description": adDetail["description"],
                "properties": adDetail["properties"],
                "location": {
                    "name": adDetail["location"]["name"],
                    "geo_region": adDetail["location"]["geo_region"],
                },
                "category": {
                    "name": adDetail["category"]["name"],
                },
                "contactCard": {
                    "name": adDetail["contactCard"]["name"],
                    "phoneNumbers": adDetail["contactCard"]["phoneNumbers"]
                },
                "images": adDetail["images"],
                "money": adDetail["money"],
            }

            result = db_remote[category["name"]].insert_one(productDetail)

            if result.acknowledged:
                # label link as success
                print(f'Successfully, stored scraped {category["name"]} data into database.')
                print("Video id: " + str(result.inserted_id))
            else:
                # label link as a failure
                print("Failed, to store vehicle data into database.")

            del response
        except Exception as e:
            # register faulty link here.
            print(e)
