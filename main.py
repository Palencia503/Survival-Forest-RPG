import random
import sys
from Personaje import Personaje, Monstruo
from combate import combate
from exploracion import explorar
from Mercado import Tienda
from LimpiarPantalla import limpiar_terminal
from ui import MARRON, VERDE, AMARILLO, CIAN, AZUL, ROJO, MAGENTA, BLANCO, RESET
from guardar_datos import guardar_partida, cargar_partida

#diccionario de profesiones
def obtener_personajes_base():
    ruta = os.path.join("Info", "Personajes.json")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        
        personajes = {}
        for id_pj, info in datos.items():
            # (clase, hp, mana, escudo, ataque)
            personajes[int(id_pj)] = (
                info["clase"],
                info["hp"],
                info["mana"],
                info["escudo"],
                info["ataque"]
            )
        return personajes
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar profesiones: {e}")
        return {}
    
import json
import os

#diccionario de monstruos. Ordenado por nivel
def obtener_monstruos_base():
    ruta = os.path.join("Info", "Monstruos.json")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
        
        monstruos = {}
        for id_monster, info in datos.items():
            # Convertir a tupla para mantener compatibilidad con exploracion.py
            # (nom, hp, mana, escudo, ataque, nivel, recompensa)
            monstruos[int(id_monster)] = (
                info["nombre"],
                info["hp"],
                info["mana"],
                info["defensa"], #En exploracion.py se desempaqueta como 'escudo'
                info["ataque"],
                info["nivel"],
                info["recompensa"]
            )
        return monstruos
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar monstruos: {e}")
        return {}

#armas iniciales de los personajes
def armas():
    ruta = os.path.join("Info", "ArmasIniciales.json")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error al cargar armas iniciales: {e}")
        return {}

#crear al jugador
def crear_jugador(personajes_base, puntos_de_habilidad):
    while True:
        print("\nCREAR PERSONAJE")
        print("--- ELIGE PROFESION ---")
        for i, pj in personajes_base.items(): #muestra las profesiones
            print(f"{i}. {VERDE}{pj[0]}{RESET}") 
        
        try:
            opcion = int(input("Selecciona un numero: "))#elige la profesion
            if opcion in personajes_base:
                clase, hp, mana, escudo, ataque = personajes_base[opcion]
                jugador = Personaje(clase, hp, mana, escudo, ataque)#crea al jugador con sus atributos
                
                # Equipar arma inicial
                armas_base = armas()
                if clase in armas_base:
                    info = armas_base[clase]

                    nom = info["nom"]

                    #si tiene daño
                    if "dano" in info:
                        dano = info["dano"]
                    else:
                        dano = 0

                    #si tiene defensa
                    if "defensa" in info:
                        defensa = info["defensa"]
                    else:
                        defensa = 0

                    jugador.equipar_arma(nom, dano, defensa)

                input("Clic para continuar...")
                limpiar_terminal()#limpia terminal
                print(f"\nTienes {puntos_de_habilidad} puntos de habilidad para añadir a tus atributos.")#muestra los puntos de habilidad
                
                while puntos_de_habilidad > 0:#si hay puntos de habilidad continua
                    print(f"\nPuntos restantes:{VERDE} {puntos_de_habilidad}{RESET}")#muestra los puntos restantes
                    print(f"Atributos actuales: HP:{VERDE}{jugador.hp}{RESET}, Escudo: {AZUL}{jugador.escudo}{RESET}, Ataque: {ROJO}{jugador.ataque}{RESET}")#muestra los atributos actuales
                    print(f"{AMARILLO}1. Mejorar HP (+10){RESET}")
                    print(f"{AMARILLO}2. Mejorar Escudo (+5){RESET}")
                    print(f"{AMARILLO}3. Mejorar Ataque (+2){RESET}")
                    
                    eleccion = input("Selecciona que mejorar: ")#elige la mejora
                    limpiar_terminal()  #limpia terminal
                    if eleccion == "1":
                        jugador.hp += 10  #mejora el hp
                        puntos_de_habilidad -= 1#resta un punto de habilidad

                    elif eleccion == "2":
                        jugador.defensa_base += 5
                        jugador.escudo += 5  #mejora el escudo
                        puntos_de_habilidad -= 1#resta un punto de habilidad

                    elif eleccion == "3":
                        jugador.ataque += 2  #mejora el ataque
                        puntos_de_habilidad -= 1  #resta un punto de habilidad

                    else:
                        print("Opcion no valida.")

                jugador.estado()
                input("\nPresiona ENTER para comenzar la aventura...")
                limpiar_terminal()#limpia terminal
                return jugador
            print("¡Opcion no valida!")

        except ValueError:
            print("Error: Debes ingresar un numero.")

#mochila
def menu_mochila(jugador):
    while True:   
        limpiar_terminal()
        print("--- MOCHILA ---")
        print("1. Ver pociones")
        print("2. Ver armas")
        print("3. Ver otros")
        print("4. Usar pocion")
        print("5. Equipar arma")
        print("0. Volver")

        opcion = input("\nElige una opcion: ")
        limpiar_terminal()
        if opcion == "1": #muestra pociones
            jugador.mostrar_pociones()

        elif opcion == "2":#muestra armas
            jugador.mostrar_armas()

        elif opcion == "3": #muestra otros
            jugador.mostrar_otros()

        elif opcion == "4": #usar pociones
            jugador.usar_pocion()

        elif opcion == "5": #equipar armas
            menu_equipar_arma(jugador)

        elif opcion == "0":
            break

        else:
            print("Opcion no valida.")
            input("ENTER para continuar...")
            limpiar_terminal()#limpia terminal


