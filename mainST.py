import streamlit as st
import basedecider as bd

#Initialize Chat History
if "history" not in st.session_state:
    #Will store all the models and their mesg
    st.session_state.history={
        "llama-3.1-70b-instruct" : [""], 
        "llama-3.1-8b-instruct" : [""], 
        "llama-3.1-nemotron-nano-8B-v1": [""], 
        "llama-3.3-70b-instruct": [""],
        "mistral-7b-instruct": [""], 
        "mistral-small-3.1": [""],
        "nemotron-3-nano-30b-a3b": [""], 
        "nemotron-3-super-120b-a12b": [""],
        "codestral-22b": [""],
        "gemma-3-27b-it": [""],
        "gpt-oss-20b": [""]
        ,"gpt-oss-120b" : [""]
        ,"granite-3.3-8b-instruct": [""]
        ,"sfr-embedding-mistral": [""]
        ,"nomic-embed-text-v1.5": [""]
        ,"flux.1-dev": [""]
        ,"flux.1-schnell" : [""]
        ,"whisper-large-v3" : [""]
        ,"kokoro": [""]
    }
#Streamlit specific fix
def handle_input():
   
    #Store user prompt
    currModel = st.session_state.AIoption
    #Call model in a async func?
    try:
        if currModel == "whisper-large-v3":
            upload_file = st.session_state.AIAudio
            if upload_file is not None: 
                filePath= "saved_audio" + str(len(st.session_state.history[currModel])) + ".mp3"
                with open(filePath, "wb") as f:
                    f.write(upload_file.getbuffer())
                st.session_state.history[currModel].append("User: inputted" + filePath)
                st.session_state.history[currModel].append(currModel + ": " + bd.audioToText(currModel, filePath))
        elif currModel == "kokoro":
            user_text = st.session_state.widget_input
            st.session_state.history[currModel].append("User: " + user_text)
            filedir = "generate_audio" + str(len(st.session_state.history[currModel])) + ".mp3"
            bd.generateAudio(user_text, currModel, filedir)
            st.session_state.history[currModel].append(currModel + ": " + filedir)
        elif currModel == "flux.1-dev" or currModel == "flux.1-schnell":
            user_text = st.session_state.widget_input
            st.session_state.history[currModel].append("User: " + user_text)
            filedir = "generate_image" + str(len(st.session_state.history[currModel])) + ".png"
            bd.imageCreation(user_text, currModel, filedir)
            st.session_state.history[currModel].append(currModel + ": " + filedir)
        elif st.session_state.AIoption == "sfr-embedding-mistral" or st.session_state.AIoption == "nomic-embed-text-v1.5":
            user_text = st.session_state.widget_input
            st.session_state.history[currModel].append("User: " + user_text)
            filedir = "embeddedtext" + str(len(st.session_state.history[currModel])) + ".txt"
            bd.embedding(user_text, currModel, filedir)
            st.session_state.history[currModel].append(currModel + ": " + filedir)
        else:
            user_text = st.session_state.widget_input
            st.session_state.history[currModel].append("User: " + user_text)
            st.session_state.history[currModel].append(currModel + ": " + bd.talkToModel(user_text,currModel))
    except:
        if currModel == "whisper-large-v3":
            st.session_state.history[currModel].append(currModel + ": " + "Input a valid file pls (mp3 or wav)")
        elif currModel == "kokoro":
            st.session_state.history[currModel].append("User" + ": " + "Error with generating audio, possible API error")
        elif currModel == "flux.1-dev" or currModel == "flux.1-schnell":
            user_text = st.session_state.widget_input
            st.session_state.history[currModel].append("User: " + user_text)
            st.session_state.history[currModel].append("Error: Possible API error with navigator")
        elif st.session_state.AIoption == "sfr-embedding-mistral" or st.session_state.AIoption == "nomic-embed-text-v1.5":
            user_text = st.session_state.widget_input
            st.session_state.history[currModel].append("User: " + user_text)
            st.session_state.history[currModel].append(f"User: Error with file")
        else:
            user_text = st.session_state.widget_input
            st.session_state.history[currModel].append("User: " + user_text)
            st.session_state.history[currModel].append(currModel + ": " + "Error occured with attempting to make contact with a base model")

    st.session_state.widget_input = ""

