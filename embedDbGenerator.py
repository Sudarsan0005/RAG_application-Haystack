import os
import sys
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from haystack import Pipeline
from haystack.components.writers import DocumentWriter
from haystack.components.converters import TextFileToDocument
from haystack.components.preprocessors import DocumentSplitter
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from constant import *
os.makedirs(DB_FOLDER, exist_ok=True)


indexing = Pipeline()
document_store = ChromaDocumentStore(persist_path=r'DB',embedding_function='OpenAIEmbeddingFunction',model_name=embedModel,api_key=API_KEY)
indexing.add_component("converter", TextFileToDocument())
indexing.add_component("splitter",DocumentSplitter(split_by="passage", split_length=10, split_overlap=0))
indexing.add_component("writer", DocumentWriter(document_store))
indexing.connect("converter", "splitter")
indexing.connect("splitter", "writer")

def documentStore(file_paths):
    '''Store document to chromaDB'''
    try:
        indexing.run({"converter": {"sources": file_paths}})
    except Exception as e:
        return 0
    return 1

