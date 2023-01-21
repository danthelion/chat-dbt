# chat-dbt

This repo is an implementation of a chatbot specifically focused on question answering over
the [dbt documentation](https://docs.getdbt.com/docs/introduction).
It is based on the amazing [chat-langchain](https://github.com/hwchase17/chat-langchain).

## 🚀 Important Links

Blog Post about the original
langchain-chat library: [blog.langchain.dev/langchain-chat/](https://blog.langchain.dev/langchain-chat/)

## 📚 Technical description

There are two components: ingestion and question-answering.

Ingestion has the following steps:

1. Clone the dbt documentation repository
2. Split documents with
   LangChain's [TextSplitter](https://langchain.readthedocs.io/en/latest/modules/utils/combine_docs_examples/textsplitter.html)
3. Create a vectorstore of embeddings, using
   LangChain's [vectorstore wrapper](https://langchain.readthedocs.io/en/latest/modules/utils/combine_docs_examples/vectorstores.html) (
   with OpenAI's embeddings and Weaviate's vectorstore)

Question-Answering has the following steps:

1. Given the chat history and new user input, determine what a standalone question would be (using GPT-3)
2. Given that standalone question, look up relevant documents from the vectorstore
3. Pass the standalone question and relevant documents to GPT-3 to generate a final answer

## Running locally

1. Clone the dbt documentation repository

```bash
git clone git@github.com:dbt-labs/docs.getdbt.com.git
```

2. Add your OPENAI_API_KEY to an .env file

```bash
mv .env.example .env
```

3. Run the app

```bash
docker-compose up
```


