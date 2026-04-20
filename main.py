import random
import sys
from Personaje import Personaje, Monstruo
from combate import combate
from exploracion import explorar
from Mercado import Tienda
from LimpiarPantalla import limpiar_terminal

#diccionario de profesiones
def obtener_personajes_base():
    return {
        1: ("Tanque", 150, 0, 0, 15),
        2: ("Mago", 80, 20, 0, 15),
        3: ("Asesino", 80, 0, 0, 15),
        4: ("Tirador", 70, 0, 0, 15),
        5: ("Guerrero", 120, 0, 0, 15)

    }
    
#diccionario de monstruos. Ordenado por nivel
def obtener_monstruos_base():
    return {
        1:  ("Goblin", 60, 0, 5, 10, 1, {"oro": 10}),
        2:  ("Lobo", 70, 0, 6, 14, 2, {"tipo": "otros", "nom": "Colmillo afilado"}),
        3:  ("Esqueleto", 80, 0, 8, 12, 3, {"tipo": "armas", "nom": "Hueso afilado", "dano": 3}),
        4:  ("Bandido", 90, 0, 10, 15, 4, {"oro": 20}),
        5:  ("Orco", 110, 5, 12, 18, 5, {"tipo": "armas", "nom": "Espada oxidada", "dano": 5}),

        6:  ("Trol pequeno", 130, 5, 14, 20, 6, {"oro": 25}),
        7:  ("Murcielago gigante", 120, 0, 10, 22, 7, {"tipo": "otros", "nom": "Ala oscura"}),
        8:  ("Zombi", 140, 0, 12, 20, 8, {"tipo": "pociones", "nom": "Pocion debil", "curacion": 20}),
        9:  ("Guerrero esqueleto", 150, 0, 15, 25, 9, {"tipo": "armas", "nom": "Espada rota", "dano": 4}),
        10: ("Ogro", 180, 5, 18, 28, 10, {"oro": 40}),

        11: ("Lobo alfa", 200, 0, 20, 30, 11, {"tipo": "otros", "nom": "Garra afilada"}),
        12: ("Chaman orco", 180, 20, 15, 32, 12, {"tipo": "pociones", "nom": "Pocion magica", "curacion": 40}),
        13: ("Golem de piedra", 250, 0, 25, 35, 13, {"oro": 50}),
        14: ("Arana gigante", 220, 0, 18, 33, 14, {"tipo": "otros", "nom": "Veneno viscoso"}),
        15: ("Caballero oscuro", 260, 10, 30, 40, 15, {"tipo": "armas", "nom": "Espada negra", "dano": 10}),

        16: ("Trol de guerra", 300, 10, 28, 42, 16, {"oro": 60}),
        17: ("Espectro", 240, 30, 10, 38, 17, {"tipo": "otros", "nom": "Esencia oscura"}),
        18: ("Minotauro", 320, 0, 22, 45, 18, {"tipo": "armas", "nom": "Hacha rota", "dano": 8}),
        19: ("Harpia", 260, 0, 15, 40, 19, {"tipo": "otros", "nom": "Pluma afilada"}),
        20: ("Golem de hierro", 350, 0, 35, 50, 20, {"oro": 80}),

        21: ("Demonio menor", 300, 20, 25, 48, 21, {"tipo": "pociones", "nom": "Pocion infernal", "curacion": 60}),
        22: ("Serpiente colosal", 330, 0, 18, 52, 22, {"tipo": "otros", "nom": "Escama venenosa"}),
        23: ("Nigromante", 280, 40, 12, 45, 23, {"oro": 100}),
        24: ("Caballero maldito", 360, 10, 30, 55, 24, {"tipo": "armas", "nom": "Espada maldita", "dano": 15}),
        25: ("Trol anciano", 400, 15, 32, 60, 25, {"oro": 120}),

        26: ("Dragon joven", 450, 20, 40, 65, 26, {"tipo": "otros", "nom": "Escama roja"}),
        27: ("Demonio mayor", 420, 30, 35, 70, 27, {"oro": 150}),
        28: ("Titan de roca", 500, 0, 45, 75, 28, {"tipo": "otros", "nom": "Nucleo de piedra"}),
        29: ("Dragon adulto", 600, 40, 50, 80, 29, {"tipo": "armas", "nom": "Colmillo de dragon", "dano": 20}),
        30: ("Senor demonio", 700, 50, 60, 90, 30, {"oro": 200})
    }

