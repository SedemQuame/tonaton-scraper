import sqlite3

class LocalDBStore:
    def __init__(self, name):
        self.db_name = name

    def createConnection(self):
        self.conn = sqlite3.connect(self.db_name)
        print("successfully created db")
        self.cursor = self.conn.cursor
    
    def executeQuery(self, query):
        self.conn.execute(query)
        self.conn.commit()

    def createDbTable(self, table_name):
        create_table_statement = f'CREATE TABLE IF NOT EXISTS {table_name} (category TEXT NOT NULL, state TEXT NOT NULL, url TEXT NOT NULL UNIQUE);'
        print(create_table_statement)
        self.executeQuery(create_table_statement)

    def insertProductsInToDbTable(self, table_name, category, state, url):
        insert_into_table = f'INSERT INTO {table_name}(category, state, url) VALUES ("{category}", "{state}", "{url}")'
        try:
            self.executeQuery(insert_into_table)
        except sqlite3.IntegrityError as err:
            print("Program tried writting, link multiple times")

    def deleteFromDbTable(self, table_name, url):
        delete_from_table = f'DELETE FROM {table_name} WHERE url = {url}'
        self.executeQuery(delete_from_table)

    def updateRowState(self, table_name, url):
        update_row = f'UPDATE {table_name} SET state = "visited" WHERE url = "{url}"'
        self.executeQuery(update_row)

    def selectPagesOfData(self, table_name, category):
        page_categorical_data = f'SELECT DISTINCT url FROM {table_name} WHERE category = "{category}"'
        data = self.conn.execute(page_categorical_data)
        return data

    
    def closeConnection(self):
        self.conn.close()

       

# create new object of the connector class
# db_instance = LocalDBStore('data.db')
# db_instance.createConnection()
# db_instance.createDbTable('products')
# db_instance.insertProductsInToDbTable('products', 'electronics', 'unvisited', 'https://tonaton.com/en/ad/rode-nt2-a-large-diaphragm-condenser-microphone-for-sale-accra')
# db_instance.insertProductsInToDbTable('products', 'fashion', 'unvisited', 'https://tonaton.com/en/ad/yamaha-psr-s775-for-sale-accra-51')
# db_instance.insertProductsInToDbTable('products', 'fashion', 'unvisited', 'https://tonaton.com/en/ad/barcelona-pink-polo-for-sale-accra-2')
# db_instance.updateRowState('products', 'https://tonaton.com/en/ad/supreme-gluta-white-pills-for-sale-accra')
# db_instance.selectPagesOfData('products', 'Electronics')