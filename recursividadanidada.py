def guardar_juguetes(caja):
    # TAREA 1: etiquetar la caja y las cajas de adentro
    print(f"🏷️  Poniendo etiqueta a: {caja['nombre']}")
    
    for cosa in caja["adentro"]:
        if cosa["tipo"] == "juguete":
            print(f"    🧸 Guardando: {cosa['nombre']}")
        else:  # es otra caja
            guardar_juguetes(cosa)   # <-- RECURSIÓN: entro a la caja de adentro


# Nuestras cajas
mi_cuarto = {
    "nombre": "Caja grande del clóset",
    "tipo": "caja",
    "adentro": [
        {"tipo": "juguete", "nombre": "Pelota"},
        {
            "tipo": "caja",
            "nombre": "Caja mediana (bajo la cama)",
            "adentro": [
                {"tipo": "juguete", "nombre": "Carrito"},
                {
                    "tipo": "caja",
                    "nombre": "Cajita pequeña",
                    "adentro": [
                        {"tipo": "juguete", "nombre": "Canica"},
                        {"tipo": "juguete", "nombre": "Estampa"},
                    ],
                },
            ],
        },
    ],
}

guardar_juguetes(mi_cuarto)