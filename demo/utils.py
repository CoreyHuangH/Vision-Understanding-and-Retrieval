import typesense
import os
from PIL import Image


def search_images(query, typesense_client):
    """
    Search for images based on a query using Typesense.
    Args:
        query (str): The search query.
        typesense_client (typesense.Client): The Typesense client.
    """
    try:
        print(f"Searching images for query: {query}")

        # Perform the search query
        search_results = typesense_client.collections["images"].documents.search(
            {
                "q": query,
                "query_by": "description",  # Search by the 'description' field
                "sort_by_score": True,  # Sort by the relevance score
                "num_typos": 0,  # Allow zero typos in the query
            }
        )

        print(f"Search results: {search_results}")

        # Extract relevant information from search results
        results = []
        for hit in search_results["hits"]:
            doc = hit["document"]
            results.append(
                {"filename": doc["filename"], "description": doc["description"]}
            )

        return results

    except Exception as e:
        print(f"Error searching images: {e}")
        return []


def get_img_path(img_folder_path, filename):
    return os.path.join(img_folder_path, filename)


def display_results(query):
    """
    Display the search results for a given query.
    Args:
        query (str): The search query.
    """
    typesense_client = typesense.Client(
        {
            "nodes": [
                {
                    "host": "localhost",
                    "port": "8108",
                    "protocol": "http",
                }
            ],
            "api_key": "xyz",
            "connection_timeout_seconds": 2,
        }
    )
    img_folder_path = "coco_subset"
    results = search_images(query, typesense_client)

    # Prepare output for Gradio
    for result in results:
        image_path = get_img_path(img_folder_path, result["filename"])
        output = Image.open(image_path)

    return output, results
