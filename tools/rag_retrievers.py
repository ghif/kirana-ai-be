from dotenv import load_dotenv
load_dotenv()

import os

from vertexai import rag
import vertexai

from langchain_core.tools import tool

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCP_LOCATION_ID = os.getenv("GCP_LOCATION_ID")
RAG_CORPUS_ID = os.getenv("RAG_CORPUS_ID")

vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION_ID)

@tool(response_format="content_and_artifact")
def retrieve_from_vertex_rag_engine(query: str):
    """
    Retrieve documents from Vertex RAG engine based on the provided query.
    
    Args:
        query (str): The query to search for in the RAG corpus.
        
    Returns:
        response: The response containing retrieved contexts.
    """
    corpus_name = f"projects/{GCP_PROJECT_ID}/locations/{GCP_LOCATION_ID}/ragCorpora/{RAG_CORPUS_ID}"

    response = rag.retrieval_query(
        rag_resources=[
            rag.RagResource(
                rag_corpus=corpus_name,
                # Optional: supply IDs from `rag.list_files()`.
                # rag_file_ids=["rag-file-1", "rag-file-2", ...],
            )
        ],
        text=query,
        rag_retrieval_config=rag.RagRetrievalConfig(
            top_k=20,
            filter=rag.utils.resources.Filter(vector_distance_threshold=0.5),
        ),
    )

    serialized_docs = "\n\n".join(
        (f"Filename: {context.source_display_name}\n" f"URI: {context.source_uri}\n" f"Content: {context.text}")
        for context in response.contexts.contexts
    )
    
    return serialized_docs, response.contexts.contexts

# corpus_name = f"projects/{GCP_PROJECT_ID}/locations/{GCP_LOCATION_ID}/ragCorpora/{RAG_CORPUS_ID}"

# query = "What are the latest research findings on education aid?"
# response = rag.retrieval_query(
#     rag_resources=[
#         rag.RagResource(
#             rag_corpus=corpus_name,
#             # Optional: supply IDs from `rag.list_files()`.
#             # rag_file_ids=["rag-file-1", "rag-file-2", ...],
#         )
#     ],
#     text=query,
#     rag_retrieval_config=rag.RagRetrievalConfig(
#         top_k=5,
#         filter=rag.utils.resources.Filter(vector_distance_threshold=0.5),
#     ),
# )
# print(response)

# serialized_docs = "\n\n".join(
#     (f"Filename: {context.source_display_name}\n" f"URI: {context.source_uri}\n" f"Content: {context.text}")
#     for context in response.contexts.contexts
# )

# for i, context in enumerate(response.contexts.contexts):
#     print(f"### [{i + 1}] ###")
#     print(f"Display Name: {context.source_display_name}")
#     print(f"Context URI: {context.source_uri}")
#     print(f"Score: {context.score}")
#     print(f"Text : {context.text[:500]}\n")
#     print("-" * 40)

    