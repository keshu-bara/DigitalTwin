import re

def parse_chat(file_path):

    with open(file_path,"r",encoding = 'utf-8') as f:
        lines = f.readlines()

    messages = []

    merged_messages = []
    current_message = None

    message_pattern = r"^\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}.*?-"

    #raw messages 
    for line in lines:
        line = line.strip()

        if re.match(message_pattern,line):
            timestamp = line.split(' -')[0]
            speaker = line.split(' -')[1].split(':')[0].strip()
            mss = line.split(' -')[1].split(':')[1].strip()


        messages.append({
                        'timestamp':timestamp,
                        'speaker':speaker,
                        'text':mss
                    })

    #mereged messages
    for line in lines:
        line = line.strip()

        if re.match(message_pattern,line):

            timestamp = line.split(' -')[0]
            speaker = line.split(' -')[1].split(':')[0].strip()
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