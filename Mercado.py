from Personaje import Personaje
from Objetos import Pocion, Arma, Objeto
from LimpiarPantalla import limpiar_terminal



class Tienda: 
    def __init__(self): 
        self.inventario = {} 
        self.inventario_tienda() 

    def inventario_tienda(self): 
        #POCIONES CURATIVAS 
        self.inventario["POCIONES CURATIVAS"] = { 
            1: Pocion("pocion", 3, "P C basica", 12, cura = 10), 
            2: Pocion("pocion", 2, "P C media", 18, cura = 15), 
            3: Pocion("pocion", 5, "P C avanzada", 25, cura = 20), 
            4: Pocion("pocion", 1, "P C legendaria", 30, cura = 25)
        }

        #POCIONES DE ATAQUE 
        self.inventario["POCIONES DE ATAQUE"] = { 
            5: Pocion("pocion", 20, "P A basica", 10, dano = 5), 
            6: Pocion("pocion", 12, "P A media", 15, dano = 10), 
            7: Pocion("pocion", 11, "P A avanzada", 20, dano = 15), 
            8: Pocion("pocion", 10, "P A legendaria", 25, dano = 20)
        }

        #POCIONES DE MANA 
        self.inventario["POCIONES DE MANA"] = { 
            9: Pocion("pocion", 11, "P M basica", 6, cura = 5), 
            10: Pocion("pocion", 4, "P M media", 8, cura = 10), 
            11: Pocion("pocion", 6, "P M avanzada", 12, cura = 15), 
            12: Pocion("pocion", 6, "P M legendaria", 18, cura = 20)
        }

        #ARMAS 
        self.inventario["ARMAS"] = {
            #ESPADAS(guerrero)
            13: Arma("espada", 4, "Espada madera", 50, dano = 5),
            14: Arma("espada", 7, "Espada hierro", 100, dano = 10),
            15: Arma("espada", 4, "Espada diamante", 200, dano = 20),
            16: Arma("espada", 2, "Espada legendaria", 500, dano = 50),

            #ARCOS(tirador)
            17: Arma("arco", 4, "Arco simple", 50, dano = 5),
            18: Arma("arco", 7, "Arco reforzado", 100, dano = 10),
            19: Arma("arco", 4, "Arco de caza", 200, dano = 20),
            20: Arma("arco", 2, "Arco ancestral", 500, dano = 50),

            #DAGAS(asesino)
            21: Arma("daga", 4, "Daga oxidada", 50, dano = 5),
            22: Arma("daga", 7, "Daga afilada", 100, dano = 10),
            23: Arma("daga", 4, "Daga de sombra", 200, dano = 20),
            24: Arma("daga", 2, "Daga legendaria", 500, dano = 50),

            #VARITAS(mago)
            25: Arma("varita", 4, "Varita simple", 50, dano = 5),
            26: Arma("varita", 7, "Varita magica", 100, dano = 10),
            27: Arma("varita", 4, "Varita arcana", 200, dano = 20),
            28: Arma("varita", 2, "Varita ancestral", 500, dano = 50),
            
            #ESCUDOS(tanque)
            29: Arma("escudo", 4, "Escudo madera", 50, dano = 5, defensa = 5),
            30: Arma("escudo", 7, "Escudo hierro", 100, dano = 10, defensa = 10),
            31: Arma("escudo", 4, "Escudo reforzado", 200, dano = 20, defensa = 20),
            32: Arma("escudo", 2, "Escudo legendario", 500, dano = 40, defensa = 40),
        }

    #mostrar inventario
    def mostrar_inventario(self): 
        print("\n- - Tienda de Objetos - -") 
        for categoria, items in self.inventario.items(): 
            print(f"\n{categoria}:") 

            for id_item, objeto in items.items(): 
                print(f"{id_item}. {objeto}") 

        print("\n0. Salir") 
    #comprar objetos del inventario
    def comprar(self, id_buscado, jugador): 
        for categoria, items in self.inventario.items(): 
            if id_buscado in items: 
                objeto = items[id_buscado] 
                #comprueba que haya stok
                if objeto.cantidad <= 0: 
                    print("No queda stock.") 
                    return 
                #comprueba que el jugador tenga dinero suficiente
                if jugador.dinero < objeto.precio: 
                    print("No tienes suficiente dinero.") 
                    return 

                jugador.dinero -= objeto.precio   #le quita ek dinero que cuesta el objeto
                objeto.cantidad -= 1              #resta 1 del stok
                objeto_copia = objeto.clonar()    #lo clona
                #si es pocion lo añade a pociones en inventario
                if objeto.tipo == "pocion": 
                    jugador.inventario["pociones"].append(objeto_copia) 
                #si es un arma la añade a armas
                elif objeto.tipo in ("espada", "arco", "daga", "varita", "escudo"): 
                    jugador.inventario["armas"].append(objeto_copia) 
                #sino lo añade a otros
                else: jugador.inventario["otros"].append(objeto_copia)
                #dice el nombre del objeto que compras
                print(f"Has comprado {objeto.nom}") 
                return
        
        print("Objeto no disponible.")

                

