
from datasets import load_dataset

# With CassIO, the engine powering the Astra DB integration in LangChain,
# you will also initialize the DB connection:
import os
from dotenv import load_dotenv

from langchain.text_splitter import CharacterTextSplitter
# from langchain_ollama import OllamaLLM
# from langchain_ollama import OllamaEmbeddings
# from cassandra.cluster import Cluster

from langchain_community.vectorstores import Cassandra
from langchain.indexes.vectorstore import VectorStoreIndexWrapper

from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings

import cassio
from cassio.config import init
load_dotenv()
os.environ["ASTRA_DB_KEY"] = os.getenv("ASTRA_DB_KEY")
os.environ["ASTRA_DB_ID"] = os.getenv("ASTRA_DB_ID")
cassio.init(token=os.getenv("ASTRA_DB_KEY"), database_id=os.getenv("ASTRA_DB_ID"))


from astrapy import DataAPIClient

llm = OpenAI(openai_api_key="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")
embedding = OpenAIEmbeddings(openai_api_key="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")
astra_vector_store = Cassandra(
   embedding=embedding,
   table_name="pdf_vector_store",
   session=None,
   keyspace=None,
)


# We need to split the text using Character Text Split such that it sshould not increse token size
text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 800,
    chunk_overlap  = 200,
    length_function = len,
)


def writeDataToDB(raw_text):
    print("Write Data to DB is executing ... !")
    texts = text_splitter.split_text(raw_text)
    astra_vector_store.add_texts(texts[:50])
    print("Inserted %i headlines." % len(texts[:50]))
    astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)



astra_vector_index = VectorStoreIndexWrapper(vectorstore=astra_vector_store)
def readDataFromDB(query_text):
    print("\nQUESTION: \"%s\"" % query_text)
    answer = astra_vector_index.query(query_text, llm=llm).strip()
    print("ANSWER: \"%s\"\n" % answer)

    print("FIRST DOCUMENTS BY RELEVANCE:")
    for doc, score in astra_vector_store.similarity_search_with_score(query_text, k=4):
        print("    [%0.4f] \"%s ...\"" % (score, doc.page_content[:100]))
    return answer
      