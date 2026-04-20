#clase de objetos
class Objeto:
    def __init__(self, tipo, nom, precio):
        self.tipo = tipo
        self.nom = nom
        self.precio = precio
    #devuelve una copia simple del objeto base
    def clonar(self): 
        return Objeto(self.tipo, self.nom, self.precio)
    
#Clase para pociones(curacion o daño)
class Pocion(Objeto):
    def __init__(self, tipo, cantidad, nom, precio, cura = 0, dano = 0):
        super().__init__(tipo, nom, precio)
        self.cantidad = cantidad
        self.cura = cura
        self.dano = dano
    #devuelve una copia de la pocion
    def clonar(self):
        return Pocion(self.tipo, 1, self.nom, self.precio, self.cura, self.dano)
    #texto que se muestra en el menu
    def __str__(self):
        efecto = ""
        if self.cura > 0:
            efecto = f"Cura: {self.cura}"

        if self.dano > 0:
            if efecto:
                efecto += ", "
            efecto += f"Daño: {self.dano}"
            
        return f"{self.nom} (x{self.cantidad}) - Precio: {self.precio} - {efecto}"
    
#Clase para armas
class Arma(Objeto):
    def __init__(self, tipo, cantidad, nom, precio, dano=0, defensa=0):
        super().__init__(tipo, nom, precio)
        self.cantidad = cantidad
        self.dano = dano
        self.defensa = defensa
    #Texto que se muestra en el menu de armas
    def __str__(self):
        texto = f"{self.nom} (x{self.cantidad}) - Precio: {self.precio}"
        if self.dano > 0:
            texto += f" - Dano: {self.dano}"
        if self.defensa > 0:
            texto += f" - Defensa: {self.defensa}"
        return texto
    #devuelve una copia del arma
    def clonar(self):
        return Arma(self.tipo, 1, self.nom, self.precio, self.dano, self.defensa)
