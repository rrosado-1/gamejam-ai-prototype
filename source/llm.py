from merchant import Merchant
from langchain_ollama import ChatOllama
from langchain_core import ConversationChain

npc_inventory = [
    {
        "id": 1,
        "name": "Sword",
        "description": "A sharp sword",
        "price": 50,
    },
    {
        "id": 2,
        "name": "Shield",
        "description": "A sturdy shield",
        "price": 30,
    },
    {
        "id": 3,
        "name": "Potion",
        "description": "A healing potion",
        "price": 10,
    }
]

player_inventory = {
    "items": []
}

npc = Merchant(inventory=npc_inventory)
llm = ChatOllama(model="mistral", num_ctx=16384, temperature=0.5).bind_tools(npc.tools)

def chat_llm():
    cchain = ConversationChain()
    chain = npc.prompt | llm
    message = ""
    while(not message == "exit"):
        print("Player Message: ", end=" ")
        message = input()
        result = chain.invoke({"player_message": message})
        print(result.content)
        print(result.tool_calls)

chat_llm()