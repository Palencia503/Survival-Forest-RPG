import json
import os
import random as ra
import glob
from ui import ROJO, VERDE, AMARILLO, CIAN, AZUL, MAGENTA, BLANCO, RESET
from Personaje import Personaje, Monstruo
from Objetos import Pocion, Arma

def guardar_partida(jugador, piso_actual):
    numero_partida = 600
    
    carpeta_dades = "Dades"

    if not os.path.exists(carpeta_dades):
        os.makedirs(carpeta_dades)
        
    ruta = os.path.join("Dades", f"{numero_partida}.json")
    
    #convertir inventario a datos serializables
    inventario_serializado = {
        "armas": [],
        "pociones": [],
        "otros": []
    }
    
    for arma in jugador.inventario["armas"]:
        inventario_serializado["armas"].append({
            "tipo": arma.tipo,
            "nom": arma.nom,
            "precio": arma.precio,
            "dano": arma.dano,
            "defensa": arma.defensa,
            "cantidad": getattr(arma, "cantidad", 1)
        })
        
    for pocion in jugador.inventario["pociones"]:
        inventario_serializado["pociones"].append({
            "tipo": pocion.tipo,
            "nom": pocion.nom,
            "precio": pocion.precio,
            "cura": pocion.cura,
            "dano": pocion.dano,
            "cantidad": getattr(pocion, "cantidad", 1)
        })
        
    for otros in jugador.inventario["otros"]:
        inventario_serializado["otros"].append({
            "tipo": otros.tipo,
            "nom": otros.nom,
            "precio": otros.precio
        })

    datos = {
        "piso_actual": piso_actual,
        "jugador": {
            "clase": jugador.clase,
            "hp": jugador.hp,
            "mana": jugador.mana,
            "escudo": jugador.escudo,
            "ataque": jugador.ataque,
            "defensa_base": jugador.defensa_base,
            "dinero": jugador.dinero,
            "exp": jugador.exp,
            "exp_necesaria": jugador.exp_necesaria,
            "nivel": jugador.nivel,
            "arma": jugador.arma,
            "inventario": inventario_serializado
        }
    }
    
    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent = 4, ensure_ascii = False)
        print(f"\n{VERDE}¡Partida guardada correctamente!{RESET}")
    except Exception as e:
        print(f"\nError al guardar la partida: {e}")

def cargar_partida():
    carpetaPartidas = './Dades'

    print("Partidas Guardadas:")
    archivos_json = glob.glob(os.path.join(carpetaPartidas, '*.json'))
    for archivo in archivos_json:
        print(os.path.basename(archivo))

    numero_partida = input("Ingrese el número de partida a cargar: ")
    ruta = os.path.join("Dades", f"{numero_partida}.json")
    if not os.path.exists(ruta):
        return None, 1
        
    try:
        with open(ruta, "r", encoding = "utf-8") as f:
            datos = json.load(f)
            
        p_info = datos["jugador"]
        jugador = Personaje(
            p_info["clase"], 
            p_info["hp"], 
            p_info["mana"], 
            p_info["escudo"], 
            p_info["ataque"]
        )
        jugador.defensa_base = p_info["defensa_base"]
        jugador.dinero = p_info["dinero"]
        jugador.exp = p_info["exp"]
        jugador.exp_necesaria = p_info["exp_necesaria"]
        jugador.nivel = p_info["nivel"]
        jugador.arma = p_info["arma"]
        
        # Cargar inventario
        inv = p_info["inventario"]
        for a in inv["armas"]:
            jugador.inventario["armas"].append(Arma(a["tipo"], a["cantidad"], a["nom"], a["precio"], a["dano"], a["defensa"]))
        for p in inv["pociones"]:
            jugador.inventario["pociones"].append(Pocion(p["tipo"], p["cantidad"], p["nom"], p["precio"], p["cura"], p["dano"]))
        for o in inv["otros"]:
            from Objetos import Objeto
            jugador.inventario["otros"].append(Objeto(o["tipo"], o["nom"], o["precio"]))
            
        return jugador, datos["piso_actual"]
    except Exception as e:
        print(f"Error al cargar la partida: {e}")
        return None, 1
