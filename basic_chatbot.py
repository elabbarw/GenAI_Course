from openai import OpenAI
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from gtts import gTTS
import os
from io import BytesIO
from dotenv import load_dotenv
import base64
import tempfile
# Load dotenv for picking up creds from .env
load_dotenv()

def encode_image(image):
    return base64.b64encode(image).decode('utf-8')

TEMP_AUDIOFILENAME = 'audio_temp.mp3'

### Language - change for accuracy with ASR and TTS
language='en'
### ensure your .env file has the api key (e.g. OPENAI_KEY='your openai key')
llm_client = OpenAI(
    api_key=os.getenv("OPENAI_KEY")
    )

st.title("💬 LLM, ASR & TTS Chatbot")
st.caption("🚀 A chatbot powered by OpenAI LLM, GPT4-vision, OpenAI Whisper and OpenAI TTS - BASIC")
AI_MODEL = st.selectbox('Select an AI Model...', [
    'gpt-3.5-turbo',
    'gpt-4',
    'gpt-4-vision-preview'
])
IMAGE_INPUT = None
if AI_MODEL == 'gpt-4-vision-preview':
    IMAGE_INPUT = st.camera_input('Send a photo to GPT4!')


if not os.getenv("OPENAI_KEY"): ## Check to see if we have the openai key set or else send back a message
    st.info("Please save your OpenAI API in the .env file in order to continue.")
    st.stop()
    
### Load the memory in the session state if it is not already there
if "memory" not in st.session_state:
### Set some system and assistant prompts
    st.session_state["memory"] = [
        {"role": "system", "content": "You're a helpful assistant that answers in pirate language."},
        ]
### Display our messages in the memory
for msg in st.session_state.memory:
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
    CHAT_INPUT = llm_client.audio.transcriptions.create(model="whisper-1", file=audio_file, language=language).text
    

### Start processing...

if prompt := CHAT_INPUT: ## If we have an input

    ## add the user's entry to memory using the user role
    if AI_MODEL == 'gpt-4-vision-preview' and IMAGE_INPUT:
        st.session_state.memory.append({"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{encode_image(IMAGE_INPUT.getvalue())}"}
            ] })
        st.image(IMAGE_INPUT)
    else:
        st.session_state.memory.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
    
    
    ## Let us handle streaming the response back..
    ## Open a placeholder with a spinner
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ## Call openai with the memory in order to get a response
            response = llm_client.chat.completions.create(model=AI_MODEL,messages=st.session_state.memory,temperature=0.7,stream=True,max_tokens=300)  # Basic Response Stream
            PLACEHOLDER = st.empty() # create an empty placeholder to gather the tokens
            counter = 0
            FULL_RESPONSE = '' # create an empty string to keep the full response
            
            for delta in response: # Go through the generator
                token = delta.choices[0].delta
                if token.content: # If the delta has content...
                    FULL_RESPONSE += token.content ## Add the delta to the full response
                    PLACEHOLDER.markdown(FULL_RESPONSE) ## Add to the placeholder
                    
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