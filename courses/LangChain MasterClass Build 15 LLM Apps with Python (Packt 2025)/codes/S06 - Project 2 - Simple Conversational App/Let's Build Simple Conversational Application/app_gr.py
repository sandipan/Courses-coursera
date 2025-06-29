#import streamlit as st
import gradio as gr

#As Langchain team has been working aggresively on improving the tool, we can see a lot of changes happening every weeek,
#As a part of it, the below import has been depreciated
#from langchain.chat_models import ChatOpenAI

#New import from langchain, which replaces the above
from langchain_openai import ChatOpenAI

#import os
#os.environ["OPENAI_API_KEY"] = ""


from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

# From here down is all the StreamLit UI
#st.set_page_config(page_title="LangChain Demo", page_icon=":robot:")
#st.header("Hey, I'm your Chat GPT")



#if "sessionMessages" not in st.session_state:
#     st.session_state.sessionMessages = [
#        SystemMessage(content="You are a helpful assistant.")
#    ]



def load_answer(question, chat_msgs):

    #st.session_state.sessionMessages.append(HumanMessage(content=question))
    chat_msgs.append(SystemMessage(content="You are a helpful assistant."))
    chat_msgs.append(HumanMessage(content=question))
    assistant_answer  = chat.invoke(chat_msgs)
    #st.session_state.sessionMessages.append(AIMessage(content=assistant_answer.content))
    chat_msgs.append(AIMessage(content=assistant_answer.content))
    return assistant_answer.content


chat = ChatOpenAI(temperature=0)

#user_input=get_text()
#submit = st.button('Generate')  

#if submit:
    
#    response = load_answer(user_input)
#    st.subheader("Answer:")

#    st.write(response)

chat_msgs = []

def respond(text):
    response = load_answer(text, chat_msgs)
    return f"Answer:{response}"

demo = gr.Interface(fn=respond, inputs=gr.Textbox(label="Generate"), outputs="text")

if __name__ == "__main__":
    demo.launch()