import os
import logging
from rag_utils import parse_chat, reply_context_chat, create_rag_memory, save_rag_memory

logging.basicConfig(level=logging.INFO)

def rag_dataprocessing_pipeline(folder_path, target_speaker, output_file):


    pairs = []

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        # Skip directories or non-text files
        if not os.path.isfile(file_path) or not file_name.endswith(".txt"):
            continue

        logging.info(f"Processing file: {file_name}")

        try:
            merged_messages = parse_chat(file_path)
            context_reply = reply_context_chat(merged_messages, target_speaker)
            pairs.append(context_reply)
        except Exception as e:
            logging.error(f"Failed to process {file_name}: {e}")

    try:
        rag_data = create_rag_memory(pairs)
        save_rag_memory(rag_data, output_file)
        logging.info("Data Processing done.")
    except Exception as e:
        logging.error(f"Saving file error: {e}")


    logging.info("All files processed.")