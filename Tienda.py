import pygame
from Personaje import Personaje

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


class Tienda:
    def __init__(self):
        #carga iconos
        self.iconos = {
            "mana": pygame.image.load("Tienda/Pociones/P_Mana_Mid.png"),
            "vida": pygame.image.load("Tienda/Pociones/P_Vida_Mid.png"),
            "vida_max": pygame.image.load("Tienda/Pociones/P_VidaMax.png"),
            "buff_ataque": pygame.image.load("Tienda/Pociones/P_Buff_Ataque.png")
        }

        #Productos a la venta
        self.productos = [
            {
                "pocion": Pocion("Pocion de Mana", 50, 0, 0, "Tienda/Pociones/P_Mana_Mid.png"),
                "precio": 80,
                "icono": self.iconos["mana"]
            },
            {
                "pocion": Pocion("Pocion de Vida", 0, 40, 0, "Tienda/Pociones/P_Vida_Mid.png"),
                "precio": 120,
                "icono": self.iconos["vida"]
            },
            {
                "pocion": Pocion("Pocion Vida Max", 0, 100, 0, "Tienda/Pociones/P_VidaMax.png"),
                "precio": 250,
                "icono": self.iconos["vida_max"]
            },
            {
                "pocion": Pocion("Pocion Buff Ataque", 0, 0, 10, "Tienda/Pociones/P_Buff_Ataque.png"),
                "precio": 150,
                "icono": self.iconos["buff_ataque"]
            }
        ]

    def comprar(self, personaje, producto):
        precio = producto["precio"]
        if personaje.dinero >= precio:
            personaje.dinero -= precio
            personaje.agregar_pocion_a_inventario(producto["pocion"])
            return True

        print("No tienes suficiente oro")
        return False
