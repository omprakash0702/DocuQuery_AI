import asyncio
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from openai import AsyncOpenAI
from rag_utils import chunk_text
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# OpenAI client
client = AsyncOpenAI()

# FREE embeddings (local)
embedder = SentenceTransformer("all-MiniLM-L6-v2")


class State(TypedDict):
    text: str
    chunks: List[str]
    vectors: list
    vectordb: any
    query: str
    answer: str


async def chunk_node(state: State):
    state["chunks"] = chunk_text(state["text"])
    return state


async def embed_node(state: State):
    if not state["chunks"]:
        state["chunks"] = [state["text"][:1000]]

    vectors = embedder.encode(state["chunks"]).astype("float32")

    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors)

    state["vectors"] = vectors
    state["vectordb"] = index
    return state


async def answer_node(state: State):
    # Embed query
    q_vec = embedder.encode([state["query"]]).astype("float32")
    D, I = state["vectordb"].search(q_vec, 3)

    ctx = "\n\n".join([state["chunks"][i] for i in I[0]])

    # Call OpenAI LLM
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Answer based only on the provided context."},
            {"role": "user", "content": f"Context:\n{ctx}\n\nQuestion: {state['query']}"}
        ],
    )

    # FIXED: new API format uses .content
    state["answer"] = response.choices[0].message.content
    return state


graph = StateGraph(State)
graph.add_node("chunk", chunk_node)
graph.add_node("embed", embed_node)
graph.add_node("answer", answer_node)

graph.set_entry_point("chunk")
graph.add_edge("chunk", "embed")
graph.add_edge("embed", "answer")
graph.add_edge("answer", END)

app = graph.compile()


def run_rag_sync(text, query):
    state = {"text": text, "query": query}
    return asyncio.run(app.ainvoke(state))
