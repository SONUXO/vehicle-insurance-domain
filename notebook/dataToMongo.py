import os
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

try:
    # Step 1: Read env vars
    mongo_uri = os.getenv("MONGO_CLUSTER_URI")
    mongo_db = os.getenv("MONGO_DB")
    collection_name = "vehicleData"

    if not mongo_uri or not mongo_db:
        raise ValueError("Environment variables MONGO_CLUSTER_URI or MONGO_DB are not set properly.")
    
    print(f"[INFO] Using database: {mongo_db}")
    print(f"[INFO] Connecting to Mongo URI: {mongo_uri[:50]}...")  # Only show partial URI for security

    # Step 2: Load CSV
    data_path = "data.csv"
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"CSV file not found at path: {data_path}")
    
    df = pd.read_csv(data_path)
    print(f"[INFO] Loaded CSV with {len(df)} records.")

    data = df.to_dict(orient="records")

    # Step 3: Connect to MongoDB
    try:
        client = MongoClient(mongo_uri)
        database = client[mongo_db]
        collection = database[collection_name]
        print(f"[INFO] Connected to MongoDB and selected collection: {collection_name}")
    except Exception as conn_error:
        print("[ERROR] Failed to connect to MongoDB:")
        raise conn_error

    # Step 4: Insert into MongoDB
    if data:
        res = collection.insert_many(data)
        print(f"[SUCCESS] Inserted {len(res.inserted_ids)} documents.")
    else:
        print("[WARN] No data to insert.")

except Exception as e:
    print(f"[EXCEPTION] {type(e).__name__}: {e}")
