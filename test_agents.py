import time
from agent import chat_with_agent as ollama_agent
from langchain_agent import chat_with_agent as langchain_agent


TESTS = [
    "quanti ordini sono in ritardo?",
    "quali sono?",
    "l'ORD-0004 è in ritardo?",
    "quali ordini sono in transito?",
    "quali sono?",
    "quali ordini ci sono il 7 agosto?",
    "dimmi lo stato dell'ORD-0003",
]


def esegui_test(nome, funzione_agente):

    print("\n" + "=" * 70)
    print(nome)
    print("=" * 70)

    tempi = []

    for numero, domanda in enumerate(TESTS, start=1):

        print(f"\nTEST {numero}")
        print(f"Domanda: {domanda}")

        start = time.perf_counter()

        risposta = funzione_agente(domanda)

        end = time.perf_counter()

        tempo = end - start
        tempi.append(tempo)

        print(f"Risposta: {risposta}")
        print(f"Tempo: {tempo:.2f} secondi")

    media = sum(tempi) / len(tempi)

    print("\n" + "-" * 70)
    print(f"Tempo medio {nome}: {media:.2f} secondi")
    print("-" * 70)

    return media


if __name__ == "__main__":

    print("\nBENCHMARK OLLAMA PURO vs LANGCHAIN")

    tempo_ollama = esegui_test(
        "OLLAMA PURO",
        ollama_agent
    )

    tempo_langchain = esegui_test(
        "LANGCHAIN",
        langchain_agent
    )

    print("\n" + "=" * 70)
    print("RISULTATO FINALE")
    print("=" * 70)

    print(f"Ollama puro : {tempo_ollama:.2f} secondi")
    print(f"LangChain   : {tempo_langchain:.2f} secondi")