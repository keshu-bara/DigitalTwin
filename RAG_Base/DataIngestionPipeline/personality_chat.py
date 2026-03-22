from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import subprocess
import ollama


#load embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
)

# Load vector DB
vectorstore = Chroma(
    persist_directory="./personality_vector_db",
    embedding_function=embedding_model
)

retriever = vectorstore.as_retriever(search_kwargs={"k":5})


def generate_reply(user_message):

    docs = retriever.invoke(user_message)

    examples = ""
    for d in docs:
        context = d.page_content
        reply = d.metadata["reply"]
        examples += f"""
Friend: {context}
You: {reply}
"""

    prompt = f"""
    You are a digital twin of a person.

    Your job is to reply like him in WhatsApp chats.

    Rules:
    - Reply as "You"
    - Do NOT repeat the message
    - Give a natural reply
    - Use Hindi + English mix
    - Short casual replies
    - Use emojis sometimes

    Conversation examples:

    {examples}

    Now continue the chat.

    Friend: {user_message}
    You:
    """
    
    response = ollama.chat(
        model = "qwen2.5",
        messages = [{
            "role":"user", "content":prompt
        }],
        options = {
            "temperature":0.9,
            "top_p":0.9
        }
    )

    return response["message"]["content"]



while True:

    user = input("\nYou: ")

    reply = generate_reply(user)

    print("\nBot:", reply)
