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
2. **LangChain Agent** — stessa logica applicativa, realizzata con LangChain.

Entrambe le versioni mantengono memoria conversazionale durante la sessione e utilizzano lo stesso set di tool per interrogare gli ordini. Il progetto include inoltre uno script di benchmark che esegue la stessa sequenza di domande su entrambe le implementazioni e ne confronta i tempi di risposta.

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

Esempio di flusso di esecuzione:

```
"Quali ordini sono in ritardo?"
        │
        ▼
       LLM
        │
        ▼
cerca_ordini_per_stato("in ritardo")
        │
        ▼
       CSV
        │
        ▼
  ORD-0004, ORD-0008
        │
        ▼
       LLM
        │
        ▼
  Risposta finale
```

## Struttura del progetto

```
.
├── agent.py              # Implementazione nativa Ollama
├── langchain_agent.py    # Implementazione LangChain
├── readcsv.py             # Lettura e interrogazione del dataset ordini
├── tool_definitions.py    # Definizione dei tool esposti all'LLM
├── test_agents.py         # Script di benchmark
├── orders.csv              # Dataset di esempio
├── requirements.txt
└── README.md
```

| File | Responsabilità |
|---|---|
| `agent.py` | Gestisce l'interazione con il modello, la cronologia della conversazione, il tool calling e la generazione della risposta finale, senza framework intermedi. |
| `langchain_agent.py` | Reimplementa la stessa logica dell'agente utilizzando LangChain, per confronto diretto con la versione nativa. |
| `readcsv.py` | Contiene le funzioni per leggere e interrogare il dataset degli ordini. |
| `tool_definitions.py` | Definisce i tool disponibili per l'LLM: `cerca_ordine`, `cerca_ordini_per_stato`, `cerca_ordini_per_data`, `conta_ordini_per_stato`. |
| `test_agents.py` | Esegue la stessa sequenza di domande su entrambe le implementazioni e ne misura i tempi di risposta. |

## Requisiti

- Python 3.10 o superiore
- [Ollama](https://ollama.com/) installato e in esecuzione
- Un modello con supporto al tool calling (il progetto utilizza `qwen3:8b`)

## Installazione

### 1. Clonare il repository

```bash
git clone <URL_DEL_REPOSITORY>
cd <NOME_REPOSITORY>
```

### 2. Creare un ambiente virtuale

```bash
python -m venv .venv
```

Attivarlo:

```bash
# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Installare le dipendenze

```bash
pip install -r requirements.txt
```

### 4. Configurare Ollama

Scaricare il modello utilizzato dal progetto:

```bash
ollama pull qwen3:8b
```

Verificare che sia disponibile:

```bash
ollama list
```

Assicurarsi che il servizio Ollama sia in esecuzione prima di avviare l'agente.

## Esecuzione

Implementazione nativa Ollama:

```bash
python agent.py
```

Implementazione LangChain:

```bash
python langchain_agent.py
```

## Benchmark

Il progetto include uno script di benchmark che esegue la stessa sequenza di domande su entrambe le implementazioni, per confrontarne i tempi di risposta.

```bash
python test_agents.py
```

Risultato ottenuto nell'ambiente di test:

| Implementazione | Tempo medio di risposta |
|---|---|
| Ollama nativo | 4,45 s |
| LangChain | 24,97 s |

Nel test effettuato, l'implementazione nativa Ollama è risultata significativamente più veloce rispetto a quella basata su LangChain.

I risultati del benchmark dipendono da hardware, stato di caricamento del modello, dimensione dei prompt, overhead di esecuzione dei tool e configurazione utilizzata. I valori riportati sono quindi rappresentativi dell'ambiente in cui è stato eseguito il test e non vanno interpretati come una valutazione generale delle due tecnologie.

### Considerazioni sul confronto

| | Ollama nativo | LangChain |
|---|---|---|
| Vantaggi | Minore astrazione, controllo diretto sul ciclo dell'agente, minore complessità architetturale, latenza potenzialmente più bassa | Astrazioni di livello più alto, interfacce standardizzate per i tool, integrazione più semplice in architetture multi-agente più complesse |
| Contesto d'uso ideale | Applicazioni di dimensioni contenute, con un flusso deterministico e la necessità di controllo diretto sul comportamento dell'agente | Sistemi più ampi che beneficiano di un framework maturo e di un ecosistema di strumenti già disponibili |

Per un'applicazione di dimensioni contenute e con un flusso relativamente deterministico come questa, l'approccio nativo risulta più semplice da controllare e da mantenere. Per sistemi più complessi o multi-agente, framework come LangChain o LangGraph possono offrire vantaggi che compensano il maggiore overhead architetturale.

## Tecnologie utilizzate

Python, Ollama, Qwen3, LangChain, Pandas, CSV, tool calling per LLM, agenti conversazionali.

## Sviluppi futuri

- Aggiunta di ulteriori tool logistici (tracciamento spedizioni, creazione e modifica ordini)
- Passaggio da CSV a un database relazionale
- Risposte strutturate in formato JSON
- Logging e osservabilità, monitoraggio dell'utilizzo dei token
- Livello di routing deterministico per la selezione dei tool
- Variante basata su LangGraph
- Interfaccia web
- Supporto Docker
- Suite di test automatizzati

## Licenza

Progetto realizzato a scopo didattico e di portfolio.
