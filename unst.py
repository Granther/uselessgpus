from unstructured_client import UnstructuredClient
from unstructured_client.models import operations, shared
import os

# client = UnstructuredClient(
#     api_key_auth="EbaLpESG9umX1surY6GXtCJBVVFRzU",
#     server_url="https://api.unstructuredapp.io",
# )

# with open("hello.htm", "rb") as f:
#     files = shared.Files(
#         content=f.read(),
#         file_name="hello.htm"
#     )

# req = operations.PartitionRequest(
#     shared.PartitionParameters(
#         files=files,
#         strategy=shared.Strategy.HI_RES,
#         chunking_strategy="basic",
#         new_after_n_chars=200,
#         max_characters=300
#     )
# )

# print(req)

# from unstructured.partition.html import partition_html
# # Using partition_html to ingest HTML content
# document_elements = partition_html(filename="hello.htm")

# print(document_elements)
# from unstructured.partition.html import partition_html

# url = "https://www.cnn.com/2023/01/30/sport/empire-state-building-green-philadelphia-eagles-spt-intl/index.html"
# elements = partition_html(filename="hello.htm")
# print("\n\n".join([str(el) for el in elements]))

# from unstructured.partition.api import partition_via_api

# filename = "hello.htm"

# elements = partition_via_api(
#   filename=filename, api_key="EbaLpESG9umX1surY6GXtCJBVVFRzU", strategy="auto"
# )

# print(elements)

import requests
from bs4 import BeautifulSoup

htm = requests.get("https://beautiful-soup-4.readthedocs.io/en/latest/")

soup = BeautifulSoup(htm.text, "html.parser")

print(soup.prettify())

print(soup.title)