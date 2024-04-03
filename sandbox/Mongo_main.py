from pymongo import MongoClient

CONNECTION_STRING = "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"

def main():
    client = MongoClient(CONNECTION_STRING)

    test_db = client['test_db']
    test_collections = test_db['test_collection']

    test_title = {
        "_id": "U1IT00003",
        "item_name": "Blender_33nn",
        "max_discount": "15%",
        "batch_number": "RR450020FRG",
        "price": 340,
        "category": "kitchen appliance"
    }

    test_collections.insert_one(test_title)

    for item in test_collections.find():
        print(item)


if __name__ == "__main__":
    main()
