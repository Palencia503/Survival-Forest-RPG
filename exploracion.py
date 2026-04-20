import random
from combate import combate
from Personaje import Monstruo
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

    print("\n-Exploracion-")
    print("¿A donde quieres ir?")
    print("1. Bosque")
    print("2. Mazmorra")
    print("3. Montaña")
    print("4. Aldea (descansar)")
    print("0. Volver al menu")

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
        limpiar_terminal()
        input(f"\nBajando al piso {piso_actual} de la Mazmorra...")

        print("\nUn monstruo aparece!")
        monstruo_data = generar_monstruo_por_piso(piso_actual, monstruos_base)
        enemigo = crear_monstruo(monstruo_data)

        #si muere, vuelve al piso 1
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
            seguir = input("¿Quieres continuar bajando? (s/n): ").strip().lower()

            if seguir == "s":
                piso_actual += 1
                print(f"\nBajas al piso {piso_actual}.")
                input("ENTER para continuar...")
                limpiar_terminal()
                break

            elif seguir == "n":
                print("\nDecides volver al menu.")
                input("ENTER para continuar...")
                limpiar_terminal()
                return piso_actual
                
                

            else:
                print("Opcion no valida. Escribe S/N.")

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
