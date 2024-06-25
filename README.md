# Vision-Understanding-and-Retrieval
My Intern Project 3 @USTC: LLM for vision understanding and retrieval

## Instruction
**Dataset**

The same image dataset as Project 1, however, we just need the images, but don't need labels.
Also, a smaller set might be enough, say 50 images.

**Model**

Use Anthropic's Claude LLM for vision understanding. Search the official doc
(https://docs.anthropic.com/en/docs/welcome) to figure out how to call Claude API to process
images. Pick a model which you think is most appropriate. The Claude API key will be sent
separately.

**Search Engine**

Use Typesense (https://typesense.org/) as the vector search engine. For vector embedding, use
multilingual-e5-large as the embedding model. Note that multilingual-e5-large has 512 token
limit. Using Typesense locally is completely free.

**Task Description**

For each image, use Claude LLM to perform vision understanding, generate natural language
descriptions of each image. Necessary prompt tunings are necessary to get good result.
Then, build a search index based on the natural language descriptions in Typesense.
Finally, the Gradio demo should be able to search for relevant images based on input natural
language queries.

## Note:
- Please get your own claude api key if you need to modify *generate_descriptions.py*
- Please run the *typesense_start.sh* first to install Typesense locally. In addition, run *build_index.py* to build an index of image descriptions in Typesense before running *demo/app.py*
- Since Typesense is free only when hosted locally, **this project does not have a HuggingFace Space**. Please run *demo/app.py* to see the demo