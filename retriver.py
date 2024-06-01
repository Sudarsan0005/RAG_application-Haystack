from haystack.components.embedders import OpenAITextEmbedder
from haystack.utils import Secret
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever
from haystack.components.builders import PromptBuilder
from haystack import Pipeline
from haystack.components.generators import OpenAIGenerator
from constant import *

generator = OpenAIGenerator(api_key=Secret.from_token(API_KEY),model=llm)
text_embedder = OpenAITextEmbedder(api_key=Secret.from_token(API_KEY),model=embedModel)
document_store = ChromaDocumentStore(persist_path=r'DB')
querying = Pipeline()
querying.add_component("query_embedder",text_embedder)
querying.add_component("retriever", ChromaEmbeddingRetriever(top_k=2,document_store=document_store))
prompt_builder = PromptBuilder(template=template)
querying.add_component("prompt_builder", prompt_builder)
querying.add_component("llm", generator)
querying.connect("query_embedder.embedding", "retriever.query_embedding")
querying.connect("retriever", "prompt_builder.documents")
querying.connect("prompt_builder", "llm")

def _responseGenerator(question):
    "Retrive related ans from chromaDB and pass through OpenAI and generate response"
    try:
        response = querying.run({"query_embedder": {"text": question}, "prompt_builder": {"question": question}})
    except Exception as e:
        print("Error>>>While Generating response>>")
        return e
    return response["llm"]["replies"][0]