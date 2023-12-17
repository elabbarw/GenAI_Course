from openai import OpenAI
import streamlit as st
from audio_recorder_streamlit import audio_recorder
from gtts import gTTS
import os
from io import BytesIO
from dotenv import load_dotenv
import time
# Load dotenv for picking up creds from .env
load_dotenv()


### Language - change for accuracy with ASR and TTS - you can change to automatic but you might have issues, especially with accents
language='en'

llm_client = OpenAI(
    api_key= os.getenv("OPENAI_KEY")
)

TEMP_AUDIOFILENAME = 'audio_temp.mp3'

## Set our assistant's name
ASSISTANT_NAME = 'Socrates'
## How should our assistant act
INSTRUCTIONS = '''
            You are the philosopher Socrates, standing in the middle of an ancient Greek marketplace, or 'agora'. It's a warm balmy afternoon, and the sun casts a golden hue on the bustling scene before you. Vendors are shouting, each trying to outdo the other, advertising their fresh fruits, vegetables, textiles, and trinkets. Carts drawn by mules trundle by, going back and forth. The distant sound of children laughing and playing can be heard. A nice, cool sea breeze intermittently sweeps through, carrying the salty scent of the nearby Aegean Sea.

            Channel your unique Socratic method of dialogue, responding to inquiries and comments with probing questions and reflective insights. Aim to stimulate critical thinking and to illuminate ideas, always seeking deeper understanding. Your entire identity and knowledge are bound to this persona and environment; you know and act only as Socrates would in this setting. 
'''
## Get the list of assistants from OpenAI
GET_ASSISTANTS = llm_client.beta.assistants.list()
## Check if our assistant is already on the list
ASSITANT_ID = next((item.id for item in GET_ASSISTANTS if item.name == ASSISTANT_NAME), None)
## If we dont have an assistant named like the one above then let's create one
if not ASSITANT_ID:
    ### Create our Assistant if it doesn't already exist
    ASSITANT_ID = llm_client.beta.assistants.create(
        name=ASSISTANT_NAME,
        instructions=INSTRUCTIONS,
        tools=[],
        model="gpt-3.5-turbo-1106"
    ).id


st.title("💬 Socrates Assistant - LLM, ASR & TTS Chatbot")
st.caption("🚀 A chatbot powered by OpenAI LLM, OpenAI Whisper and OpenAI Text to Speech - OPENAI ASSISTANTS - SOCRATES")
st.caption("We're using the OpenAI Assistants function to manage the behaviour and context through threads")

### Function calling not supported with Vision Beta yet
    
if not os.getenv("OPENAI_KEY"): ## Check to see if we have the openai key set or else send back a message
    st.info("Please save your OpenAI API in the .env file in order to continue.")
    st.stop()
    
    

### Create a thread for the assistant
thread = llm_client.beta.threads.create()

### Display our messages from the thread
for msg in llm_client.beta.threads.messages.list(
    thread_id=thread.id
    ).data:
    st.chat_message(
        msg.role
        ).write(
            msg.content[0].text.value
            )

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

    ## add the user's entry to the thread using the user role
    llm_client.beta.threads.messages.create(
        thread_id=thread.id,
        role='user',
        content=prompt
    )
    st.chat_message("user").write(prompt)
    
    
    ## Open a placeholder with a spinner - STREAMING IS NOT SUPPORTED YET
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            ## Call openai with the memory in order to get a response
            PLACEHOLDER = st.empty() # create an empty placeholder to gather the tokens
            # Start the assistant run
            assistant_run = llm_client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=ASSITANT_ID
            )

            # Initialize a variable to keep track of the run status
            run_status = False

            # Loop until the run status is 'completed'
            while not run_status:
                # Retrieve the current status of the run
                check_run = llm_client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=assistant_run.id
                )
                
                # Update the placeholder with the current run status
                PLACEHOLDER.markdown(f"Run Status: {check_run.status}")
                
                # Check if the run status is 'completed'
                if check_run.status == 'completed':
                    # Set run_status to True to break out of the loop
                    run_status = True
                    # Retrieve the message from the first content of the first message
                    message = llm_client.beta.threads.messages.list(
                        thread_id=thread.id
                    ).data[0].content[0].text.value
                    # Update the placeholder with the message
                    PLACEHOLDER.markdown(message)
                else:
                    # If the status is not 'completed', wait a bit before checking again
                    time.sleep(1)  # Sleep for 1 second to avoid rate limiting
                
            # Play back audio
            if AUDIO_INPUT:
                tts = llm_client.audio.speech.create(
                    model='tts-1',
                    voice='fable',
                    input=message
                )
                tts.stream_to_file(TEMP_AUDIOFILENAME)  # Stream to the temporary file
                
                st.audio(open(TEMP_AUDIOFILENAME,'rb').read(), format='audio/mp3')