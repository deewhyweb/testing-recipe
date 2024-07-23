
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from rouge_score import rouge_scorer
import streamlit as st
import tempfile
import requests
import json
import time
import os

model_service = os.getenv("MODEL_ENDPOINT",
                          "http://localhost:8001")
model_service = f"{model_service}/v1"

@st.cache_resource(show_spinner=False)
def checking_model_service():
    start = time.time()
    print("Checking Model Service Availability...")
    ready = False
    while not ready:
        try:
            request = requests.get(f'{model_service}/models')
            if request.status_code == 200:
                ready = True
        except:
            pass
        time.sleep(1) 
    print("Model Service Available")
    print(f"{time.time()-start} seconds")

with st.spinner("Checking Model Service Availability..."):
    checking_model_service()
st.title("Bob's Fried Chicken Restaurant")

text = st.text_input("Please enter your restaurant review",value="")

llm = ChatOpenAI(base_url=model_service,
             api_key="not required",
             streaming=True,
             temperature=0.0,
             max_tokens=400,
             )

### prompt example is from  https://python.langchain.com/docs/use_cases/summarization
refine_template = PromptTemplate.from_template(
    "Instructions: Analyze the text and determine if it is positive or negative.\n"
    "------------\n"
    "{text}\n"
    "------------\n"
    "Generate and print a response as if you are a person called Bob Hughes the owner of a restaurant called Bob's fried Chicken restaurant responding to this text as a review of their restaurant"
)

if text:
    answer = ""
    st.write(f"We are reading your review, please wait for a response.")
    response = llm.invoke(refine_template.format(text=text,answer=answer))
    answer = response.content
    st.write(answer)

