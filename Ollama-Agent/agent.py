import ollama
import json
from validation_controll import determina_tool, valida_stato, valida_numero_ordine
from readcsv import (
    cerca_ordine,
    cerca_ordini_per_stato,
    conta_ordini_per_stato,
    cerca_ordini_per_data
)

conversation_history = []

#ollama rm 'nome_modello' elimina il modello dalla memoria pc


SYSTEM_PROMPT = """
Sei un classificatore di richieste relative agli ordini logistici.

Devi classificare ESCLUSIVAMENTE la richiesta dell'utente presente nell'ULTIMO messaggio.

Non devi utilizzare informazioni provenienti da richieste precedenti.

Gli intent disponibili sono ESATTAMENTE:

- stato_ordine
- dettaglio_ordine
- ordini_per_stato
- conteggio_stato
- ordini_per_data

REGOLE:

1. stato_ordine
Usalo quando l'utente vuole conoscere lo stato di UNO SPECIFICO ordine.

Esempio:
"Dimmi lo stato di ORD-0003"

Risposta:
{
    "intent": "stato_ordine",
    "numero_ordine": "ORD-0003"
}

2. dettaglio_ordine
Usalo quando l'utente vuole informazioni su UNO SPECIFICO ordine.

Esempio:
"Controlla ORD-0003"

Risposta:
{
    "intent": "dettaglio_ordine",
    "numero_ordine": "ORD-0003"
}

3. ordini_per_stato
Usalo quando l'utente vuole sapere QUALI ordini hanno un determinato stato.

Esempio:
"Quali sono gli ordini in ritardo?"

Risposta:
{
    "intent": "ordini_per_stato",
    "stato": "ritardo"
}

4. conteggio_stato
Usalo quando l'utente vuole sapere QUANTI ordini hanno un determinato stato.

Esempio:
"Quanti ordini sono in transito?"

Risposta:
{
    "intent": "conteggio_stato",
    "stato": "in transito"
}

5. ordini_per_data
Usalo quando l'utente vuole cercare ordini associati a una determinata data.

Esempio:
"Cerca gli ordini del 10 agosto"

Risposta:
{
    "intent": "ordini_per_data",
    "data": "2026-08-10"
}

IMPORTANTE:

"Qual è lo stato di ORD-0003?"
→ stato_ordine

"Quali ordini sono in ritardo?"
→ ordini_per_stato

"Quanti ordini sono in ritardo?"
→ conteggio_stato

Rispondi ESCLUSIVAMENTE con JSON valido.
"""


def interpreta_richiesta(user_input):
    #messages è una piccola memoria di archiviazione messaggi
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    response = ollama.chat(
        model="qwen3:8b",
        messages=messages,
        stream=False,
        think=False,
        format="json",
        keep_alive="5m",
        options={
            "temperature": 0,
            "top_p": 0.9,
            "top_k": 40,
            "num_predict": 256,
            "num_ctx": 4096,
            "repeat_penalty": 1.1,
            "seed": 42,
        },
    )

    contenuto = response["message"]["content"]

    return json.loads(contenuto)


def esegui_tool(richiesta):

    intent = richiesta.get("intent")

    tool = determina_tool(intent)

    if tool is None:
        return "Intent non riconosciuto"

    if tool == "cerca_ordine":

        numero_ordine = richiesta.get("numero_ordine")

        numero_ordine = valida_numero_ordine(numero_ordine)

        if numero_ordine is None:
            return "Numero ordine non valido"

        risultato = cerca_ordine(numero_ordine)

        return risultato

    elif tool == "cerca_ordini_per_stato":

        stato = richiesta.get("stato")

        stato = valida_stato(stato)

        if stato is None:
            return "Stato non valido"

        risultato = cerca_ordini_per_stato(stato)

        return risultato

    elif tool == "conta_ordini_per_stato":

        stato = richiesta.get("stato")

        stato = valida_stato(stato)

        if stato is None:
            return "Stato non valido"

        risultato = conta_ordini_per_stato(stato)

        return risultato

    elif tool == "cerca_ordini_per_data":

        data = richiesta.get("data")

        if data is None:
            return "Data non specificata"

        risultato = cerca_ordini_per_data(data)

        return risultato


def genera_risposta(user_input, risultato):

    conversation_history.append({
        "role": "user",
        "content": user_input
    })

    messages = [
        {
            "role": "system",
            "content": """
Sei un assistente logistico.

Rispondi utilizzando esclusivamente le informazioni
presenti nei risultati forniti dal database.

Non inventare informazioni.

Rispondi in modo chiaro e sintetico.
"""
        }
    ]

    messages.extend(conversation_history)

    messages.append({
        "role": "user",
        "content": f"""
Risultato del database:
{risultato}
"""
    })

    response = ollama.chat(
        model="qwen3:8b",
        messages=messages,
        stream=False,
        think=False,
        keep_alive="5m",
        options={
            "temperature": 0,
            "top_p": 0.9,
            "top_k": 40,
            "num_predict": 256,
            "num_ctx": 4096,
            "repeat_penalty": 1.1,
            "seed": 42,
        },
    )

    risposta = response["message"]["content"]

    conversation_history.append({
        "role": "assistant",
        "content": risposta
    })

    return risposta

def chat_with_agent(user_input):

    richiesta = interpreta_richiesta(user_input)

    risultato = esegui_tool(richiesta)

    risposta = genera_risposta(user_input, risultato)

    return risposta


if __name__ == "__main__":

    print("Chat avviata! Scrivi 'exit' per uscire.\n")

    while True:

        user_input = input("Tu: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Chat terminata.")
            break

        risposta = chat_with_agent(user_input)

        print("Agente:", risposta)