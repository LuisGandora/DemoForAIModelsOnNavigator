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
        responseR = client.embeddings.create(
            model=modelName,
            input = mesg,
            encoding_format="float"
        )
        response = responseR.data[0].embedding
    elif modelName == "flux.1-dev" or modelName == "flux.1-schnell": #Images
        responseT = client.images.generate(
            model=modelName,
            prompt=mesg,
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
    elif modelName == "whisper-large-v3": #Audio
        #Turn Audio to text
        audio = open("HelloMesg.mp3", "rb")
        responseL = client.audio.transcriptions.create(
            model=modelName,
            file = audio
        )
        response += responseL.text
    elif modelName == "kokoro": # Text-to-Speech
        with client.audio.speech.with_streaming_response.create(
            model=modelName,
            voice="alloy", # Kokoro usually requires a voice parameter
            input="Say Hello",   # The text you want spoken
            instructions="Speak in a monotone voice"
        ) as response_audio:
            response_audio.stream_to_file("outputAudio.mp3")
        response = "Audio successfully written to outputAudio.mp3"
    else: # Normal response
        responseT = client.chat.completions.create(
            model=modelName , # model to send to the proxy
            messages = [
                {
                    "role": "user",
                    "content": mesg
                }
            ]
        )
        response = responseT.choices[0].message.content
    return response

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
