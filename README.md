# tonaton-scraper

Script to scrape, data from tonaton and save them onto a mongo database server.

To run the script, clone this repository and run the command
"pip3 install -r requirements.txt" to install the following dependencies.

1. bs4
2. requests
3. pymongo
4. dnspython
5. lxml
6. sqlite3

To collect the data, into you own database, please change the location pointing to my mongodb,
database to yours, in the data_connector.py file.

Below is a link to an article, which demonstrates how to get that done.
https://intercom.help/mongodb-atlas/en/articles/3013643-creating-databases-and-collections-for-atlas-clusters

It should be noted, that this script will only, work if the current codebase of tonaton is preserved.
This is as a result of hardcoding class names which have specific classes, ids or element tag names, which
contain some data of interest, which was accomplished by using beautifulsoup (bs4).

# Next
1. The project can be extended to act as a multisite scrapper, though necessary adjustments will be needed, to work around sites, that use asynchronous loading, and also sites built using fameworks like React and Angular.
2. With the data stored, in the remote database, a simple frontend project can be created to display the data.
3. ML, can be used to help people get the best deals on similar products listed on multiple sites, by using categorical data such as the location of buyer and seller, product price. 
