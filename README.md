# RAG_application-Haystack
- [ ] I have use Haystack framework for building RAG application . Chromadb + OpenAI
<p align="center">
  <img src="rag_page-0001.jpg" width="550" title="hover text">
</p>

### Start with 
pip install -r requirements.txt

### constant.py
- [ ] API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" (paste your OpenAI key here)
- [ ] llm = "gpt-3.5-turbo-0125" (OpenAI model you want to use)
- [ ] embedModel = "text-embedding-3-small" (embedding model)
- [ ] template = """ 
-- You are a helpful assistant. Always follow <<Context:>>
-- Please answer the <<Question:>> user asked accordingly. Don't try to generate random answer.

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{question}}
Answer:
""" (Prompt template)

- [ ] DB_FOLDER = 'DB' (ChromaDB location)
