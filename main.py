import pygame
import SelectorPersonaje
import Mazmorra
from Personaje import *
import Lobby
from Combate import *
import GuardarPartida

def iniciar_juego():
    pygame.init()
    pygame.display.set_caption("Survival Forest RPG")

    #VENTANA MAESTRA
    screen = pygame.display.set_mode((1200, 800))
    reloj = pygame.time.Clock()

    personaje = None

    #Si existe una partida guardada, entra directo al lobby
    if GuardarPartida.existe_partida_guardada():
        personaje = GuardarPartida.cargar_partida()
        estado = "LOBBY"
    else:
        estado = "SELECCION"

    while estado != "SALIR":
        if estado == "SELECCION":
            resultado = SelectorPersonaje.ejecutar(screen, reloj)
            if resultado == "CONTINUAR":
                personaje = GuardarPartida.cargar_partida()
                estado = "LOBBY"
            elif resultado is not None:
                personaje = resultado  #objeto Personaje nuevo
                estado = "LOBBY"
            else:
                estado = "SALIR"

        elif estado == "LOBBY":
            estado = Lobby.ejecutar(screen, reloj, personaje)

        elif estado == "MOCHILA":
            estado = Lobby.mochila(screen, reloj, personaje)

        elif estado == "TIENDA":
            estado = Lobby.ejecutar_tienda(screen, reloj, personaje)

        elif estado == "COMBATE":
            estado = seleccion_piso(screen, reloj, personaje)
            if estado == "COMBATE": 
                estado = ejecutar(screen, reloj, personaje)
            
        elif estado == "GAMEOVER":
            GuardarPartida.borrar_partida()   #borra el save al morir
            estado = "SELECCION"

    pygame.quit()

if __name__ == "__main__":
    iniciar_juego()