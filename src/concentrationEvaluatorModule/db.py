import pymongo

class KeyloggerDatabase:
    def __init__(self, mongo_url, database_name, collection_name):
        self.db_client = pymongo.MongoClient(mongo_url)
        self.db = self.db_client[database_name]
        self.keylogger_collection = self.db[collection_name]
        
    def insertEvaluation(self, data):
        inserted_id = self.keylogger_collection.insert_one(data)
        print(inserted_id)
    
