tools = [
    {
        "type": "function",
        "function": {
            "name": "cerca_ordine",
            "description": "Cerca un ordine nel CSV tramite il numero ordine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "numero_ordine": {
                        "type": "string", #evita di trasformare ord-001 in ord-1
                        "description": "Numero identificativo dell'ordine, ad esempio ord-001."
                    }
                },
                "required": ["numero_ordine"]
            }
        }
    },

    {   
        "type": "function",
        "function": {
            "name": "conta_ordini_per_stato",
            "description": "Conta quanti ordini hanno lo stato specificato.",
            "parameters": {
                "type": "object",
                "properties": {
                    "stato": {
                        "type": "string",
                        "description": "Stato dell'ordine, ad esempio ritardo o consegnato."
                    }
                },
                "required": ["stato"] 
            }
        }  
    },

    {
        "type": "function",
        "function": {
            "name": "cerca_ordini_per_stato",
            "description": "Cerca tutti gli ordini che hanno lo stato specificato.",
            "parameters": {
                "type": "object",
                "properties": {
                    "stato": {
                        "type": "string",
                        "description": "Stato dell'ordine, ad esempio ritardo o consegnato."
                    }
                },
                "required": ["stato"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "cerca_ordini_per_data",
            "description": "Cerca tutti gli ordini associati alla data specificata.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "string",
                        "description": "Data dell'ordine nel formato YYYY-MM-DD."
                    }
                },
                "required": ["data"]
            }
        }
    }
]