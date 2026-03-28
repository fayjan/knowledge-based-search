import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter # Updated import
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough


load_dotenv()

class RAGEngine:
    def __init__(self):
        # Initializing models
        self.embeddings = OpenAIEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.2)
        self.vectorstore = None
        
        # Assignment-specific prompt
        self.template = """
        Using only the following documents, answer the user's question succinctly.
        If you don't know the answer, say "Information not found in documents."
        
        Context: {context}
        Question: {question}
        
        Answer:"""

    def ingest_docs(self, file_paths):
        all_docs = []
        for path in file_paths:
            loader = PyPDFLoader(path)
            all_docs.extend(loader.load())
        
        # Split text into chunks for better search accuracy
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        chunks = text_splitter.split_documents(all_docs)
        
        # Create a temporary local vector database
        self.vectorstore = Chroma.from_documents(
            documents=chunks, 
            embedding=self.embeddings
        )

    def query_knowledge_base(self, user_input):
        if not self.vectorstore:
            return "Error: No documents have been indexed yet."
        
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        qa_prompt = PromptTemplate.from_template(self.template)
        
        # Build a simple retrieval chain
        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | qa_prompt
            | self.llm
        )
        
        response = chain.invoke(user_input)
        return response.content