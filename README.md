# Local-LLM-Logistics-Agent-Ollama-vs-LangChain
Agente AI locale per la gestione di ordini logistici, costruito con Ollama e Qwen3, con tool calling, memoria conversazionale e un benchmark comparativo tra un'implementazione nativa Ollama e una basata su LangChain.

## Descrizione

Il progetto implementa un agente in grado di rispondere a domande in linguaggio naturale su un set di ordini logistici. L'agente interpreta la richiesta dell'utente, seleziona il tool più appropriato tra quelli disponibili e recupera le informazioni direttamente da un dataset CSV.

Esempi di domande gestite:

- "Quanti ordini sono in ritardo?"
- "Quali sono?"
- "L'ORD-0004 è in ritardo?"
- "Quali ordini sono in transito?"
- "Quali ordini ci sono il 7 agosto?"
- "Dimmi lo stato dell'ORD-0003"

La memoria conversazionale consente di gestire domande di follow-up che fanno riferimento al contesto della richiesta precedente (es. "Quali sono?" dopo aver chiesto quanti ordini sono in ritardo).

Sono state realizzate due implementazioni dello stesso agente:

1. **Ollama Native Agent** — implementazione diretta, senza framework intermedi, basata sulle API di tool calling di Ollama.
2. **LangChain Agent** — stessa logica applicativa, realizzata con LangChain, con i tool definiti tramite decoratore `@tool`.

Entrambe le versioni mantengono memoria conversazionale durante la sessione e interrogano lo stesso dataset. Il progetto include uno script di benchmark che esegue la stessa sequenza di domande su entrambe le implementazioni e ne confronta i tempi di risposta.

## Architettura

```
Utente
  │
  ▼
Agente AI
  │
  ├── interpreta la richiesta
  ├── seleziona il tool appropriato
  │
  ▼
Tool
  │
  └── CSV / Pandas
        │
        ▼
  Ordini logistici
```

## Struttura del progetto

```
.
├── agent.py                # Implementazione nativa Ollama
├── langchain_agent.py      # Implementazione LangChain
├── readcsv.py               # Lettura e interrogazione del dataset (versione nativa)
├── readcsv_tool_csv.py       # Tool per l'agente LangChain, definiti con @tool
├── tool_definitions.py       # Schema dei tool esposti all'LLM (versione nativa)
├── test_agents.py            # Script di benchmark
├── orders.csv                 # Dataset di esempio
├── requirements.txt
└── README.md
```

| File | Responsabilità |
|---|---|
| `agent.py` | Gestisce interazione col modello, cronologia della conversazione, tool calling e generazione della risposta finale, senza framework intermedi. |
| `langchain_agent.py` | Reimplementa la stessa logica dell'agente utilizzando LangChain. |
| `readcsv.py` | Funzioni di lettura e interrogazione del dataset per l'agente nativo. |
| `readcsv_tool_csv.py` | Le stesse interrogazioni esposte come tool LangChain tramite decoratore `@tool`, con schema e docstring che il modello usa per decidere quando e come chiamarli. |
| `tool_definitions.py` | Definisce i tool per l'agente nativo: `cerca_ordine`, `cerca_ordini_per_stato`, `cerca_ordini_per_data`, `conta_ordini_per_stato`. |
| `test_agents.py` | Esegue la stessa sequenza di domande su entrambe le implementazioni e ne misura i tempi di risposta. |

## Requisiti

- Python 3.10 o superiore
- [Ollama](https://ollama.com/) installato e in esecuzione
- Un modello con supporto al tool calling (il progetto utilizza `qwen3:8b`)

## Installazione

```bash
git clone <URL_DEL_REPOSITORY>
cd <NOME_REPOSITORY>

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Scaricare il modello e verificarlo:

```bash
ollama pull qwen3:8b
ollama list
```

Assicurarsi che il servizio Ollama sia in esecuzione prima di avviare l'agente.

## Esecuzione

```bash
python agent.py            # implementazione nativa Ollama
python langchain_agent.py  # implementazione LangChain
```

## Benchmark

```bash
python test_agents.py
```

| Implementazione | Tempo medio di risposta |
|---|---|
| Ollama nativo | 4,45 s |
| LangChain | 24,97 s |

I risultati dipendono da hardware, stato di caricamento del modello, dimensione dei prompt e configurazione utilizzata: vanno considerati rappresentativi dell'ambiente di test, non un dato assoluto sulle due tecnologie.

## Ollama nativo vs LangChain: differenze tecniche

Il divario di tempo osservato non racconta tutta la storia. Le due implementazioni differiscono soprattutto nel modo in cui gestiscono la parte più delicata di un agente: il ciclo di tool calling.

**LangChain** standardizza il parsing delle chiamate ai tool, la validazione degli argomenti (tramite gli schema Pydantic generati dal decoratore `@tool`) e la gestione degli errori quando il modello genera una chiamata malformata. Questo introduce overhead — più livelli di astrazione, più chiamate interne, tempi di risposta più alti — ma rende il comportamento dell'agente più prevedibile e più facile da estendere con tool aggiuntivi o logiche più complesse.

**Ollama nativo**, pur essendo nettamente più veloce nel benchmark, delega quasi interamente al codice applicativo ciò che LangChain fa in automatico: parsing della risposta del modello, validazione dei parametri passati ai tool, gestione dei casi in cui il modello richiede un tool inesistente o con argomenti incompleti, e mantenimento manuale della cronologia della conversazione nel formato atteso dall'API. Con `qwen3:8b` in particolare, il tool calling è meno affidabile su richieste ambigue o su catene di più tool in sequenza: il modello a volte non chiama alcun tool quando dovrebbe, oppure genera argomenti nel formato sbagliato, senza che ci sia un livello di validazione a intercettare l'errore prima che raggiunga la logica applicativa. Questo rende l'implementazione nativa più veloce ma anche più fragile, e il margine di velocità si paga in robustezza e in tempo di sviluppo per gestire i casi limite a mano.

In sintesi, la scelta non è "quale tecnologia è migliore" ma quanto controllo manuale si è disposti a scrivere per ottenere quanta velocità: per un'applicazione piccola e con un numero limitato di tool, come questa, il compromesso nativo è accettabile; scalando il numero di tool o la complessità delle richieste, l'assenza di validazione automatica diventa un rischio più concreto della latenza aggiuntiva di LangChain.

## Sviluppi futuri

Miglioramenti diretti al progetto attuale:

- Livello di validazione degli argomenti anche nell'implementazione nativa, per ridurre la fragilità del tool calling su richieste ambigue
- Retry automatico quando il modello genera una chiamata a tool malformata o inesistente
- Test con modelli diversi da `qwen3:8b` per verificare se il compromesso velocità/affidabilità cambia
- Benchmark esteso non solo sul tempo di risposta ma anche sul tasso di successo delle chiamate ai tool (quante volte il modello sceglie il tool corretto con i parametri corretti)

Estensioni funzionali:

- Nuovi tool logistici (tracciamento spedizioni, creazione e modifica ordini)
- Passaggio da CSV a database relazionale
- Risposte strutturate in formato JSON
- Logging, osservabilità e monitoraggio dell'utilizzo dei token
- Variante basata su LangGraph per gestire flussi multi-step
- Interfaccia web e supporto Docker
- Suite di test automatizzati
