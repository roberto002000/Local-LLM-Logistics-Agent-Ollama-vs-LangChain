import pandas as pd
from langchain_core.tools import tool
from typing import Literal

def carica_ordini(percorso_csv):
    df = pd.read_csv(percorso_csv)
    return df


percorso = "ordini.csv"

ordini = carica_ordini(percorso)


@tool
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


@tool
def cerca_ordini_per_stato(stato: str):
    """
    Cerca tutti gli ordini che hanno lo stato specificato.
    """

    stato = stato.lower().strip()

    if stato in ["ritardo", "ritardato", "in ritardo"]:
        stato = "in ritardo"

    risultato = ordini[
        ordini["stato"].str.lower() == stato
    ]

    if risultato.empty:
        return "Nessun ordine trovato"

    return risultato.to_dict(orient="records")


@tool
def conta_ordini_per_stato(stato: str):
    """
    Conta quanti ordini hanno lo stato specificato.
    """

    stato = stato.lower().strip()

    if stato in ["ritardo", "ritardato", "in ritardo"]:
        stato = "in ritardo"

    risultato = ordini[
        ordini["stato"].str.lower() == stato
    ]

    return len(risultato)

@tool
def cerca_ordini_per_data(data):
    """Cerca tutti gli ordini associati alla data specificata."""

    risultato = ordini[
        ordini["data"].astype(str) == str(data)
    ]

    if risultato.empty:
        return "Nessun ordine trovato"

    return risultato.to_dict(orient="records")