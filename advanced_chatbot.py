from openai import OpenAI
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from gtts import gTTS
import os
from io import BytesIO
from dotenv import load_dotenv
# Load dotenv for picking up creds from .env
load_dotenv()
from advanced_chatbot import chat_llm
import base64

def encode_image(image):
    return base64.b64encode(image).decode('utf-8')

TEMP_AUDIOFILENAME = 'audio_temp.mp3'

### Language - change for accuracy with ASR and TTS - you can change to automatic but you might have issues, especially with accents
language='en'

llm_client = OpenAI(
    api_key= os.getenv("OPENAI_KEY")
)


st.title("💬 LLM, ASR & TTS Chatbot")
st.caption("🚀 A chatbot powered by OpenAI LLM, OpenAI Whisper and OpenAI TTS - ADVANCED AI AGENT")
st.caption("Rather than using a one-liner to call OpenAI, we import a function that handles the messages and skill selection")

AI_MODEL = st.selectbox('Select an AI Model...', [
    'gpt-3.5-turbo',
    'gpt-4',
])
### Function calling not supported with Vision Beta yet
    
if not os.getenv("OPENAI_KEY"): ## Check to see if we have the openai key set or else send back a message
    st.info("Please save your OpenAI API in the .env file in order to continue.")
    st.stop()
    
### Load the memory in the session state if it is not already there
if "memory" not in st.session_state:
### Set some system and assistant prompts
    st.session_state["memory"] = [
        {"role": "system", "content": "You have tools that add more up to date context to queries should they be required, otherwise act as a helpful assistant."},
        ]
### Display our messages in the memory
for msg in st.session_state.memory:
    if 'system' not in msg['role']: ### Hide the system messages because they will contain the skill prompts - you can remove this to check it out :)
        st.chat_message(msg["role"]).write(msg["content"])

## Load our chat widget
CHAT_INPUT = st.chat_input()
AUDIO_INPUT = False

## Load our microphone recorder
audio_bytes = audio_recorder(pause_threshold=180)
if audio_bytes:
    st.audio(audio_bytes, format="audio/mp3")
    # save audio file to mp3
    with open(TEMP_AUDIOFILENAME, "wb") as f:
        f.write(audio_bytes)
    # load the file
    audio_file = open(TEMP_AUDIOFILENAME, "rb")
    # transcribe and set it as the chat input
    AUDIO_INPUT = True
    CHAT_INPUT = llm_client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file,
        language=language
        ).text
    

### Start processing...

if prompt := CHAT_INPUT: ## If we have an input

    ## add the user's entry to memory using the user role
    st.session_state.memory.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    
    ## Open a placeholder with a spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ## Call openai with the memory in order to get a response
            PLACEHOLDER = st.empty() # create an empty placeholder to gather the tokens
            FULL_RESPONSE = '' # create an empty string to keep the full response
            counter = 0
            for token in chat_llm(AI_MODEL, st.session_state.memory): # Get the tokens yielded from the LLM function - ADVANCED
                    FULL_RESPONSE += str(token) ## Add the delta to the full response
                    counter += 1
                    if counter >= 30:
                        PLACEHOLDER.markdown(FULL_RESPONSE) ## Add to the placeholder
                        counter = 0
                    
            PLACEHOLDER.markdown(FULL_RESPONSE) ## Finally update one last time
            
            # Add our bot response to the memory.
            st.session_state.memory.append({"role":"assistant","content": FULL_RESPONSE})
            
            # Play back audio
            if AUDIO_INPUT:
                tts = llm_client.audio.speech.create(
                    model='tts-1',
                    voice='fable',
                    input=FULL_RESPONSE
                )
                tts.stream_to_file(TEMP_AUDIOFILENAME)  # Stream to the temporary file
                
                st.audio(open(TEMP_AUDIOFILENAME,'rb').read(), format='audio/mp3')