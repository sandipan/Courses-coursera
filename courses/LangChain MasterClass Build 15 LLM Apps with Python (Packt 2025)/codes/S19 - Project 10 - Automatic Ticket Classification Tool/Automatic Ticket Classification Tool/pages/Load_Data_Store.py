import streamlit as st
from dotenv import load_dotenv
from pages.admin_utils import *


def main():
    load_dotenv()
    st.set_page_config(page_title="Dump PDF to Pinecone - Vector Store")
    st.title("Please upload your files...📁 ")

    # Upload the pdf file...
    pdf = st.file_uploader("Only PDF files allowed", type=["pdf"])

    # Extract the whole text from the uploaded pdf file
    if pdf is not None:
        with st.spinner('Wait for it...'):
            text=read_pdf_data(pdf)
            st.write("👉Reading PDF done")

            # Create chunks
            docs_chunks=split_data(text)
            #st.write(docs_chunks)
            st.write("👉Splitting data into chunks done")

            # Create the embeddings
            embeddings=create_embeddings_load_data()
            st.write("👉Creating embeddings instance done")

            # Build the vector store (Push the PDF data embeddings)
            #Recent changes by langchain team, expects ""PINECONE_API_KEY" environment variable for Pinecone usage! So we are creating it here
            import os
            os.environ["PINECONE_API_KEY"] = ""
            push_to_pinecone(os.getenv("PINECONE_API_KEY"),"gcp-starter","tickets",embeddings,docs_chunks)

        st.success("Successfully pushed the embeddings to Pinecone")


if __name__ == '__main__':
    main()
