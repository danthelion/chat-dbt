import os
from pathlib import Path

import weaviate
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()

docs = []
metadatas = []
for p in Path("docs.getdbt.com/website/docs/docs").rglob("*"):
    if p.is_dir():
        continue
    with open(p) as f:
        docs.append(f.read())
        metadatas.append({"source": p})

text_splitter = CharacterTextSplitter(
    separator="\n",
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
)

documents = text_splitter.create_documents(docs, metadatas=metadatas)

WEAVIATE_URL = os.environ["WEAVIATE_URL"]
client = weaviate.Client(
    url=WEAVIATE_URL,
    additional_headers={"X-OpenAI-Api-Key": os.environ["OPENAI_API_KEY"]},
)

client.schema.get()
schema = {
    "classes": [
        {
            "class": "Paragraph",
            "description": "A written paragraph",
            "vectorizer": "text2vec-openai",
            "moduleConfig": {
                "text2vec-openai": {
                    "model": "ada",
                    "modelVersion": "002",
                    "type": "text",
                }
            },
            "properties": [
                {
                    "dataType": ["text"],
                    "description": "The content of the paragraph",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": False,
                            "vectorizePropertyName": False,
                        }
                    },
                    "name": "content",
                },
                {
                    "dataType": ["text"],
                    "description": "The link",
                    "moduleConfig": {
                        "text2vec-openai": {
                            "skip": True,
                            "vectorizePropertyName": False,
                        }
                    },
                    "name": "source",
                },
            ],
        },
    ]
}

try:
    client.schema.create(schema)
except weaviate.exceptions.UnexpectedStatusCodeException as e:
    if e.status_code == 422:
        print("Schema already exists, deleting and recreating")
        client.schema.delete_class("Paragraph")
        client.schema.create(schema)

with client.batch as batch:
    for text in documents:
        print(f"Adding batch from source: {text.metadata['source']}")
        batch.add_data_object(
            {"content": text.page_content, "source": str(text.metadata["source"])},
            "Paragraph",
        )
