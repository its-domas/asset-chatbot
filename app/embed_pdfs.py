import glob
import os
from dotenv import load_dotenv
load_dotenv()

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma 
from langchain.embeddings.openai import OpenAIEmbeddings

# Load all PDF files from the 'data' folder
pdf_files = glob.glob('data/*.pdf')
documents = []

for pdf_file in pdf_files:
    loader = PyPDFLoader(pdf_file)
    docs = loader.load()
    for doc in docs:
        # Add metadata (optional)
        doc.metadata['source'] = pdf_file
    documents.extend(docs)

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(documents)

# Generate embeddings and store them persistently
embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory='./vectorstore'
)
