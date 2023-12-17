from openai import OpenAI
from qdrant_client import QdrantClient
from gptrim import trim
from dotenv import load_dotenv
import os
# Load dotenv for picking up creds from .env
load_dotenv()
# Load the vectordb
qdrant_client = QdrantClient(
    url=os.getenv('VECTORDB_ENDPOINT'), 
    api_key=os.getenv('VECTORDB_KEY'),
)
llm_client = OpenAI(
    api_key=os.getenv('OPENAI_KEY')
)
def search_kb(query):

    response = llm_client.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )

    embeddings = response.data[0].embedding

    search_result = str(qdrant_client.search(
        collection_name="books",
        query_vector=embeddings, 
        limit=5
    )
)
    search_prompt = f"""
        Based on the knowledge base snippets provided in <>, provide an answer to the query [] if it is relevant along with a source. \
        If there are no snippets or if they are not relevant then say \"Please try again.\"\
        
        context:<{trim(search_result)}>
        query:[{query}]
        """
    
    return {"role":"system","content": search_prompt}