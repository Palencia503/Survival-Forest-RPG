import os
import json
from Personaje import Personaje, Pocion

RUTA_GUARDADO = "Dades/Partida.json"

#GUARDAR
def guardar_partida(personaje):
    #Convierte pociones(objetos) a diccionarios
    pociones_guardar = []
    for pocion in personaje.inventario["pociones"]:
        pociones_guardar.append({
            "nombre": pocion.nombre,
            "mana": pocion.mana,
            "cura": pocion.cura,
            "buff_ataque": pocion.buff_ataque,
            "cantidad": pocion.cantidad,
            "icono_path": pocion.icono_path
        })

    datos = {
        "clase": personaje.clase,
        "hp": personaje.hp,
        "hp_max": personaje.hp_max,
        "mana": personaje.mana,
        "mana_max": personaje.mana_max,
        "escudo": personaje.escudo,
        "escudo_base": personaje.escudo_base,
        "defensa_base": personaje.defensa_base,
        "ataque": personaje.ataque,
        "dinero": personaje.dinero,
        "exp": personaje.exp,
        "exp_necesaria": personaje.exp_necesaria,
        "nivel": personaje.nivel,
        "nivel_mazmorra":personaje.nivel_mazmorra,
        "arma": personaje.arma,
        "inventario": {
            "pociones": pociones_guardar
        }
    }

    if not os.path.exists("Dades"):
        os.makedirs("Dades")

    with open(RUTA_GUARDADO, "w", encoding = "utf-8") as archivo:
        json.dump(datos, archivo, indent = 4, ensure_ascii = False)

    print("Partida guardada exitosamente.")

#CARGAR
def cargar_partida():
    with open(RUTA_GUARDADO, "r", encoding = "utf-8") as archivo:
        datos = json.load(archivo)

    pj = Personaje(
        clase = datos["clase"],
        hp = datos["hp"],
        hp_max = datos["hp_max"],
        mana = datos["mana"],
        mana_max = datos["mana_max"],
        escudo = datos["escudo"],
        escudo_base = datos["escudo_base"],
        ataque = datos["ataque"],
        dinero = datos["dinero"],
    )

    #Restaura campos que el constructor
    pj.defensa_base = datos.get("defensa_base", datos["escudo_base"])
    pj.exp = datos["exp"]
    pj.exp_necesaria = datos["exp_necesaria"]
    pj.nivel = datos["nivel"]
    pj.nivel_mazmorra = datos["nivel_mazmorra"]
    pj.arma = datos["arma"]

    #Reconstruye objetos Pocion
    pj.inventario["pociones"] = []
    for p in datos["inventario"]["pociones"]:
        pocion = Pocion(
            nombre = p["nombre"],
            mana = p["mana"],
            cura = p["cura"],
            buff_ataque = p["buff_ataque"],
            icono_path = p.get("icono_path")
        )
        pocion.cantidad = p.get("cantidad", 1)
        pj.inventario["pociones"].append(pocion)

    print("Partida cargada exitosamente.")
    return pj

#UTILIDADES
def existe_partida_guardada():
    return os.path.exists(RUTA_GUARDADO)

def borrar_partida():
    if os.path.exists(RUTA_GUARDADO):
        os.remove(RUTA_GUARDADO)
        print("Partida eliminada.")
