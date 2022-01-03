import pymongo


class mongodb_connection:

    def __init__(self, wiki_object, db_name, collection_name, summary, refrence_links, base64_format_images):
        """creates the object for wikipedia_task class"""
        try:
            self.wiki_object1 = wiki_object
            self.db_name = db_name
            self.collection_name = collection_name
            self.summary = summary
            self.refrence_links = refrence_links
            self.base64_format_images = base64_format_images

        except Exception as e:
            print("error in init() of class mongodb_connection--" + str(e))

    # mongodb connection
    def create_mongodb_connection(self):
        """creates the mongodb connection"""
        try:
            username = "jyoti8059"
            password = "malik12"

            client = pymongo.MongoClient(
                "mongodb+srv://{}:{}@cluster0.0bt3w.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(
                    username, password))
            db = client.test
            return client
        except Exception as e:
            print("error in create_mongodb_connection() of class mongodb_connection--" + str(e))

    # database creation
    def create_database(self):
        """creates the database"""
        try:
            client = self.create_mongodb_connection()

            Database = client[self.db_name]
            return Database
        except Exception as e:
            print("error in create_database() of class mongodb_connection--" + str(e))

    # collection creation
    def create_collection(self):
        """creates the collection"""
        try:
            Database = self.create_database()
            # collection_name='all_the_data'
            collection = Database[self.collection_name]
            return collection
        except Exception as e:
            print("error in create_collection() of class mongodb_connection--" + str(e))

    # document creation
    def insert_many_records(self):
        """it will insert many records in the collection"""
        try:
            collection = self.create_collection()
            records = [
                {
                    "summary": self.summary
                },
                {
                    "refrence_links": self.refrence_links
                },
                {
                    "images": self.base64_format_images

                }
            ]

            records_inserted = collection.insert_many(records)
            print("document is inserted inside the collection")
            return records_inserted
        except Exception as e:
            print("error in insert_many_records() of class mongodb_connection--" + str(e))

    # checking is database is present
    def check_database_is_present(self):
        """to check if weather the database is present or not"""
        try:

            dbname = self.db_name
            client = self.create_mongodb_connection()

            if dbname in client.list_database_names():
                print("database is present")
                return True
            else:
                print("database is not present or the collection is not created")
                return False
        except Exception as e:
            print("error in check_database_is_present() of class mongodb_connection--" + str(e))

    # checking is collection is present
    def check_collection_is_present(self):
        """to check weather the collection is present or not"""
        try:

            collection_name = self.collection_name
            Database = self.create_database()
            if collection_name in Database.list_collection_names():
                print("collection is present")
                return True
            else:
                print("collection is not present or document is not created")
                return False

        except Exception as e:
            print("error in check_collection_is_present() of class mongodb_connection--" + str(e))

