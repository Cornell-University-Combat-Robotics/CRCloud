import chromadb
import drive_downloads

DEBUG = True


if DEBUG:
    filename = "test"
    drive_downloads.save_json(drive_downloads.CLOUD_FOLDER_ID)
    collection = drive_downloads.vectorize_json("data.json")
    print(f'Vectorize_json return: {collection}')

    results = collection.query(
    query_texts=["Rohin is 5'11"], # Chroma will embed this for you
    n_results=3 # how many results to return
    )
    print(f"top 3 results = {results['ids']}")  
