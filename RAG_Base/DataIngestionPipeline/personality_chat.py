from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import subprocess


#load embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all_MiniLM-L6-v2"
)

# Load vector DB
vectorstore = Chroma(
    persist_directory="./personality_vector_db",
    embedding_function=embedding_model
)

retriever = vectorstore.as_retriever(search_kwargs={"k":5})


def generate_reply(user_message):

    docs = retriever.get_relevant_documents(user_message)

    examples = ""
    for d in docs:
        context = d.page_content
        reply = d.metadata["reply"]

        examples += f"""
Context: {context}
Reply: {reply}
"""

    prompt = f"""
You are imitating Nikhil Mishra CE.

Reply exactly like him:
- same slang
- same tone
- short casual replies
- Hindi + English mix

Examples:
{examples}

Now reply to this message.

Context: {user_message}
Reply:
"""

    result = subprocess.run(
        ["ollama", "run", "mistral"],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout


while True:

    user = input("\nYou: ")

    reply = generate_reply(user)

    print("\nBot:", reply)
