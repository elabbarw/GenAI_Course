from openai import OpenAI
import json
import os
from .search_internet import search_internet
from .search_kb import search_kb
from dotenv import load_dotenv
# Load dotenv for picking up creds from .env
load_dotenv()
llm_client = OpenAI(
        api_key =  os.getenv('OPENAI_KEY')
)
        
def chat_llm(aimodel, incoming_messages):
        """
        Interacts with the OpenAI API to process user messages and provide chatbot responses.

        Since we're streaming the response with function calling, the code for this function is a bigger than the basic chatbot's one liner
        because we have to gather enough tokens to know when a function is needed and then act upon it.

        """

        ### Skills
        skills = json.load(open('./advanced_chatbot/skills.json'))


        
        try: # Try the below or else throw back the error to the chat screen if something goes wrong

                response_generator = llm_client.chat.completions.create( ### We call GPT for the first time with our skills
                        model=aimodel,
                        messages=incoming_messages,
                        temperature=0.7,
                        functions=skills,
                        function_call="auto",
                        stream=True,
                        max_tokens=300
                )
                

                function_call_detected = False ### Add triggers for when a function is needed
                our_functions = False ### Sometimes OpenAI makes up a function name so lets use another trigger
                func_call = {"name": "", "arguments": ""} ## Prepare an empty json for the function name and arguments
                
                for response_chunk in response_generator: ### Start getting the deltas/chunks from the first response...

                        if response_chunk.choices and len(response_chunk.choices) > 0:
                                deltas = response_chunk.choices[0].delta
                                if deltas.function_call:  ### If a function_call value is picked up from the delta
                                        function_call_detected = True ### change trigger to true
                                        if deltas.function_call.name: ### if this delta has a name in the function_call
                                                func_call["name"] = deltas.function_call.name ## save it
                                        if deltas.function_call.arguments: ### if this delta has the arguments in the function_call
                                                func_call["arguments"] += deltas.function_call.arguments ## save the arguments
                                if (
                                        function_call_detected ### If our function trigger is true
                                        and response_chunk.choices[0].finish_reason == "function_call" ### and the response finish_reason says function_call
                                ): ## kick off the process to call the function, get the response and send back to LLM for the final answer
                                        
                                        available_functions = { ### Link function_name values with the actual functions 
                                        "search_internet": search_internet,
                                        "search_kb": search_kb
                                        }

                                        if available_functions.get(func_call["name"]): ## if the function name returned from GPT matches any one of ours
                                                our_functions = True ## it wants to trigger our function so change the trigger to True
                                                function_to_call = available_functions.get(func_call["name"]) ## assign the function to call
                                                function_args = json.loads(func_call["arguments"]) ## assign the function arguments
                                                function_response = function_to_call(**function_args) ## get the response from the function
                                                incoming_messages.append(function_response) ## add the response to the list of messages
                                                
                                                final_response_generator = llm_client.chat.completions.create( ## Call gpt a second time with the added message
                                                                model='gpt-3.5-turbo',
                                                                messages=incoming_messages,
                                                                temperature=0.7,
                                                                stream=True
                                                        )
                                        
                                                
                                                for final_chunk in final_response_generator: ### stream and return the chunks one by one to the chat application 
                                                        if final_chunk.choices and len(final_chunk.choices) > 0:
                                                                final_message_content = final_chunk.choices[0].delta.content
                                                                if final_message_content:
                                                                        yield final_message_content
                                                                        
                                                # Reset flags and function call data after processing the function call
                                                function_call_detected = False
                                                our_functions = False
                                                func_call = {"name": "", "arguments": ""}
                                                continue  # This will move the loop to process the next chunk from response_generator

                                                                        
                                elif deltas.content and not function_call_detected and not our_functions:  ### if a function call is not needed, or a function call was hallucinated...
                                        yield deltas.content ### Send back the normal response.
        except Exception as err: ### if something goes wrong then send the error back to the chat app
                yield err