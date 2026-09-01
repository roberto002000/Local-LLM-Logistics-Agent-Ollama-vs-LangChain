import re


STATI_VALIDI = {
    "consegnato": "consegnato",
    "in transito": "in transito",
    "transito": "in transito",
    "ritardo": "in ritardo",
    "in ritardo": "in ritardo",
    "non consegnato": "non consegnato"
}

def valida_stato(stato):

    stato = stato.lower().strip()

    if stato in STATI_VALIDI:
        return STATI_VALIDI[stato]

    return None

def valida_numero_ordine(numero_ordine):

    numero_ordine = numero_ordine.upper().strip()

    if re.fullmatch(r"ORD-\d{4}", numero_ordine):
        return numero_ordine

    return None


INTENT_TO_TOOL = {
    "stato_ordine": "cerca_ordine",
    "dettaglio_ordine": "cerca_ordine",
    "ordini_per_stato": "cerca_ordini_per_stato",
    "conteggio_stato": "conta_ordini_per_stato",
    "ordini_per_data": "cerca_ordini_per_data"
}


def determina_tool(intent):

    return INTENT_TO_TOOL.get(intent)

