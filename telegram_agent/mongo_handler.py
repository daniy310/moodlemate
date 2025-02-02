import os
from pymongo import MongoClient, errors
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize MongoDB client
class MongoHandler:
    def __init__(self, collection_name):
        """
        Initialize the MongoDB Handler.

        Args:
            collection_name (str): The name of the MongoDB collection.
        """
        # Get the MongoDB connection URI and database name from environment variables
        uri = os.getenv("MONGO_URL", "mongodb://mongo:mongo@localhost:27017")
        db_name = os.getenv("MONGO_DB", "moodlemate_db")

        # Connect to the MongoDB instance
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save(self, data, unique_key=None):
        """
        Save or update a document in the MongoDB collection.

        Args:
            data: The data to save.
            unique_key (dict): The unique key for checking duplicates. Defaults to None.
        """
        try:
            if unique_key:
                self.collection.update_one(
                    unique_key,  # Check for duplicates
                    {"$set": data},  # Update if exists
                    upsert=True  # Insert if no match
                )
            else:
                self.collection.insert_one(data)  # Insert if no unique key provided

            print("Data saved successfully.")
        except errors.DuplicateKeyError:
            print("Duplicate data ignored.")
        except Exception as e:
            print(f"Error saving data: {e}")

    def update(self, unique_key, update_dict):
        """
        Update an existing document in the MongoDB collection.

        Args:
            unique_key (dict): The unique key to identify the document.
            update_dict (dict): The data to update.
        """
        try:
            self.collection.update_one(unique_key, {"$set": update_dict})
            print("Data updated successfully.")
        except Exception as e:
            print(f"Error updating data: {e}")

    def find(self, query):
        """
        Find a document in the collection.

        Args:
            query (dict): The query to match the document.
        """
        return self.collection.find_one(query)

    def find_many(self, query):
        """
        Find documents in the collection.

        Args:
            query (dict): The query to match documents.

        Returns:
            list: A list of documents that match the query.
        """
        return list(self.collection.find(query))

