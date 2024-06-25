import gradio as gr
from utils import display_results

# Create a Gradio interface
interface = gr.Interface(
    fn=display_results,  # Function to perform image search and prepare output
    inputs=gr.Textbox(
        lines=2, placeholder="Enter a description to search images"
    ),  # Input textbox for query
    outputs=[
        gr.Image(type="pil", label="Matched Image/One Possible Image"),
        gr.JSON(label="Search Results"),
    ],  # Output image
    title="Typesense Image Search",  # Title of the Gradio interface
    description="Search for relevant images based on natural language descriptions using Typesense. If error occurs, please re-enter the query with more key objects",  # Description of the interface
    examples=["airport terminal", "young people"],  # Example queries
)

if __name__ == "__main__":
    interface.launch()
