__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import os
from tavily import TavilyClient
import requests
from unstructured_ingest.connector.local import SimpleLocalConfig
from unstructured_ingest.interfaces import PartitionConfig, ProcessorConfig, ReadConfig
from unstructured_ingest.runner import LocalRunner
from langchain_community.document_loaders import JSONLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import chromadb
from uuid import uuid4
from pprint import pprint
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

search = "Tell me about golden retrievers"
collection_name = "rags"
file_path = "./local-ingest-output/pysocket.html.json"
out_dir = "./out"

def query_col(query: str, collection_name: str, n_results: int = 1):
    persistent_client = chromadb.PersistentClient()
    collection = persistent_client.get_or_create_collection(collection_name)

    res = collection.query(query_texts=[query], n_results=n_results)
    
    return res

def download_url(url: str, out_dir: str):
    r = requests.get(url)
    open(out_dir + "/" + str(uuid4()) + ".html", "wb").write(r.content)

def partition(html_dir: str, out_dir: str):
    runner = LocalRunner(
        processor_config=ProcessorConfig(
            verbose=True,
            output_dir=out_dir,
            num_processes=2,
        ),
        read_config=ReadConfig(),
        partition_config=PartitionConfig(
            partition_by_api=True,
            api_key="EbaLpESG9umX1surY6GXtCJBVVFRzU",
            partition_endpoint="https://api.unstructuredapp.io/general/v0/general",
        ),
        connector_config=SimpleLocalConfig(
            input_path=html_dir,
            recursive=True,
        ),
    )
    runner.run()

def embed_json(json_path: str, collection_name: str):
    loader = JSONLoader(file_path=json_path, jq_schema=".[]", text_content=False)
    documents = loader.load()
    persistent_client = chromadb.PersistentClient()
    collection = persistent_client.get_or_create_collection(collection_name)
    langchain_chroma = Chroma(
        client=persistent_client,
        collection_name=collection_name,
        embedding_function=embeddings
    )

    uuids = [str(uuid4()) for _ in range(len(documents))]

    langchain_chroma.add_documents(documents=documents, ids=uuids)

if __name__ == "__main__":
    client = TavilyClient(api_key="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")
    response = client.search(search, search_depth="basic", topic="general", max_results=1)

    for item in response['results']:
        download_url(item['url'], out_dir=out_dir)

    partition(out_dir, "./partitioned")

    for file in os.listdir("./partitioned"):
        embed_json("./partitioned/" + file, "dogs")

    print(query_col("How long do golden retrievers live", "dogs"))