#equipar arma
def menu_equipar_arma(jugador):
    armas = jugador.inventario["armas"]
    #si no tienes armas
    if not armas:
        print("No tienes armas.")
        input("ENTER...")
        return

    print("- - EQUIPAR ARMA - -")
    for i, arma in enumerate(armas, 1):
        print(f"{i}. {arma}")

    print("0. Desequipar arma")

    eleccion = input("ID arma: ")
    #si no es numero el introducido
    if not eleccion.isdigit():
        print("Opcion no valida.")
        input("ENTER...")
        return
    #si elige desequipar
    eleccion = int(eleccion)
    if eleccion == 0: 
        jugador.desequipar_arma() 
        input("ENTER...") 
        return
    #control de numeros negativos o que no existan
    idx = eleccion - 1
    if idx < 0 or idx >= len(armas):
        print("Opcion fuera de rango.")
        input("ENTER...")
        return

    arma = armas[idx]
    jugador.equipar_arma(arma.nom, arma.dano, arma.defensa)
    input("ENTER...")


def main():
    limpiar_terminal()#limpia terminal
    print(F'{AZUL}    -------------------------------------{RESET}')
    print(f'{AMARILLO}             Survival-Forest-RPG{RESET}')
    print(f'{AZUL}    -------------------------------------{RESET}\n')
    inicio_historia = f"""{VERDE}
    Despiertas en un camino polvoriento sin recordar nada.

    A lo lejos ves un pequeño pueblo rodeado de murallas.

    Un guardia te mira sorprendido.

    —¿Otro recien llegado? Entra… aqui estaras a salvo.

    Asi comienza tu nueva vida.{RESET} 
    """
    print(inicio_historia)
    #falta introducir la historia en diferentes partes
    #del juego.

    personajes_base = obtener_personajes_base() #obtiene los personajes base
    monstruos_base = obtener_monstruos_base() #obtiene los monstruos base
    
    # Intentar cargar partida
    jugador = None
    piso_actual = 1
    
    if os.path.exists(os.path.join("Dades/")):
        cargar = input("¿Deseas cargar la partida guardada? (s/n): ").strip().lower()
        if cargar == "s":
            jugador, piso_actual = cargar_partida()
            if jugador:
                print(f"\nPartida cargada. Bienvenido de nuevo, {VERDE}{jugador.clase}{RESET}!")
                input("ENTER para continuar...")
                limpiar_terminal()
            else:
                print("\nNo se pudo cargar la partida.")
    
    if not jugador:
        puntos_de_habilidad = 5 #puntos de habilidad
        jugador = crear_jugador(personajes_base, puntos_de_habilidad)#crea al jugador
    
    tienda = Tienda() #la tienda
    jugar = True

    #bucle principal
    while jugar:  
        #si el personaje muere se acaba el juego.
        if jugador.hp <= 0:
            break

        print(f"\n{AZUL}--- MENU PRINCIPAL ---{RESET}")
        print(f"{CIAN}1. Explorar{RESET}")
        print(f"{BLANCO}2. Ver estado{RESET}")
        print(f"{MARRON}3. Mochila{RESET}")
        print(f"{AMARILLO}4. Tienda{RESET}")
        print(f"{VERDE}5. Guardar Partida{RESET}")
        print(f"0. Salir")
        
        opcion = input("Elige una opcion: ")
        #explorar
        if opcion == "1": 
            limpiar_terminal()#limpia terminal
            print("- - EXPLORAR - -")
            piso_actual = explorar(jugador, monstruos_base, piso_actual)
            input("\nPresiona ENTER para continuar...")

        #estado del personaje
        elif opcion == "2": 
            limpiar_terminal()#limpia terminal
            print("- - ESTADO - -")
            jugador.estado()
            input("\nPresiona ENTER para continuar...")
            limpiar_terminal()

        #mochila
        elif opcion == "3":
            limpiar_terminal() 
            print("\n- - MOCHILA - -") 
            menu_mochila(jugador)

        #tienda
        elif opcion == "4": 
            while True:
                limpiar_terminal()
                print(f"\n{AZUL}- - TIENDA - -{RESET}")
                print(f"{VERDE}1. Comprar objetos{RESET}")
                print(f"{VERDE}2. Vender restos de monstruos{RESET}")
                print(f"0. Salir de la tienda")

                opcion_tienda = input("Elige una opcion: ")
                
                if opcion_tienda == "1":
                    limpiar_terminal()
                    tienda.mostrar_inventario()

                    objeto_comprar = input("ID del objeto a comprar: ")
                    if objeto_comprar.isdigit():
                        tienda.comprar(int(objeto_comprar), jugador)
                    else:
                        print("¡¡ Introduce el ID. Ejemplo: 1. !!")

                    input("\nPresiona ENTER para continuar...")
                
                elif opcion_tienda == "2":
                    tienda.vender(jugador)
                
                elif opcion_tienda == "0":
                    limpiar_terminal()
                    break
                else:
                    print("Opcion no valida.")
                    input("\nPresiona ENTER para continuar...")
        
        #guardar partida
        elif opcion == "5":
            guardar_partida(jugador, piso_actual)
            input("\nPresiona ENTER para continuar...")

        #salir
        elif opcion == "0": 
            limpiar_terminal()#limpia terminal2
            print("Gracias por jugar. ¡Hasta la proxima!")
            sys.exit()
        else:
            print("¡Opcion no valida!")

if __name__ == "__main__":
    main()