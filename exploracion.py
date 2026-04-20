import random
from combate import combate
from Personaje import Monstruo
from ui import VERDE, AMARILLO, CIAN, AZUL, ROJO, MAGENTA, BLANCO, GRIS, MARRON, RESET
from LimpiarPantalla import limpiar_terminal

#generar monstruo segun el piso
def generar_monstruo_por_piso(piso, monstruos_base):
    piso = int(piso) 
    nivel = min(piso, 30)
    return monstruos_base[nivel]

#generar monstruos desde datos
def crear_monstruo(monstruo_data):
    nom, hp, mana, escudo, ataque, nivel, recompensa = monstruo_data
    return Monstruo(nom, hp, mana, escudo, ataque, nivel, recompensa)

#manejar combate y muerte
def enfrentar_monstruo(jugador, monstruo):
    resultado = combate(jugador, monstruo)

    if resultado == "huida":
        return "huida"
    #si mueres pierdes el inventario
    if resultado == "derrota":
        print("\nHas muerto... pierdes todo tu inventario.")
        print("¡La vida solo es una! ;)")
        jugador.inventario = {
            "armas": [],
            "pociones": [],
            "otros": []
        }
        jugador.desequipar_arma()
        input("ENTER para continuar...")
        return "derrota"

    return "victoria"

#exploracion
def explorar(jugador, monstruos_base, piso_actual):
    print(f"\n{AZUL}-Exploracion-{RESET}")
    print("¿A donde quieres ir?")
    print(f"1.{VERDE}Bosque{RESET}")
    print(f"2.{MARRON}Mazmorra{RESET}")
    print(f"3.{GRIS}Montaña{RESET}")
    print(f"4.{CIAN}Aldea (descansar){RESET}")
    print(f"0.olver al menu principal")

    opcion = input("Elige una zona: ")
    evento = random.randint(1, 100)

    #bosque
    if opcion == "1":
        limpiar_terminal()
        input("\nCaminando hacia el Bosque...")

        if evento > 50:
            print("\nTe encuentras con un monstruo!")
            monstruo_data = random.choice(list(monstruos_base.values()))
            enemigo = crear_monstruo(monstruo_data)

            if enfrentar_monstruo(jugador, enemigo):
                return piso_actual  #vuelve al menu
        else:
            print("No has encontrado nada.")

   #mazmorras(usa pisos)
    elif opcion == "2":
        while True:
            limpiar_terminal()
            input(f"\nExplorando el piso {piso_actual} de la Mazmorra...")

            #historia de la mazmorra
            if piso_actual == 5:
                print("\n--- NOTA ENCONTRADA ---")
                print("'No podemos salir de la sala. La puerta se ha cerrado...'")
                print("-----------------------\n")
                input("ENTER...")
            elif piso_actual == 10:
                print("\n--- RESTOS ENCONTRADOS ---")
                print("Ves huesos de aventureros anteriores. Comprendes algo oscuro:")
                print("El pueblo no salva a la gente, la atrapa para alimentar a la mazmorra.")
                print("--------------------------\n")
                input("ENTER...")
            elif piso_actual == 20:
                print("\n--- LA VOZ EN LA CABEZA ---")
                print("'Has llegado mas lejos que nadie... pero este poder tiene un precio.'")
                print("---------------------------\n")
                input("ENTER...")
            elif piso_actual == 30:
                print("\n--- REVELACION CONGELANTE ---")
                print("Una figura oscura susurra...")
                print("'Tu creaste este bucle para tener un desafio infinito, pero olvidaste tu propia trampa.'")
                print("-----------------------------\n")
                input("ENTER...")

            # Probabilidad de cofre (20%)
            evento_mazmorra = random.randint(1, 100)
            if evento_mazmorra <= 20 and piso_actual not in (5, 10, 20, 30):
                print("\n¡Encuentras un cofre abandonado!")
                oro_encontrado = random.randint(10, 50) + (piso_actual * 2)
                jugador.dinero += oro_encontrado
                print(f"Obtienes {oro_encontrado} monedas de oro.")
                input("ENTER para continuar...")
                resultado = "victoria" 

            else:
                print("\n¡Un monstruo aparece!")
                monstruo_data = generar_monstruo_por_piso(piso_actual, monstruos_base)
                enemigo = crear_monstruo(monstruo_data)
                
                #Jefe de piso cada 5 pisos
                if piso_actual % 5 == 0:
                    print("¡¡ES UN JEFE DE PISO!!")
                    enemigo.hp = int(enemigo.hp * 1.5)
                    enemigo.ataque = int(enemigo.ataque * 1.2)

                resultado = enfrentar_monstruo(jugador, enemigo)

            if resultado == "derrota":
                piso_actual = 1
                return piso_actual

            if resultado == "huida":
                print("\nHas escapado de la mazmorra.")
                input("ENTER para continuar...")
                limpiar_terminal()
                return piso_actual

            #preguntar si quiere continuar
            while True:
                seguir = input("¿Quieres continuar bajando de piso? (s/n): ").strip().lower()
                #si quiere continuar sube de piso
                if seguir == "s":
                    piso_actual += 1
                    cura = random.randint(5, 15)
                    jugador.hp += cura
                    print(f"\nDescansas en las escaleras. Recuperas {cura} HP.")
                    print(f"Bajas al piso {piso_actual}.")
                    input("ENTER para continuar...")
                    limpiar_terminal()
                    break

                elif seguir == "n":
                    print("\nDecides volver al menu principal para reabastecerte.")
                    input("ENTER para continuar...")
                    limpiar_terminal()
                    return piso_actual
                    
                else:
                    print("Opcion no valida. Escribe (S/N).")

    #montaña
    elif opcion == "3":
        limpiar_terminal()
        input("\nCaminando hacia la Montaña...")

        if evento < 25 or evento > 75:
            print("\nTe encuentras con un monstruo!")
            monstruo_data = random.choice(list(monstruos_base.values()))
            enemigo = crear_monstruo(monstruo_data)

            if enfrentar_monstruo(jugador, enemigo):
                return piso_actual
        else:
            print("No has encontrado nada.")

    #aldea
    elif opcion == "4":
        limpiar_terminal()
        input("\nCaminando hacia la Aldea...")
        jugador.hp += 50
        print("Descansas y recuperas +50 HP.")

    return piso_actual
