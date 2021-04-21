import pymongo

MONGO_URL = "mongodb://localhost:27017/"
DATABASE_NAME = "KeyloggerDB"
COLLECTION_NAME = "keylogs"
    
class KeyloggerDatabase:
    def __init__(self, mongo_url, database_name, collection_name):
        self.db_client = pymongo.MongoClient(mongo_url)
        self.db = self.db_client[database_name]
        self.keylogger_collection = self.db[collection_name]
        
    def insertEvaluation()
