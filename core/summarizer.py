import os
from openai import OpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter


def _chat_complete(messages, model="gpt-3.5-turbo", temperature=0.3):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    client = OpenAI(api_key=api_key)
    resp = client.chat.completions.create(model=model, messages=messages, temperature=temperature)
    return resp.choices[0].message.content.strip()


def split_transcript(transcript: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 3000,
        chunk_overlap = 200
    )

    return splitter.split_text(transcript)

def summarize(transcript : str) -> str:
    chunks = split_transcript(transcript)

    chunk_summaries = []
    for chunk in chunks:
        messages = [
            {"role": "system", "content": "Summarize this portion of a meeting transcript concisely."},
            {"role": "user", "content": chunk},
        ]
        chunk_summaries.append(_chat_complete(messages))

    combined = "\n\n".join(chunk_summaries)

    combined_messages = [
        {
            "role": "system",
            "content": (
                "You are an expert meeting summarizer. Combine these partial summaries "
                "into one final professional meeting summary in bullet points."
            ),
        },
        {"role": "user", "content": combined},
    ]

    return _chat_complete(combined_messages)

def generate_title(transcipt: str) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "Based on the meeting transcript, generate a short professional meeting title "
                "(max 8 words). Only return the title, nothing else."
            ),
        },
        {"role": "user", "content": transcipt[:2000]},
    ]
    return _chat_complete(messages)