#armas iniciales de los personajes
def armas():
    return {
        "Tanque": {
            "nom": "Escudo Simple",
            "dano": 5,
            "defensa": 10,
        },
        "Mago": {
            "nom": "Varita Simple",
            "dano": 15
        },
        "Asesino": {
            "nom": "Daga Simple",   
            "dano": 20
        },
        "Tirador": {
            "nom": "Arco Simple",
            "dano": 25
        },
        "Guerrero": {
            "nom": "Espada Simple",
            "dano": 30
        }
    }

#crear al jugador
def crear_jugador(personajes_base, puntos_de_habilidad):
    while True:
        print("\nCREAR PERSONAJE")
        print("--- ELIGE PROFESION ---")
        for i, pj in personajes_base.items(): #muestra las profesiones
            print(f"{i}. {pj[0]}") 
        
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
                    print(f"\nPuntos restantes: {puntos_de_habilidad}")#muestra los puntos restantes
                    print(f"Atributos actuales: HP: {jugador.hp}, Escudo: {jugador.escudo}, Ataque: {jugador.ataque}")#muestra los atributos actuales
                    print("1. Mejorar HP (+10)")
                    print("2. Mejorar Escudo (+5)")
                    print("3. Mejorar Ataque (+2)")
                    
                    eleccion = input("Selecciona que mejorar: ")#elige la mejora
                    limpiar_terminal()  #limpia terminal
                    if eleccion == "1":
                        jugador.hp += 10  #mejora el hp
                        puntos_de_habilidad -= 1#resta un punto de habilidad

                    elif eleccion == "2":
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
    #si elige desequipar equipo los puños
    eleccion = int(eleccion)
    if eleccion == 0: 
        jugador.equipar_arma("Punos", 1) 
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
    print('    -------------------------------------')
    print('             Survival-Forest-RPG')
    print('    -------------------------------------\n')
    inicio_historia = """
    Despiertas en un camino polvoriento sin recordar nada.
    A lo lejos ves un pequeño pueblo rodeado de murallas.
    Un guardia te mira sorprendido.
    —¿Otro recien llegado? Entra… aqui estaras a salvo.
    Asi comienza tu nueva vida. 
    """
    print(inicio_historia)
    #falta introducir la historia en diferentes partes
    #del juego.

    personajes_base = obtener_personajes_base() #obtiene los personajes base
    monstruos_base = obtener_monstruos_base() #obtiene los monstruos base
    puntos_de_habilidad = 5 #puntos de habilidad
    jugador = crear_jugador(personajes_base, puntos_de_habilidad)#crea al jugador
    
    tienda = Tienda() #la tienda
    piso_actual = 1
    jugar = True

    #bucle principal
    while jugar:  
        #si el personaje muere se acaba el juego.
        if jugador.hp < 0:
            break

        print("\n--- MENU PRINCIPAL ---")
        print("1. Explorar")
        print("2. Ver estado")
        print("3. Mochila")
        print("4. Tienda")
        print("0. Salir")
        
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
            limpiar_terminal()#limpia terminal
            tienda.mostrar_inventario()

            objeto_comprar = input("ID del objeto a comprar: ")
            if objeto_comprar.isdigit():
                tienda.comprar(int(objeto_comprar), jugador)
            else:
                print("¡¡ Introduce el ID. Ejemplo: 1. !!")

            input("\nPresiona ENTER para continuar...")
            limpiar_terminal()#limpia terminal

        #salir
        elif opcion == "0": 
            limpiar_terminal()#limpia terminal2
            print("Gracias por jugar. ¡Hasta la proxima!")
            sys.exit()
        else:
            print("¡Opcion no valida!")

if __name__ == "__main__":
    main()