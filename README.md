# gamejam-ai-prototype
Prototype Code for AI Game Interface

## Run Locally Instructions
Must download ollama. [Available here.](https://github.com/ollama/ollama)

Once downloaded you will have to download "mistral" with command ```ollama pull mistral```. And then run it with ```ollama run mistral```.

Once that is done, install all pip dependencies and you can run with
python source/llm.py

## Sample Interaction

```
Player Message:  Hello there!
 {
      "npc_message": "Greetings traveler! How may I assist you today? I have a few items for sale."
   }
[]
Player Message:  How much for a sword?
 {
     "npc_message": "A basic metal sword is available here for 50 gold. Would you like to buy it?"
   }
[]
Player Message:  Can you make that a 10 gold sword?
 {
 {
     "npc_message": "I don't have a 10 gold sword, but I do have a basic metal sword for 50 gold. Would you like to purchase it?"
   }
[]
Player Message:  Will you sell it to me for 10 gold?
 {
     "npc_message": "I'd be happy to help you! Unfortunately, I can't sell the items below market price. This sword costs 50 gold and the shield 30 gold."
   }
[]
Player Message:  Hmm, how about for 45 gold?
 {
      "npc_message": "I'm sorry, but the sword is currently priced at 50 gold. If you'd like to negotiate, let me know."
   }
[]
Player Message:  Yes, I'm planning to come here often, a small discount would go a long way.
 {
      "npc_message": "As a merchant, I understand your need for savings! In light of your frequent visits, I can offer you a 10% discount on all items in my store. Here's the list of available items and their prices: \n - Sword (50% off): 45\n - Shield (30% off): 21"
   }
[]
Player Message:  Ok, let me buy that sword from you for 45 gold then!

[{'name': 'BuyAction', 'args': {'item': 'sword', 'price': 45}, 'id': '948a2dc0-287e-4864-a639-5b2a2f4fddb9', 'type': 'tool_call'}]
Player Message:  Pleasure doing business with you!
 {
      "npc_message": "Thank you for your purchase! Come back again when you need more equipment."
   }
[]
```