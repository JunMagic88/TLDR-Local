# TLDR-Local
chatGPT-powered summariser that can be run locally for large documents

## Setup
1. Install Python: https://www.python.org/
2. Create several chatGPT accounts: https://chat.openai.com/chat (recommend to create 5 for optimum speed, but even just one will still work)
3. Download or git clone this repository to a local folder of your choice
```python
git clone https://github.com/JunMagic88/TLDR-local.git
```
4. Open the **TLDR-Local.py** file and replace the add your OpenAI API key to the line:
```llm = ChatOpenAI(openai_api_key="sk-xxxxxxxxxxx",temperature=0,model_name="gpt-3.5-turbo")```

5. Navigate to the TLDR-Local folder via **Terminal (Mac)** or **Command Prompt (Windows)** and run: 
```python
pip install -r requirements
```

## Adding texts to summarise
1. Add any **.txt** **.pdf** or **.epub**files to summarise in the **/Books** folder 

## Let's TLDR!
1. Run this to convert all files in **/Books** into **.txt** and save them in the **/Texts** folder
```python
python parse.py
```
2. Run this to start the summarisation. The summarised chunks are saved in **/Summaries** folder. If anything happens that caused the summariser to stop (e.g. your internet got disconnected or chatGPT is down), you can check the **error_log.txt** file to see where it got up to. Delete the files and text already summarised and run it again to continue. To stop it from running at any time, just press **Ctrl + C**
```python
python TLDR-Local.py
```
Note: if you see {'detail': 'Too many requests in 1 hour. Try again later.'}, just ignore it, it will keep retrying until it works.

## (Advanced) Custom Prompt 
- You can change the prompt to your own liking by updating the **promp.txt** file. This is the instruction set to chatGPT. Make sure to keep the <\<TEXT\>> tag so it can load the text in at run time.
