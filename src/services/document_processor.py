import pypdf
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain_openai.chat_models import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

class DocumentProcessor:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.text_splitter = RecursiveCharacterTextSplitter()
        self.embeddings = OpenAIEmbeddings(self.openai_api_key)
        self.llm = ChatOpenAI(temperature=0,
                              model="gpt-4o-mini",
                              api_key=self.openai_api_key)
        
    def process_document(self, document_path):
        try:
            document = pypdf.PyPDFDocument(document_path)
            text = document.get_text()
            return self.retrieval_qa.process_document(text)
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
            texts = self.text_splitter.split_text(document_text, chunk_size=1000, chunk_overlap=200)
            vector_store = FAISS.from_texts(texts, self.embeddings)
            
            # Create an improved prompt template
            prompt_template = ChatPromptTemplate.from_template("""
                Answer the question based on the provided context. If the answer cannot be found
                in the context, reply with "I cannot find the answer in the provided context."
                
                Context: {context}
                Question: {question}
                
                Answer in a clear and concise manner.
            """)

            # Create retrieval chain with optimized settings
            document_chain = create_stuff_documents_chain(
                llm=self.llm,
                prompt=prompt_template,
            )

            retrieval_chain = create_retrieval_chain(
                retriever=vector_store.as_retriever(
                    search_type="similarity",
                    search_kwargs={"k": 3}
                ),
                combine_documents_chain=document_chain
            )
            
            # Generate and validate answer
            result = retrieval_chain.invoke({
                "question": question,
                "context": document_text
            })
            
            return result.get("answer", "Unable to generate an answer")
            
        except Exception as e:
            raise Exception(f"Error generating answer: {str(e)}")