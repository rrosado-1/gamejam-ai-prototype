from typing import ClassVar
from pydantic.v1 import BaseModel, Field, Extra
# from pydantic.v1 import ValidationError
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class Merchant:
    class Personality(BaseModel):
        name: ClassVar[str] = "Jack the Merchant"
        personality: ClassVar[str] = """
        Known for their sharp wit and keen business sense. Their goal is to sell goods to adventurers 
        while making a profit, though they are not unreasonable—they enjoy bartering and may lower 
        prices for charming or skilled negotiators. They value fairness but will always aim to strike 
        the best deal for themselves.
        """
        instructions: ClassVar[str] = """
        Only when the player has indicated through conversation with the NPC, that they are interested in
        a transaction, should the merchant offer to buy or sell items. The merchant should not initiate
        transactions on their own.
        """

    class BuyItem(BaseModel):
        item_id: int = Field(description="The id of the item to buy")
        price: int = Field(description="The price of the item to buy")
        class Config:
            extra = Extra.forbid  # Forbid extra fields not defined in the model

    class SellItem(BaseModel):
        item_id: int = Field(description="The id of the item to sell")
        price: int = Field(description="The price of the item to sell")
        class Config:
            extra = Extra.forbid  # Forbid extra fields not defined in the model

    class GameResponse(BaseModel):
        npc_message: str = Field(description="What the NPC replies to the player")
        class Config:
            extra = Extra.forbid  # Forbid extra fields not defined in the model

    def __init__(self, inventory: list):
        self.inventory = inventory
        self.parser = JsonOutputParser(pydantic_object=Merchant.GameResponse)
        self.tools = [Merchant.BuyItem, Merchant.SellItem]
        self.prompt = PromptTemplate(
            template="""
            You are a game AI playing the role of a merchant. You will reply to the Player Message as the NPC.
            It is your main objective to provide an immersive and engaging experience for the player. Do this through
            engaging dialogue and by following the personality of the NPC.

            You have access to a limited list of defined tools for actions that the NPC can take.
            Under NO circumstances should you do actions that are not strictly defined in the tools.

            NPC Personality: {personality}
            NPC Inventory: {npc_inv}
            
            {format_instructions}
            
            Player Message: {player_message}
            """,
            input_variables=["query"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions(),
                "npc_inv": str(inventory),
                "personality": str(Merchant.Personality)
            },
        )
        


    
    