from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage,AIMessage
import os
key=os.getenv("GPT_KEY")

llm=ChatOpenAI(model="gpt-4o",api_key=key)

chat=[]
sys_msg=SystemMessage(content="You are a helpfull assistant")
chat.append(sys_msg)


while True:
    prompt=input("User:")
    if prompt=="stop":
        break
    human_msg=HumanMessage(content=prompt)
    chat.append(human_msg)
    resp=llm.invoke(chat)
    ai_res=resp.content
    print("AI",ai_res)
    ai_msg=AIMessage(content=ai_res)
    chat.append(ai_msg)


    