import pygame
import json
import random

#Imagenes de los enemigos
#Los enemigos sin imagen usan un Surface de color como placeholder
def _surface_color(color):
    s = pygame.Surface((200, 200))
    s.fill(color)
    return s

enemigos = {
    "Slime Verde": pygame.image.load("Characters/Enemigos/slime.png"),
    "Esqueleto": _surface_color((236, 240, 241)),   #Blanco hueso
    "Goblin": _surface_color((211, 84, 0)),        #Marron goblin
    "Orco": _surface_color((39, 174, 96)),      #Verde orco
    "Mago Oscuro": _surface_color((142, 68, 173)),     #Purpura magico
}


with open("Info/Monstruos.json", "r") as archivo:
    enemigos_data = json.load(archivo)

def generar_enemigo(nivel):
    enemigos_disponibles = [e for e in enemigos_data.values() if e["nivel"] <= nivel]
    if not enemigos_disponibles:
        enemigos_disponibles = [enemigos_data["1"]]
    enemigo_base = random.choice(enemigos_disponibles)
    nuevo_enemigo = {k: v for k, v in enemigo_base.items()}
    nuevo_enemigo["exp"] = int(nuevo_enemigo["exp"] * (1 + 0.2 * (nivel - enemigo_base["nivel"])))
    nuevo_enemigo["recompensa"] = int(nuevo_enemigo["recompensa"] * (1 + 0.2 * (nivel - enemigo_base["nivel"])))
    nuevo_enemigo["hp_max"] = nuevo_enemigo["hp"]  #Vida maxima para la barra
    nuevo_enemigo["salud"] = nuevo_enemigo["hp"]   #Vida actual del enemigo en combate
    nuevo_enemigo["nivel"] = nivel
    return nuevo_enemigo

