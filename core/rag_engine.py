import os
import os
from openai import OpenAI
from core.vector_store import build_vector_store, load_vector_store, get_retriever


def _chat_complete(messages, model="gpt-3.5-turbo", temperature=0.3):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(model=model, messages=messages, temperature=temperature)
    return resp.choices[0].message.content.strip()


def format_docs(docs):
    return "\n\n".join([getattr(doc, "page_content", str(doc)) for doc in docs])


def build_rag_chain(transcript: str):
    vector_store = build_vector_store(transcript)
    retriever = get_retriever(vector_store, k=4)
    return {"retriever": retriever}


def load_rag_chain():
    vector_store = load_vector_store()
    retriever = get_retriever(vector_store)
    return {"retriever": retriever}


# def ask_question(rag_chain, question: str) -> str:
#     print(f"Question : {question}")
#     retriever = rag_chain.get("retriever") if isinstance(rag_chain, dict) else rag_chain
#     docs = retriever.get_relevant_documents(question)
#     context = format_docs(docs[:4])

def ask_question(rag_chain, question: str) -> str:
    print(f"Question : {question}")

    retriever = rag_chain.get("retriever") if isinstance(rag_chain, dict) else rag_chain

    docs = retriever.invoke(question)

    context = format_docs(docs[:4])

    # baaki code same rehne do
    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert meeting assistant. Answer the user's question "
                "based ONLY on the meeting transcript context provided below.\n\n"
                "If the answer is not found in the context, say: 'I could not find this information in the meeting transcript.'\n\n"
                "Always be concise and precise. If quoting someone, mention it clearly.\n\n"
                "Context from meeting transcript:\n" + context
            ),
        },
        {"role": "user", "content": question},
    ]

    answer = _chat_complete(messages)
    print(f"answer :{answer}")
    return answer
