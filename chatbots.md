# Creating a Basic Chatbot with ASR & TTS Using Streamlit

## Introduction
You now have the opportunity to put your knowledge into action by building a simple chatbot. Keep in mind that these concepts can be applied to a wide range of use-cases. This demonstration will also illustrate how to incorporate Automatic Speech Recognition (ASR) and Text-to-Speech (TTS) capabilities (PLUS GPT-4 VISION!). You can interact with the chatbot through speech input and receive responses in speech format.

## How to Get Started

1. Make sure you have your credentials correctly saved in the .env file. **THE FILE MUST BE ".env" ONLY**
2. Make sure you're running within your venv environment. Use the following commands:

Windows
Run the below under powershell or terminal as admin:
```
Set-ExecutionPolicy RemoteSigned
```
Once that's done you can run the following in VS Code:
```
./venv/scripts/activate.ps1
```
in Cmd you can run
```
c:\pathtovenv\scripts\activate.bat
```

On *nix/mac you can run this command
```
source ./venv/bin/activate
```
2. Once in the environment, run the following command to install all the required modules for this application:
   
   ```
   pip install -r requirements.txt
   ```

## To launch the basic chatbot
The basic chatbot just provides chat functionality with ASR, TTS & Vision. You can run it with the following command:
   ```
   streamlit run 'basic_chatbot.py'
   ```
## To launch the advanced autonomous agent chatbot
The advanced chatbot includes all basic functions (minus vision as it doesnt support functions) in addition to automated function calling of internet and kb skills. 

You can run it with the following command:
   ```
   streamlit run 'advanced_chatbot.py'
   ```
## To launch the OpenAI Assistants & Threads chatbot
The assistant chatbot uses the new OpenAI Assistants and Threads functions.

You can run it with the following command:
   ```
   streamlit run 'chatbot_assistants.py'
   ```

**Please make sure to complete the course before going into this file as i will slowly explain everything**

Feel free to engage in a conversation with the chatbot. You can also customize and enhance the system prompts as needed. This is all about effectively providing input and using the output to your advantage. While we are currently focused on speech, it won't be long before we gain access to using photos and videos as inputs and outputs as well! Have fun, and best of luck with your future endeavors.

Wanis Elabbar