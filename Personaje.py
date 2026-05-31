import pygame
import json
import random

#Mapeo de armas permitidas por clase para evitar penalizacion de dano (con sinonimos para Pygame)
armas_clase = {
    "tanque": ["escudo"], 
    "mago": ["varita", "baston"], 
    "asesino": ["daga"], 
    "tirador": ["arco", "ballesta"], 
    "guerrero": ["espada"] 
}

class Pocion:
    def __init__(self, nombre, mana, cura, buff_ataque, icono_path = None):
        self.nombre = nombre
        self.mana = mana
        self.cura = cura
        self.buff_ataque = buff_ataque
        self.icono_path = icono_path 


    def __str__(self):
        texto = self.nombre
        if self.cura > 0:
            texto += f" | Cura: +{self.cura} HP"
        if self.mana > 0:
            texto += f" | Mana: +{self.mana}"
        if self.buff_ataque > 0:
            texto += f" | Ataque: +{self.buff_ataque}"
        return texto

class Personaje:
    #CONSTRUCTOR DEL PERSONAJE
    def __init__(self, clase, hp, hp_max, mana, mana_max, escudo, escudo_base, ataque, dinero = 1000):
        self.clase = clase
        self.hp_max = hp_max  #Guardamos la vida maxima para barras de vida
        self.hp = hp
        self.mana = mana
        self.mana_max = mana_max
        self.escudo = escudo
        self.escudo_base = escudo_base
        self.ataque = ataque

        self.defensa_base = escudo_base   #defensa natural del personaje
        self.escudo = self.defensa_base  
        #cooldown
        self.cooldown = 0
        self.cooldown_max = 500        

        self.dinero = dinero #oro del jugador
        self.exp = 0
        self.exp_necesaria = 100
        self.nivel = 0
        self.nivel_mazmorra = 1

        self.arma = {
            "nom": "Puños",
            "dano": 1
        }    
        self.inventario = {
            "pociones": []

        }
        self.cantidad = 0

    #Agregar pocion al inventario
    def agregar_pocion_a_inventario(self, pocion):
        stock = self.inventario["pociones"]
        for i in stock:
            if i.nombre == pocion.nombre:
                i.cantidad += 1
                print(f"Se ha agregado {pocion.nombre} al inventario.")
                return
        stock.append(pocion)
        pocion.cantidad = 1
        print(f"Se ha agregado {pocion.nombre} al inventario.")
        
    #Usar pocion
    def usar_pocion(self, pocion):
        if pocion.cantidad > 0:
            pocion.cantidad -= 1
            self.hp = min(self.hp_max, self.hp + pocion.cura)
            self.mana = min(self.mana_max, self.mana + pocion.mana)
            self.ataque = self.ataque + pocion.buff_ataque
            print(f"Se ha usado {pocion.nombre} y ha recuperado {pocion.cura} HP y {pocion.mana} de mana.")
        else:
            print(f"No quedan {pocion.nombre} en el inventario.")

    #Funcion de ataque del personaje
    def atacar(self):
        import random
        dano_base = self.ataque + self.arma["dano"]
        variacion = random.randint(-2, 4)
        return max(1, dano_base + variacion)

    #Equipar arma
    def equipar_arma(self, nom, dano, defensa):
        dano_final = dano 
        clase_lower = self.clase.lower()
        sinonimos = armas_clase.get(clase_lower, [clase_lower])

        #Penalizacion si no es el arma correcta
        es_correcta = any(s in nom.lower() for s in sinonimos)
        mensaje_penalizacion = ""
        if not es_correcta: 
            dano_final = int(dano - (dano * 0.5))           
            mensaje_penalizacion = f"¡{self.clase} no domina esta arma, hace menos daño!"
            print(mensaje_penalizacion) 

        self.arma["nom"] = nom 
        self.arma["dano"] = dano_final 

        #Si el arma es un escudo, SUMAR defensa a la defensa base
        if "escudo" in nom.lower():
            self.escudo = self.defensa_base + defensa
        else:
            #Si no es escudo, vuelve a defensa base
            self.escudo = self.defensa_base

        msg = f"{self.clase} se ha equipado {nom} con {dano_final} de daño."
        print(msg)
        if defensa > 0:
            print(f"Defensa total aumentada a {self.escudo}.")
            
        return mensaje_penalizacion, msg

    #Desequipar arma
    def desequipar_arma(self):
        self.arma["nom"] = "Puños"
        self.arma["dano"] = 3
        self.escudo = self.defensa_base
        print(f"{self.clase} ha vuelto a usar puños.")

    #Ganar experiencia
    def ganar_exp(self, cantidad):
        self.exp += cantidad
        subio_nivel = False

        #Mientras tengas suficiente EXP para subir de nivel
        while self.exp >= self.exp_necesaria:
            # Subir nivel
            self.nivel += 1
            subio_nivel = True
            self.exp -= self.exp_necesaria

            #Aumenta EXP necesaria (+20%)
            self.exp_necesaria = int(self.exp_necesaria * 1.2)

            #Mejoras según la clase
            if self.clase == "Tanque":
                self.hp_max += 20
                self.hp += 20
                self.defensa_base += 10
                self.escudo += 10
                self.ataque += 3

            elif self.clase == "Mago":
                self.hp_max += 10
                self.hp += 10
                self.mana += 20
                self.mana_max += 20
                self.ataque += 5

            elif self.clase == "Asesino":
                self.hp_max += 12
                self.hp += 12
                self.ataque += 7

            elif self.clase == "Tirador":
                self.hp_max += 10
                self.hp += 10
                self.ataque += 6

            elif self.clase == "Guerrero":
                self.hp_max += 15
                self.hp += 15
                self.ataque += 5
                self.defensa_base += 5
                self.escudo += 5

            #Mensajes de subida de nivel
            msg = f"¡{self.clase} ha subido a NIVEL {self.nivel}!"
            print(msg)
            print(f"EXP necesaria para el siguiente nivel: {self.exp_necesaria}")
            print(f"Stats mejorados: HP {self.hp}, ATAQUE {self.ataque}, ESCUDO {self.escudo}, MANA {self.mana}")

        return subio_nivel

    #Funcion para que el personaje muera
    def morir(self):
        if self.hp <= 0:
            print(f'El {self.clase} ha sido derrotado!')
            return True
        else:
            return False

class Monstruo(Personaje):
    #Constructor del monstruo
    def __init__(self, clase, hp, hp_max, mana, mana_max, escudo, escudo_base, ataque, nivel, recompensa):
        super().__init__(clase, hp, hp_max, mana, mana_max, escudo, escudo_base, ataque)
        self.nivel = nivel
        self.recompensa = recompensa

    #Funcion para mostrar el estado del monstruo
    def estado(self):
        super().estado()
        print(f'RECOMPENSA: {self.recompensa}')
        print(f'NIVEL: {self.nivel}')

    #Funcion para calcular el nivel de fuerza del monstruo
    def nivelFuerza(self, nivel_jugador):
        #Mantenemos las formulas exactas del usuario
        self.hp_max = 50 + (nivel_jugador * 20)
        self.hp = self.hp_max
        self.ataque = 5 + (nivel_jugador * 3)

    #Funcion para que el monstruo muera
    def morir(self):
        if self.hp <= 0:
            print(f'El {self.clase} ha sido derrotado!')
            print(f'Recompensa obtenida: {self.recompensa}')
            return True
        else:
            return False