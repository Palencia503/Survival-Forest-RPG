
from LimpiarPantalla import limpiar_terminal
from  ui import VERDE, AMARILLO, CIAN, AZUL, ROJO, MAGENTA, BLANCO, RESET

armas_clase = {"tanque": "escudo", 
                "mago": "varita", 
                "asesino": "daga", 
                "tirador": "arco", 
                "guerrero": "espada" 
            }

class Personaje:
    #CONSTRUCTOR DEL PERSONAJE
    def __init__(self, clase, hp, mana, escudo, ataque):
        self.clase = clase
        self.hp = hp
        self.mana = mana
        self.escudo = escudo
        self.ataque = ataque

        self.defensa_base = escudo   #defensa natural del personaje
        self.escudo = self.defensa_base         

        self.dinero = 100 #para pruebas
        self.exp = 0
        self.exp_necesaria = 100
        self.nivel = 1
        self.arma = {
            "nom": "Puños",
            "dano": 1
        }
        
        self.inventario = {
            "armas": [],
            "pociones": [],
            "otros": []
        }   

    #funcion para equipar un arma
    def mostrar_armas(self):
        limpiar_terminal()
        print("- - ARMAS - -")
        armas = self.inventario["armas"]

        if not armas:
            print("No tienes armas.")
        else:
            for i, a in enumerate(armas, 1):
                print(f"{i}. {a}")

        input("\nENTER para continuar...")

    #muetra las pociones
    def mostrar_pociones(self):
        limpiar_terminal()
        print("- - POCIONES - -")
        pocion = self.inventario["pociones"]

        if not pocion:
            print("No tienes pociones.")
        else:
            for i, a in enumerate(pocion, 1):
                print(f"{i}. {a}")

        input("\nENTER para continuar...")

    #muestra otros objetos
    def mostrar_otros(self):
        limpiar_terminal()
        print("- - OTROS - -")
        otros = self.inventario["otros"]

        if not otros:
            print("No tienes mas objetos.")
        else:
            for i, a in enumerate(otros, 1):
                print(f"{i}. {a}")

        input("\nENTER para continuar...")
    #equipar arma
    def equipar_arma(self, nom, dano, defensa):
        dano_final = dano 
        arma_correcta = armas_clase[self.clase.lower()]

        # penalizacion si no es el arma correcta
        if arma_correcta not in nom.lower(): 
            dano_final = int(dano - (dano * 0.5))           
            print(f"{self.clase} no domina esta arma, hace menos dano.") 

        self.arma["nom"] = nom 
        self.arma["dano"] = dano_final 

        #si el arma es un escudo, SUMAR defensa a la defensa base
        if "escudo" in nom.lower():
            self.escudo = self.defensa_base + defensa
        else:
            #si no es escudo, vuelve a defensa base
            self.escudo = self.defensa_base

        print(f"{self.clase} se ha equipado {nom} con {dano_final} de dano.")
        if defensa > 0:
            print(f"Defensa total aumentada a {self.escudo}.")

    #desequipar arma
    def desequipar_arma(self):
        self.arma["nom"] = "Punos"
        self.arma["dano"] = 3
        self.escudo = self.defensa_base
        print(f"{self.clase} ha vuelto a usar punos.")

    #usar pocion
    def usar_pocion(self):
        limpiar_terminal()
        print("-- POCIONES --")

        pociones = self.inventario["pociones"]
        #si no tienes pociones
        if not pociones:
            print("No tienes pociones.")
            input("ENTER...")
            return

        for i, p in enumerate(pociones, 1):
            print(f"{i}. {p}")

        usar = input("ID pocion: ")
        #si no es numero
        if not usar.isdigit():
            print("Opcion no valida.")
            input("ENTER...")
            return

        idx = int(usar) - 1
        #control para que se utilicen numero correctos y no negativos.
        if idx < 0 or idx >= len(pociones):
            print("Opcion fuera de rango.")
            input("ENTER...")
            return

        pocion = pociones[idx]
        self.hp += pocion.cura
        self.ataque += pocion.dano
        del pociones[idx]

        print(f"Has usado {pocion.nom}.")
        input("ENTER...")


    #funcion para mostrar el estado del personaje
    def estado(self):
        print(f'CLASE: {self.clase}')
        print(f'HP: {VERDE}{self.hp}{RESET}')
        print(f'MANA: {CIAN}{self.mana}{RESET}')
        print(f'ESCUDO: {AZUL}{self.escudo}{RESET}')
        print(f'ATAQUE: {ROJO}{self.ataque}{RESET}')
        print(f'EXP: {MAGENTA}{self.exp}{RESET}')
        print(f'ORO: {AMARILLO}{self.dinero}{RESET}')
        print(f'NIVEL: {self.nivel}')
        print(f'{AMARILLO}ARMA:{RESET} {self.arma["nom"]} - dano: {self.arma["dano"]}')

    #Ganar experiencia
    def ganar_exp(self, cantidad):
        self.exp += cantidad
        print(f"Has ganado {cantidad} EXP.")

        while self.exp >= self.exp_necesaria:
            self.exp -= self.exp_necesaria
            self.nivel += 1

            #aumentar dificultad: cada nivel se necesita +20% EXP
            self.exp_necesaria = int(self.exp_necesaria * 1.2)

            #mejoras por clase
            if self.clase.lower() == "tanque":
                self.hp += 20
                self.defensa_base += 10
                self.escudo += 10
                self.ataque += 3

            elif self.clase.lower() == "mago":
                self.hp += 10
                self.mana += 20
                self.ataque += 5

            elif self.clase.lower() == "asesino":
                self.hp += 12
                self.ataque += 7

            elif self.clase.lower() == "tirador":
                self.hp += 10
                self.ataque += 6

            elif self.clase.lower() == "guerrero":
                self.hp += 15
                self.ataque += 5
                self.defensa_base += 5
                self.escudo += 5

            print(f"\n¡{self.clase} ha subido a NIVEL {self.nivel}!")
            print(f"EXP necesaria para el siguiente nivel: {self.exp_necesaria}")
            print(f"Stats mejorados: HP {self.hp}, ATAQUE {self.ataque}, ESCUDO {self.escudo}, MANA {self.mana}")


    #funcion para que el personaje muera
    def morir(self):
        if self.hp <= 0:
            print(f'{ROJO}El {self.clase} ha sido derrotado!{RESET}')
            return True
        else:
            return False

class Monstruo(Personaje):
    #constructor del monstruo
    def __init__(self, clase, hp, mana, escudo, ataque, nivel, recompensa):
        super().__init__(clase, hp, mana, escudo, ataque)
        self.nivel = nivel
        self.recompensa = recompensa

    #funcion para mostrar el estado del monstruo
    def estado(self):
        super().estado()
        print(f'RECOMPENSA:{self.recompensa}')
        print(f'NIVEL:{self.nivel}')

    #funcion para calcular el nivel de fuerza del monstruo
    def nivelFuerza(self, nivel_jugador):
        self.hp = 50 + (nivel_jugador * 20)
        self.ataque = 5 + (nivel_jugador * 3)

    #funcion para que el monstruo muera
    def morir(self):
        if self.hp <= 0:
            print(f'El {self.clase} ha sido derrotado!')
            print(f'Recompensa obtenida: {self.recompensa}')
            return True
        else:
            return False
