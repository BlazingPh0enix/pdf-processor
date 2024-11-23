import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
from langchain.chains import RetrievalQA  # Add this import

load_dotenv()

class DocumentProcessor:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.text_splitter = RecursiveCharacterTextSplitter()
        # Fix the embeddings initialization
        self.embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
        # Fix the ChatOpenAI initialization and model name
        self.llm = ChatOpenAI(
            temperature=0,
            model="gpt-4o-mini",  # Changed from "gpt-4o-mini" to a valid model name
            api_key=self.openai_api_key
        )
        
    def process_document(self, file_object):
        try:
            # Create a PDF reader object from file object
            pdf_reader = PyPDF2.PdfReader(file_object)
            
            # Extract text from all pages
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            raise Exception(f"An error occurred while processing the document: {str(e)}")

    def create_vector_store(self, text: str):
        texts = self.text_splitter.split_text(text)
        return FAISS.from_texts(texts, self.embeddings)
    
    def answer_question(self, document_text: str, question: str) -> str:
        if not document_text or not question:
            raise ValueError("Document text and question cannot be empty")

        try:
            # Create vector store with optimized chunk size
            texts = self.text_splitter.split_text(document_text)
            vector_store = FAISS.from_texts(texts, self.embeddings)
            
            # Create an improved prompt template
            prompt_template = ChatPromptTemplate.from_template("""
                Answer the question based on the provided context. If the answer cannot be found
                in the context, reply with "I cannot find the answer in the provided context."
                
                Context: {context}
                Question: {question}
                
                Answer in a clear and concise manner.
            """)

            # Create QA chain using RetrievalQA
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 3}
                ),
                return_source_documents=False,
                chain_type_kwargs={
                    "prompt": prompt_template
                }
            )
            
            # Generate answer
            result = qa_chain.invoke({"query": question})
            return result.get("result", "Unable to generate an answer")
            
        except Exception as e:
            raise Exception(f"Error generating answer: {str(e)}")