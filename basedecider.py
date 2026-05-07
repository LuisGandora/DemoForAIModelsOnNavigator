#Import .env
import os
from dotenv import load_dotenv
load_dotenv()
my_API = os.getenv("LITELLMAPI")
import openai
import base64 #For writing images
import time

#Global Client variable using a litellm openAI proxy to access all models in navigator toolkit
client = openai.OpenAI(
    api_key= my_API,
    base_url="https://api.ai.it.ufl.edu" # LiteLLM Proxy is OpenAI compatible, Read More: https://docs.litellm.ai/docs/proxy/user_keys
)

###
# Create model via a function to return the chat data, returns a string repping the mesg
# Majority of models utilize the openai API
def talkToModel(mesg : str, modelName : str):
    response = ""
    if modelName == "sfr-embedding-mistral" or modelName =="nomic-embed-text-v1.5": #Embedding
        dummy = "This Is Fortnite..."
        responseR = client.embeddings.create(
            model=modelName,
            input = dummy,
            encoding_format="float"
        )
        response = responseR.data[0].embedding
    elif modelName == "flux.1-dev" or modelName == "flux.1-schnell": #Images
        image = """
    Make a image that says hello world
"""
        responseT = client.images.generate(
            model=modelName,
            prompt=image,
            response_format="b64_json"
        )
        image_base64 = responseT.data[0].b64_json
        
        if image_base64:
            images_bytes = base64.b64decode(image_base64)
            with open("outputImage.png", "wb") as f:
                f.write(images_bytes)
            response = "Image successfully written to outputImage.png"
        else:
            response = "Error: No image data received from the server."
    elif modelName == "whisper-large-v3" or modelName == "kokoro": #Audio
        #Turn Audio to text
        audio = open("HelloMesg.mp3", "rb")
        responseL = client.audio.transcriptions.create(
            model=modelName,
            file = audio
        )
        response += responseL.text
    else: # Normal response
        response = client.chat.completions.create(
            model=modelName , # model to send to the proxy
            messages = [
                {
                    "role": "user",
                    "content": "Hello"
                }
            ]
        )
    return response

#Just a test runner using inputs to pick which model a user wants.
def main():
    listOfModels = ["llama-3.1-70b-instruct", 
    "llama-3.1-8b-instruct", 
    "llama-3.1-nemotron-nano-8B-v1", 
    "llama-3.3-70b-instruct",
    "mistral-7b-instruct", #Needs to be checked-Did not run due to UF blocking me
    "mistral-small-3.1",
    "nemotron-3-nano-30b-a3b", 
    "nemotron-3-super-120b-a12b",
    "codestral-22b",
    "gemma-3-27b-it",
    "gpt-oss-20b"
    ,"gpt-oss-120b"
    ,"granite-3.3-8b-instruct"
    ,"sfr-embedding-mistral"
    ,"nomic-embed-text-v1.5"
    ,"flux.1-dev"
    ,"flux.1-schnell" #Does not work
    ,"whisper-large-v3" #Also Errors Out
    ,"kokoro" #Also errors out
    ] # List of all models available under navigator-toolkit
    print("Choose which model you want to communicate with: ")
    try:
        # print(talkToModel(" ", listOfModels[6]))
        for i in range(18, len(listOfModels)):
            print(str(i) + ": " + listOfModels[i])
            print(talkToModel(" ", listOfModels[i]))
            time.sleep(3)
            
        # option = input("Option:")
        # print(talkToModel(" ", listOfModels[int(option)]))
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    main()