def main():
    st.title("Navigator AI toolkit")
    keyOfModel = list(st.session_state.history.keys())
    st.session_state.AIoption = st.sidebar.selectbox("Selected Model", keyOfModel)
    with st.container(border=True, width=1920, height="stretch", horizontal=False):
        st.subheader(f"Model: {st.session_state.AIoption}")
        chat_container = st.container(height=400)
        with chat_container:
            current_history = st.session_state.history[st.session_state.AIoption]
            if len(current_history) > 1:
                for i in range(1, len(current_history)):
                    if st.session_state.AIoption == "kokoro":
                        if not current_history[i].startswith("User:"):
                            filePath = current_history[i].split(": ")[1]
                            try:
                                with open(filePath, "rb") as f:
                                    audio_bytes= f.read()
                                
                                st.download_button(
                                    label=f"Download: {filePath}",
                                    data=audio_bytes,
                                    file_name=filePath,
                                    mime="audio/mp3"
                                )
                            except:
                                st.write(f"Audio file at {filePath} not found.")
                        else:
                            st.write(current_history[i])
                    elif st.session_state.AIoption == "flux.1-dev" or st.session_state.AIoption == "flux.1-schnell":
                        if not current_history[i].startswith("User:"):
                            filePath = current_history[i].split(": ")[1]
                            try:
                                st.image(filePath, caption="Generated Image")
                                with open(filePath, "rb") as f:
                                    image_bytes= f.read()
                                
                                st.download_button(
                                    label=f"Download: {filePath}",
                                    data=image_bytes,
                                    file_name=filePath,
                                    mime="image/png"
                                )
                            except:
                                st.write(f"Audio file at {filePath} not found.")
                        else:
                            st.write(current_history[i])
                    elif st.session_state.AIoption == "sfr-embedding-mistral" or st.session_state.AIoption == "nomic-embed-text-v1.5":
                        if not current_history[i].startswith("User:"):
                            filePath = current_history[i].split(": ")[1]
                            try:
                                with open(filePath, "r") as f:
                                    file_content = f.read()
                            
                                st.download_button(
                                    label=f"Download: {filePath}",
                                    data=file_content,
                                    file_name=filePath,
                                    mime="text/plain"
                                )
                            except Exception as e:
                                st.write(f"Error: {str(e)}")
                        else:
                            st.write(current_history[i])
                    else:
                        st.write(current_history[i])
    if(st.session_state.AIoption ==  "whisper-large-v3"):
        st.file_uploader(label = "Upload the audio file you want to translate: ",
            type=['mp3', 'wav'],
            key = "AIAudio",
            on_change=handle_input
    )
    elif(st.session_state.AIoption == "flux.1-dev" or st.session_state.AIoption == "flux.1-schnell"):
        prompt = st.text_input(
            "Describe the image you want to generate", 
            key="widget_input",
            on_change=handle_input
        )
    elif(st.session_state.AIoption == "kokoro"):
        prompt = st.text_input(
            "Type a message you want spoken:", 
            key="widget_input",
            on_change=handle_input
        )
    elif st.session_state.AIoption == "sfr-embedding-mistral" or st.session_state.AIoption == "nomic-embed-text-v1.5":
        prompt =st.text_input(
            "Type a message you want embedded:", 
            key="widget_input",
            on_change=handle_input
        )
    else:
        prompt = st.text_input(
            "ChatArea:", 
            key="widget_input",
            on_change=handle_input
        )
    
    

                


if __name__ == "__main__":
    main()