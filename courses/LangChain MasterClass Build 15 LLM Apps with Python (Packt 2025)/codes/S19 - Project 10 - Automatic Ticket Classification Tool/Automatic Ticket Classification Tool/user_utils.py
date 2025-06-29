#Pinecone team has been making a lot of changes to there code and here is how it should be used going forward :)
from pinecone import Pinecone as PineconeClient
#from langchain.vectorstores import Pinecone     #This import has been replaced by the below one :)
from langchain_community.vectorstores import Pinecone
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
#from langchain.llms import OpenAI #This import has been replaced by the below one :)
from langchain_openai import OpenAI
from langchain.chains.question_answering import load_qa_chain
#from langchain.callbacks import get_openai_callback #This import has been replaced by the below one :)
from langchain_community.callbacks import get_openai_callback
import joblib


#Function to pull index data from Pinecone...
def pull_from_pinecone(pinecone_apikey,pinecone_environment,pinecone_index_name,embeddings):

    PineconeClient(
    api_key=pinecone_apikey,
    environment=pinecone_environment
    )

    index_name = pinecone_index_name

    index = Pinecone.from_existing_index(index_name, embeddings)
    return index

def create_embeddings():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings

#This function will help us in fetching the top relevent documents from our vector store - Pinecone Index
def get_similar_docs(index,query,k=2):

    similar_docs = index.similarity_search(query, k=k)
    return similar_docs

def get_answer(docs,user_input):
    import os
    print(os.getenv('OPENAI_API_KEY'))
    chain = load_qa_chain(OpenAI(api_key=os.getenv('OPENAI_API_KEY')), chain_type="stuff")
    with get_openai_callback() as cb:
        response = chain.run(input_documents=docs, question=user_input)
    return response


def predict(query_result):
    Fitmodel = joblib.load('modelsvm.pk1')
    result=Fitmodel.predict([query_result])
    return result[0]