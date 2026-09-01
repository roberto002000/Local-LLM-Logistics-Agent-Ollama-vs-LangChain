import pandas as pd
from langchain_core.tools import tool

def carica_ordini(percorso_csv):
    df = pd.read_csv(percorso_csv)
    return df


percorso = "ordini.csv"

ordini = carica_ordini(percorso)


def cerca_ordine(numero_ordine):
    """
    Cerca un ordine nel CSV tramite il numero ordine.
    """
    numero_ordine = numero_ordine.upper() 
    risultato = ordini[
        ordini["numero_ordine"].str.upper() == numero_ordine
    ]

    if risultato.empty:
        return "Ordine non trovato"

    return risultato.to_dict(orient="records")



def cerca_ordini_per_stato(stato):
    """Cerca tutti gli ordini che hanno lo stato specificato."""

    stato = stato.lower().strip()

    mappa_stati = {
        "ritardo": "in ritardo",
        "in ritardo": "in ritardo",
        "transito": "in transito",
        "in transito": "in transito",
        "consegnato": "consegnato",
        "non consegnato": "non consegnato",
    }

    stato = mappa_stati.get(stato, stato) 
        
    risultato = ordini[
        ordini["stato"].str.lower().str.strip() == stato
        ]

    if risultato.empty:
        return "Nessun ordine trovato"

    return risultato.to_dict(orient="records")


def conta_ordini_per_stato(stato):
    """Conta quanti ordini hanno lo stato specificato."""

    risultato = ordini[
        ordini["stato"].str.lower() == stato.lower()
    ]

    return len(risultato)

def cerca_ordini_per_data(data):
    """Cerca tutti gli ordini associati alla data specificata."""

    risultato = ordini[
        ordini["data"].astype(str) == str(data)
    ]

    if risultato.empty:
        return "Nessun ordine trovato"

    return risultato.to_dict(orient="records")
