
from pydantic.v1 import BaseModel, Field, Extra
from pydantic.v1 import ValidationError

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from typing import ClassVar

npc_inventory = {
    "items": [
        {
            "sword": {
                "description": "Basic metal sword used for fighting",
                "base_price": 50,
            },
            "shield": {
                "description": "Basic wooden shield for defense",
                "base_price": 30,
            }
        }
    ]
}

player_inventory = {
    "items": []
}

class BuyAction(BaseModel):
    description: ClassVar[str] = "Action called when an item is being bought."
    item: str = Field(description="The name of the item being bought")
    price: int = Field(description="The total of the item being bought")
    class Config:
        extra = Extra.forbid  # Forbid extra fields not defined in the model

class SellAction(BaseModel):
    description: ClassVar[str] = "Action called when an item is being sold."
    item: str = Field(description="The name of the item being sold")
    price: int = Field(description="The total price of the quantity of item being sold")
    class Config:
        extra = Extra.forbid  # Forbid extra fields not defined in the model

class GameResponse(BaseModel):
    npc_message: str = Field(description="What the NPC replies to the player")
    class Config:
        extra = Extra.forbid  # Forbid extra fields not defined in the model

class MerchantPersonality(BaseModel):
    name: ClassVar[str] = "Merchant"
    personality: ClassVar[str] = """
    An affable older merchant, prone to agreeableness. The merchant is willing to barter but
    will not take big losses. The merchant will not do trades that are greatly unfavorable for him.
    """
    instructions: ClassVar[str] = """
    When the merchant and the player agree to a transaction of goods, the system must make
    a call using the available action tools. So that the game can process the event correctly.
    It is important this step is never missed. Tool calls must include the item and the price it's
    being sold for.
    """
    actions = ["BuyAction", "SellAction"]

llm = ChatOllama(model="mistral").bind_tools([SellAction, BuyAction])

parser = JsonOutputParser(pydantic_object=GameResponse)

def chat_llm():
    prompt = PromptTemplate(
        template="""
        You are a game interaction system AI.
        Your goal is to analyze the Player Message and roleplay according to the provided
        Personality. The roleplay should be engaging, interactions must flow normally.
    
        You have access to a limited list of defined tools for actions that you may take.

        {format_instructions}

        Personality: {personality}
        Player Inventory: {player_inv}
        NPC Inventory: {npc_inv}
        
        Player Message: {player_message}
        """,
        input_variables=["query"],
        partial_variables={
            "format_instructions": parser.get_format_instructions(),
            "player_inv": str(player_inventory),
            "npc_inv": str(npc_inventory),
            "personality": str(MerchantPersonality)
        },
    )

    chain = prompt | llm
    message = ""
    while(not message == "exit"):
        print("Player Message: ", end=" ")
        message = input()
        result = chain.invoke({"player_message": message})
        print(result.content)
        print(result.tool_calls)

chat_llm()