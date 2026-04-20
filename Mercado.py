import json
import os
from Personaje import Personaje
from Objetos import Pocion, Arma, Objeto
from ui import VERDE, AMARILLO, CIAN, AZUL, ROJO, MAGENTA, BLANCO, RESET
from LimpiarPantalla import limpiar_terminal



class Tienda: 
    def __init__(self): 
        self.inventario = {} 
        self.ruta_archivo = os.path.join("Info", "Mercado.json")
        self.inventario_tienda() 

    def inventario_tienda(self): 
        try:
            with open(self.ruta_archivo, "r", encoding="utf-8") as f:
                datos = json.load(f)
            
            for categoria, items in datos.items():
                self.inventario[categoria] = {}
                for id_item, info in items.items():
                    tipo = info.get("tipo")
                    #Convertir ID a int para mantener compatibilidad
                    int_id = int(id_item)
                    
                    if tipo == "pocion":
                        self.inventario[categoria][int_id] = Pocion(
                            tipo, 
                            info["cantidad"], 
                            info["nom"], 
                            info["precio"], 
                            cura = info.get("cura", 0), 
                            dano = info.get("dano", 0)
                        )
                    elif tipo in ("espada", "arco", "daga", "varita", "escudo"):
                        self.inventario[categoria][int_id] = Arma(
                            tipo, 
                            info["cantidad"], 
                            info["nom"], 
                            info["precio"], 
                            dano = info.get("dano", 0), 
                            defensa = info.get("defensa", 0)
                        )
                    else:
                        self.inventario[categoria][int_id] = Objeto(
                            tipo, 
                            info["nom"], 
                            info["precio"]
                        )
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al cargar el mercado: {e}")
            self.inventario = {}

    def guardar_tienda(self):
        datos_para_guardar = {}
        for categoria, items in self.inventario.items():
            datos_para_guardar[categoria] = {}
            for id_item, obj in items.items():
                info = {
                    "tipo": obj.tipo,
                    "nom": obj.nom,
                    "precio": obj.precio,
                    "cantidad": getattr(obj, "cantidad", 1)
                }
                if isinstance(obj, Pocion):
                    if obj.cura > 0: info["cura"] = obj.cura
                    if obj.dano > 0: info["dano"] = obj.dano
                elif isinstance(obj, Arma):
                    if obj.dano > 0: info["dano"] = obj.dano
                    if obj.defensa > 0: info["defensa"] = obj.defensa
                
                datos_para_guardar[categoria][str(id_item)] = info
        
        try:
            with open(self.ruta_archivo, "w", encoding = "utf-8") as f:
                json.dump(datos_para_guardar, f, indent = 4, ensure_ascii = False)
        except Exception as e:
            print(f"Error al guardar el mercado: {e}")

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
                #sino lo anade a otros
                else: 
                    jugador.inventario["otros"].append(objeto_copia)
                #dice el nombre del objeto que compras
                print(f"Has comprado {objeto.nom}") 
                print(f'{objeto.nom} ha sido añadido/a a la mochila!')
                self.guardar_tienda() # Guardar cambios en el JSON
                return
        
        print("Objeto no disponible.")

    #vender objetos
    def vender(self, jugador):
        from LimpiarPantalla import limpiar_terminal
        while True:
            limpiar_terminal()
            print("- - VENDER RESTOS - -")
            otros = jugador.inventario["otros"]
            
            if not otros:
                print("No tienes restos de monstruo para vender.")
                input("\nENTER para volver...")
                break

            print("Selecciona el objeto que deseas vender:")
            for i, obj in enumerate(otros, 1):
                #comprueba si el objeto tiene un precio asignado y es mayor a 0
                if getattr(obj, "precio", 0) > 0:
                    precio = obj.precio
                #Si no tiene precio o hubo un fallo, le da un valor de 15 por defecto
                else:
                    precio = 15
                print(f"{i}. {obj.nom} - Valor: {precio} oro")
            
            print("0. Volver")
            
            eleccion = input("\nID del objeto a vender: ")
            
            if not eleccion.isdigit():
                print("Opcion no valida.")
                input("ENTER...")
                continue
                
            eleccion = int(eleccion)
            if eleccion == 0: 
                break

            idx = eleccion - 1
            if idx < 0 or idx >= len(otros):
                print("Opcion fuera de rango.")
                input("ENTER...")
                continue

            obj_vendido = otros.pop(idx)
            
            #Comprueba si el objeto vendido tiene un precio valido
            if getattr(obj_vendido, "precio", 0) > 0:
                precio = obj_vendido.precio

            #Asigna precio de 15 de oro como plan de respaldo
            else:
                precio = 15
                
            jugador.dinero += precio
            print(f"{VERDE}Has vendido {obj_vendido.nom} por {precio} monedas de oro.{RESET}")
            input("ENTER para continuar...")
