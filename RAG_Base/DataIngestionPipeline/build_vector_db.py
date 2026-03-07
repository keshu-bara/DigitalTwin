import json
from langchain.schema import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings


#load embedding model

embedding_model = HuggingFaceEmbeddings(
    model_name ="sentence-transformers/all-Mini-L6-v2"
)

# load personality memory dataset


with open("personality_memory.json")
