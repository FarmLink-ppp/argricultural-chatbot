from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv("API_KEY")
print(api_key)
# Initialize the language model
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # You can specify other versions if needed
    temperature=0.1,
    max_output_tokens=512,
    google_api_key=api_key # replace with your actual Google API Key
)

# Set up the retrieval QA chain
def setup_retrieval_qa(db):
    retriever = db.as_retriever(similarity_score_threshold=0.1)

    # Define the prompt template
    prompt_template = """Your name is AgriGenius. Please answer questions related to a website. Try explaining in simple words. Answer in less than 100 words. try answer any user question understand the context of the question.
    You are a helpful assistant. Use the context provided to answer the question. try understand the data i gave you and match it with the user prompt i mean search for the information '
    CONTEXT: {context}
    QUESTION: {question}"""

    PROMPT = PromptTemplate(template=f"[INST] {prompt_template} [/INST]", input_variables=["context", "question"])

    # Initialize the RetrievalQA chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever,
        input_key='query',
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
        verbose=True
    )
    return chain
