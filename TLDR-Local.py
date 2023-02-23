from revChatGPT.V1 import Chatbot
import textwrap
import os, re

def start_agents():
    # read login details from file
    with open('agents.txt', 'r') as f:
        data = f.readlines()
    # create as many chatbot instances as there are logins
    chatbots = []
    for line in data:
        email, password = line.strip().split(',')
        try: 
            chatbot = Chatbot(config={
                "email": email,
                "password": password
            })
            chatbots.append(chatbot)
        except Exception as e: 
            print ("Open AI login details incorrect, please check agents.txt. Ignoring line...",e)
            continue
    return chatbots    

# open the file at the given filepath and return its content
def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()

# function to generate a summary of the input text using the GPT-3 model
def summarise(bot, prompt, filename):
        for data in bot.ask(prompt):
            response = data["message"]
        text = response.strip()
        # remove extra spaces
        text = re.sub('\s+', ' ', text)
        return text
            
if __name__ == '__main__':
    bots = start_agents()

    #set parameters
    input_directory = 'Texts'
    output_directory = 'Summaries'

    # loop through all files in folder
    for filename in os.listdir(input_directory):
        filepath = os.path.join(input_directory, filename)
        text = open_file(filepath)

        # break them down into chunks, 2000 characters each
        chunks = textwrap.wrap(text, 2000)
        count = 0
        index = 0

        print ("Summarising: "+ filename +"...\n")
        
        # loop over the chunks
        for chunk in chunks:

            # read the prompt template and replace the placeholder with the current chunk
            prompt = open_file('prompt.txt').replace('<<TEXT>>', chunk)
            prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()

            # try generate a summary through all available bot instances
            count = count + 1
            success = False
            error_not_yet_shown = True
            while not success:
                try:
                    chatbot = bots[index]
                    if (count % 2 == 0):
                        chatbot.clear_conversations()
                        chatbot.reset_chat()
                except Exception as e:
                    print ("Can't create bot, trying again...")
                    index = (index + 1) % len(bots)  
                try:
                    summary = summarise(chatbot, prompt,filename)
                    summary = summary.replace("---", "\n\n")
                    success = True
                except Exception as not_summarised:
                    if error_not_yet_shown: 
                        print ("Hold tight, retrying until it works...\n")
                        error_not_yet_shown = False
                    index = (index + 1) % len(bots)  
                    success = False
                    with open ('error_log.txt', 'w', encoding = 'utf-8') as f:
                        f.write ("Summarisation failed for: "+filename+" for the following chunk of text:\n\n\""+chunk+"\"\n\n")
                    f.close()

            print('\n\n\n', count, 'of', len(chunks), ' - ', summary)

            # append to and save the summary file in the Summaries/ folder
            with open(os.path.join(output_directory, filename), 'a', encoding='utf-8') as f:
                f.write(summary + '\n\n')
            f.close()
