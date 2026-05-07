import streamlit as st
import basedecider as bd

#Initialize Chat History
if "history" not in st.session_state:
    #Will store all the models and their mesg
    st.session_state.history={
        "llama-3.1-70b-instruct" : ["", "llama-3.1-70b-instruct: Yo"], 
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
    user_text = st.session_state.widget_input
    if user_text:
        #Store user prompt
        currModel = st.session_state.AIoption
        st.session_state.history[currModel].append("User: " + user_text)
        #Call model in a async func?
        st.session_state.history[currModel].append(currModel + ": " + bd.talkToModel(user_text,currModel))
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
                    st.write(current_history[i])
    prompt = st.text_input(
        "ChatArea:", 
        key="widget_input",
        on_change=handle_input
    )
    

                


if __name__ == "__main__":
    main()