import re 
import json 
import os

def parse_chat(file_path):
    with open(file_path,"r",encoding = 'utf-8') as f:
        lines = f.readlines()

    messages = []

    merged_messages = []
    current_message = None

    message_pattern = r"^\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}.*?-"

    # #raw messages 
    # for line in lines:
    #     line = line.strip()

    #     if re.match(message_pattern,line):
    #         timestamp = line.split(' -')[0]
    #         speaker = line.split(' -')[1].split(':')[0].strip()
    #         mss = line.split(' -')[1].split(':')[1].strip()


    #     messages.append({
    #                     'timestamp':timestamp,
    #                     'speaker':speaker,
    #                     'text':mss
    #                 })

    #mereged messages
    for line in lines:
        line = line.strip()

        if re.match(message_pattern,line):


            timestamp = line.split(' -')[0]
            
            speaker = line.split(' -')[1].split(':')[0].strip()
            
            if len(line.split(' -')[1].split(':')) != 2:
                continue
            mss = line.split(' -')[1].split(':')[1].strip()
            

            if mss == "<Media omitted>":
                continue
            
        
        
            if current_message:
                if current_message['speaker'] == speaker and timestamp.split(',')[0] == current_message['timestamp'].split(',')[0]:
                    current_message['text'] = current_message['text'] + '\n' + mss
        
                else:
                    merged_messages.append(current_message)
                
                    current_message = {
                        'timestamp':timestamp,
                        'speaker':speaker,
                        'text':mss
                    }
            else:

                current_message = {
                    'timestamp':timestamp,
                    'speaker':speaker,
                    'text':mss
                }
        else:
            continue

    merged_messages.append(current_message)

    return merged_messages

def reply_context_chat(merged_messages,TARGET_SPEAKER):
    # Context , reply 
    context_reply = []

    for i in range(1, len(merged_messages)):

        previous = merged_messages[i-1]
        current = merged_messages[i]

        if (
            current["speaker"] == TARGET_SPEAKER
            and previous["speaker"] != TARGET_SPEAKER
        ):
            context = previous["text"]
            reply = current["text"]

            context_reply.append({'context':context,'reply':reply})

    return context_reply

def prepare_data(pairs):

    rag_data = []

    for p in pairs:
        for pair in p:
            context = pair["context"].strip()
            reply = pair["reply"].strip()


            if len(reply.split()) < 3:
                continue #removing low_quality replies


            rag_data.append({
                "instruction": "Reply like Keshav talking to close_friend in casual Hinglish",
                "input": context,
                "output": reply,
            })

    return rag_data
    

def save_rag_memory(rag_data,file_path):
    with open(file_path,"w",encoding = "utf-8") as f:
        json.dump(rag_data,f,indent= 2, ensure_ascii = False)

    print("RAG memory units created:", len(rag_data))
