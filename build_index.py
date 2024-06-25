import json
import torch
import typesense
from transformers import AutoTokenizer, AutoModel


def generate_vector(tokenizer, model, text):
    """
    Generate a vector representation of a text using a pre-trained model.
    Args:
        tokenizer (transformers.PreTrainedTokenizer): The tokenizer for the model.
        model (transformers.PreTrainedModel): The pre-trained model.
        text (str): The input text.
    """
    # Limit the text to 512 tokens
    truncated_text = text[:512]

    # Transfer text to token IDs
    input_ids = tokenizer.encode(truncated_text, return_tensors="pt")

    # Get the model's hidden states
    with torch.no_grad():
        outputs = model(input_ids)
        vector = outputs.last_hidden_state.mean(dim=1).squeeze()

    # Convert tensor to list and then to string representation
    vector_representation = ",".join(map(str, vector.tolist()))

    return vector_representation


def build_index(typesense_client):
    """
    Build an index of image descriptions in Typesense.
    Args:
        typesense_client (typesense.Client): The Typesense client.
    """
    tokenizer = AutoTokenizer.from_pretrained("intfloat/multilingual-e5-large")
    model = AutoModel.from_pretrained("intfloat/multilingual-e5-large")

    # Load the json file
    descriptions = []
    with open("descriptions.json", "r", encoding="utf-8") as f:
        descriptions = json.load(f)

    schema = {
        "name": "images",
        "fields": [
            {"name": "filename", "type": "string"},
            {"name": "id", "type": "string"},
            {"name": "description", "type": "string"},
            {
                "name": "vector",
                "type": "string",
                "embedding": {"model": "multilingual-e5-large"},
            },
        ],
    }

    # Create a typesense collection
    collection = typesense_client.collections.create(schema)

    for description in descriptions:
        # Generate vector for each description
        vector = generate_vector(tokenizer, model, description["description"])

        # Create the document
        document = {
            "filename": description["filename"],
            "id": description["id"],
            "description": description["description"],
            "vector": vector,
        }

        # Add the document to the collection
        try:
            typesense_client.collections["images"].documents.create(document)
            print(f"Document '{description['filename']}' indexed successfully.")
        except Exception as e:
            print(f"Failed to index document '{description['filename']}': {e}")

    print("Documents indexed successfully.")


if __name__ == "__main__":
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
    build_index(typesense_client)
