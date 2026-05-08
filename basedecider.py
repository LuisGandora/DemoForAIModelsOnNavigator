#Import .env
import os
from dotenv import load_dotenv
load_dotenv()
my_API = os.getenv("LITELLMAPI")
import openai
import base64 #For writing images
import time
import streamlit as st

#Global Client variable using a litellm openAI proxy to access all models in navigator toolkit
client = openai.OpenAI(
    api_key= st.secrets["LITELLMAPI"],
    base_url="https://api.ai.it.ufl.edu" # LiteLLM Proxy is OpenAI compatible, Read More: https://docs.litellm.ai/docs/proxy/user_keys
)

###
# Create model via a function to return the chat data, returns a string repping the mesg
# Majority of models utilize the openai API
def talkToModel(mesg : str, modelName : str):
    response = client.chat.completions.create(
        model=modelName , # model to send to the proxy
        messages = [
            {
                "role": "user",
                "content": mesg
            }
        ]
    )
    return response.choices[0].message.content

#For "whisper-large-v3", audio to text
def audioToText(modelName: str, input: str):
    #Turn Audio to text
    audio = open(input, "rb") #Default, later a path would be included
    responseL = client.audio.transcriptions.create(
        model=modelName,
        file = audio
    )
    return responseL.text

#For "kokoro", text to speech, doesnt return filepath
def generateAudio(mesg: str, modelName: str, filePath:  str):
    with client.audio.speech.with_streaming_response.create(
        model=modelName,
        voice="alloy", # Kokoro usually requires a voice parameter
        input=mesg,   # The text you want spoken
        instructions="Speak in a monotone voice"
    ) as response_audio:
        response_audio.stream_to_file(filePath)
    

#For "flux.1-dev" or "flux.1-schnell", text to images
def imageCreation(mesg: str, modelName : str, filePath: str):
    responseT = client.images.generate(
        model=modelName,
        prompt=mesg,
        response_format="b64_json"
    )
    image_base64 = responseT.data[0].b64_json
    if image_base64:
        images_bytes = base64.b64decode(image_base64)
        with open(filePath, "wb") as f:
            f.write(images_bytes)
    
#For "sfr-embedding-mistral" or "nomic-embed-text-v1.5", for embedding text into images
def embedding(mesg: str, modelName :str, filePath: str):
    responseR = client.embeddings.create(
        model=modelName,
        input = mesg,
        encoding_format="float"
    )
    vec = responseR.data[0].embedding
    with open(filePath, "w") as f:
        f.write(str(vec))

#Just a test runner using inputs to pick which model a user wants.
# def main():
#     listOfModels = [
#     "llama-3.1-70b-instruct", 
#     "llama-3.1-8b-instruct", 
#     "llama-3.1-nemotron-nano-8B-v1", 
#     "llama-3.3-70b-instruct",
#     "mistral-7b-instruct", 
#     "mistral-small-3.1",
#     "nemotron-3-nano-30b-a3b", 
#     "nemotron-3-super-120b-a12b",
#     "codestral-22b",
#     "gemma-3-27b-it",
#     "gpt-oss-20b"
#     ,"gpt-oss-120b"
#     ,"granite-3.3-8b-instruct"
#     ,"sfr-embedding-mistral"
#     ,"nomic-embed-text-v1.5"
#     ,"flux.1-dev"
#     ,"flux.1-schnell" 
#     ,"whisper-large-v3" 
#     ,"kokoro" #Also errors out
#     ] # List of all models available under navigator-toolkit
#     print("Choose which model you want to communicate with: ")
#     try:
#         for i in range(18, len(listOfModels)):
#             print(str(i) + ": " + listOfModels[i])
            
#         option = input("Option:")
#         print(talkToModel(" ", listOfModels[int(option)]))
#     except Exception as e:
#         print(str(e))

# if __name__ == "__main__":
#     main()
