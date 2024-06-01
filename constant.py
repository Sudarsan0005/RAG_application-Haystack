API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
llm = "gpt-3.5-turbo-0125"
embedModel = "text-embedding-3-small"
template = """
-- You are a helpful assistant. Always follow <<Context:>>
-- Please answer the <<Question:>> user asked accordingly. Don't try to generate random answer.

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{question}}
Answer:
"""

DB_FOLDER = 'DB'