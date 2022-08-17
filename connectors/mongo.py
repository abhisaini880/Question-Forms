import pymongo


class MongoDB:
    def __init__(self, conn):
        self.conn = conn
        self.connection = self.get_connection()

    def get_connection(self):
        MONGO_HOST = self.conn.get("MONGO_HOST")
        MONGO_PORT = self.conn.get("MONGO_PORT")
        MONGO_DB = self.conn.get("MONGO_DB", "test")
        connection_url = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

        client = pymongo.MongoClient(connection_url)
        return client[MONGO_DB]
