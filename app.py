import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
.stApp {
    background-color: #0E1117;
}

.main-title{
    text-align:center;
    font-size:55px;
    font-weight:bold;
    color:white;
    margin-bottom:10px;
}

.sub-title{
    text-align:center;
    color:#9CA3AF;
    margin-bottom:30px;
}

.chat-container{
    max-width:900px;
    margin:auto;
}

[data-testid="stChatInput"]{
    position: fixed;
    bottom: 20px;
    width: 65%;
}

.stChatMessage{
    border-radius:15px;
    padding:10px;
}

.user-msg{
    background:#2563EB;
    padding:12px;
    border-radius:12px;
    color:white;
}

.ai-msg{
    background:#1F2937;
    padding:12px;
    border-radius:12px;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------
st.markdown(
    '<div class="main-title">🤖 AI Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Powered by GPT-4o • LangChain • Streamlit</div>',
    unsafe_allow_html=True
)

# ------------------ OPENAI ------------------
key = os.getenv("GPT_KEY")

llm = ChatOpenAI(
    model="gpt-4o",
    api_key=key
)

# ------------------ SESSION ------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        SystemMessage(content="You are a helpful AI Assistant")
    ]

# ------------------ DISPLAY CHAT ------------------
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(
                f'<div class="user-msg">{msg.content}</div>',
                unsafe_allow_html=True
            )

    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(
                f'<div class="ai-msg">{msg.content}</div>',
                unsafe_allow_html=True
            )

# ------------------ INPUT ------------------
prompt = st.chat_input("💬 Ask me anything...")

if prompt:

    st.session_state.messages.append(
        HumanMessage(content=prompt)
    )

    with st.chat_message("user"):
        st.markdown(
            f'<div class="user-msg">{prompt}</div>',
            unsafe_allow_html=True
        )

    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            response = llm.invoke(st.session_state.messages)
            answer = response.content

            st.markdown(
                f'<div class="ai-msg">{answer}</div>',
                unsafe_allow_html=True
            )

    st.session_state.messages.append(
        AIMessage(content=answer)
    )