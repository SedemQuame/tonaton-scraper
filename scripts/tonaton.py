"""
Author: Sedem Quame Amekpewu
Date: Friday, 11th sept. 2020
Description: Script for getting categorical information on products from the tonaton servers,
             received data is saved in the "categories.json" file in the json folder.
"""
import requests, json, math
from bs4 import BeautifulSoup


URL = f'https://tonaton.com/'
CATEGORY_JSON = f'json/categories.json'
PAGINATED_STR = f'?sort=date&order=desc&buy_now=0&urgent=0&page='

try:
    response = requests.get(URL, timeout=45)

    # parse response text to beautiful soup, for parsing into an object.
    bs = BeautifulSoup(response.text, 'lxml')

    # get information container of interest.
    siteCategories = bs.select(f'.home-categories')[1]
    categoryHolders = siteCategories.select(".lg-3")

    # category list
    categoryList = []

    # loop through info container, and extract info
    for categoryHolder in categoryHolders:
        # create dict for each category.
        name = categoryHolder.select(f'span')[1].get_text()
        link = categoryHolder.select(f'a')[0]['href']
        count = categoryHolder.select(f'.ui-badge')[0].get_text()
        description = categoryHolder.select(f'.info')[0].get_text()
        if "tonaton" not in link:
            link = "https://tonaton.com" + link

        listOfPaginatedLinks = []

        # create list of paginated pages.
        # and store them, in the paginated links file.
        itemsPerPage = 26
        pageCount = math.floor(int(count.replace(',' , ''))/itemsPerPage);
        for x in range(pageCount):
            paginatedLink = f'{link}{PAGINATED_STR}{str(x + 1)}'
            listOfPaginatedLinks.append(paginatedLink)

        # structure for category items
        category = {
            "name": name,
            "count": count,
            "description": description,
            "link": link,
            "paginatedLinks": {
                "visited": [],
                "unvisited": listOfPaginatedLinks,
                "faulty": []
            },
            "state": "unvisited",
        }
        categoryList.append(category)
        category = None

    #store category information.
    with open(CATEGORY_JSON, f'w') as write:
        json.dump(categoryList, write, indent=4)

    # clean up
    del categoryList
except Exception as e:
    print(f'Faulty link')
    # print(e)
    # register faulty link here.

