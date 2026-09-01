'''cd /Users/bengala/Desktop/solarCV
source .venv/bin/activate'''


from langchain.agents import create_agent
from langchain_ollama import ChatOllama
from langgraph.checkpoint.memory import InMemorySaver

from readcsv_tool_csv import (
    cerca_ordine,
    cerca_ordini_per_stato,
    conta_ordini_per_stato,
    cerca_ordini_per_data
)


model = ChatOllama(
    model="qwen3:8b",
    temperature=0,
    num_predict=512,
    keep_alive="5m",
    think=False
)


tools = [
    cerca_ordine,
    cerca_ordini_per_stato,
    conta_ordini_per_stato,
    cerca_ordini_per_data
]

checkpointer = InMemorySaver() #conversazione memoria


# print(conta_ordini_per_stato.args_schema.model_json_schema()) #debug analisi richiesta

agent = create_agent(
    model=model,
    tools=tools,
    checkpointer=checkpointer,
    system_prompt="""
Sei un assistente specializzato nella gestione degli ordini logistici.

REGOLE:
- Rispondi esclusivamente sulla base dei dati restituiti dai tool.
- Non inventare informazioni.
- Non fornire consigli o suggerimenti sulla gestione degli ordini.
- Non proporre azioni che non puoi eseguire.
- Non chiedere all'utente se vuole "gestire", "modificare" o "intervenire" sugli ordini.
- Puoi fornire ulteriori informazioni sugli ordini presenti nel database se richieste dall'utente.
- Rispondi in modo sintetico e professionale.
- Se l'informazione richiesta non è presente nel database, dichiaralo chiaramente.
"""
)




def chat_with_agent(user_input):

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        },
        config={
            "configurable": {
                "thread_id": "utente_1"
            }
        }
    )

    return response["messages"][-1].content



if __name__ == "__main__":

    print("Agente LangChain avviato! Scrivi 'exit' per uscire.\n")

    while True:

        user_input = input("Tu: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Chat terminata.")
            break

        response = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            },
            #thread per identificare la memoria conversazione
            config={
                "configurable": {
                    "thread_id": "utente_1"
                }
            }
        )

        #print(response)
        print("Agente:", response["messages"][-1].content)