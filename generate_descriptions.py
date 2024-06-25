import os
import anthropic
import base64
import json


def generate_descriptions(img_folder_path):
    """
    Generate natural language descriptions of images in a folder using Claude API and save the descriptions to a JSON file.

    Args:
        img_folder_path (str): Path to the folder containing images.
    """
    descriptions = []
    for filename in os.listdir(img_folder_path):
        if filename.endswith(".jpg"):
            img_path = os.path.join(img_folder_path, filename)
            with open(img_path, "rb") as f:
                img_data = f.read()

            img_data = base64.b64encode(img_data).decode("utf-8")
            img_media_type = "image/jpeg"

            message = claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": img_media_type,
                                    "data": img_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": "Generate natural language descriptions of each image",
                            },
                        ],
                    }
                ],
            )

            # Extract descriptions from message
            description_dict = {
                "filename": filename,
                "id": message.id,
                "description": message.content[0].text,
            }
            descriptions.append(description_dict)

    # Write descriptions to JSON file
    with open("descriptions.json", "w", encoding="utf-8") as f:
        json.dump(descriptions, f, indent=4, ensure_ascii=False)


img_folder_path = "coco_subset"
CLAUDE_API_KEY = os.environ.get("CLAUDE_API_KEY")

claude_client = anthropic.Anthropic(
    api_key=CLAUDE_API_KEY,
)

if __name__ == "__main__":
    generate_descriptions(img_folder_path)
    print("Descriptions generated and saved to descriptions.json")
