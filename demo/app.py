import typesense
import gradio as gr
import sys
import os

from utils import display_results

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from index_builder.build_index import build_index

# Initialize the Typesense client
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

# Build the Typesense index
build_index(typesense_client)

# Create a Gradio interface
interface = gr.Interface(
    fn=display_results,  # Function to perform image search and prepare output
    inputs=gr.Textbox(
        lines=2, placeholder="Enter a description to search images"
    ),  # Input textbox for query
    outputs=[
        gr.Image(type="pil", label="Matched Images/One Possible Images"),
        gr.JSON(label="Search Results"),
    ],  # Output image
    title="Typesense Image Search",  # Title of the Gradio interface
    description="Search for relevant images based on natural language descriptions using Typesense. If error occurs, please re-enter the query with more key objects",  # Description of the interface
    examples=["airport terminal", "young people"],  # Example queries
)

if __name__ == "__main__":
    interface.launch()
