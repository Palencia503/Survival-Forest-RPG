import random
from Personaje import Personaje, Monstruo
from Objetos import Arma, Pocion, Objeto
from LimpiarPantalla import limpiar_terminal
from ui import VERDE, AMARILLO, CIAN, AZUL, ROJO, MAGENTA, BLANCO, RESET

def combate(jugador, monstruo):
    print(f"\n{ROJO}{jugador.clase} vs {monstruo.clase}{RESET}")
    ronda = 1 
    #combate si los dos tienen vida
    while jugador.hp > 0 and monstruo.hp > 0:
        print(f"\n{AMARILLO}- - Ronda {ronda} - -{RESET}")
        ronda += 1

        print(f"{VERDE}{jugador.clase} HP: {jugador.hp}{RESET} | {ROJO}{monstruo.clase} HP: {monstruo.hp}{RESET}")
        #huir o atacar
        accion = input(f"{CIAN}¿Que quieres hacer? {RESET}({VERDE}a = atacar{RESET} / {ROJO}h = huir{RESET}): ").lower()
        if accion in ("h", "huir"):
            print("Has huido del combate.")
            return "huido"

        if accion not in ("a", "atacar"):
            print("Opcion no valida.")
            continue

        #Defensa independiente
        defiende_monstruo = random.choice([True, False])
        defiende_jugador = random.choice([True, False])

        #ATAQUE DEL JUGADOR
        if defiende_monstruo:
            print("El monstruo bloqueo tu ataque.")
        else:
            dano_total = jugador.ataque + jugador.arma["dano"]
            dano_infligido = max(0, dano_total - monstruo.escudo)
            monstruo.hp -= dano_infligido
            print(f"Le hiciste {dano_infligido} de dano.")

        if monstruo.hp <= 0:
            break

        #ATAQUE DEL MONSTRUO
        if defiende_jugador:
            print("Bloqueaste el ataque del monstruo.")
        else:
            dano_m = max(0, monstruo.ataque - jugador.escudo)
            jugador.hp -= dano_m
            print(f"El monstruo te golpea y te quita {dano_m} de dano.")

    #RESULTADO FINAL
    if jugador.hp <= 0:
        print(f"\n{ROJO}Has sido derrotado...{RESET}")
        return "derrota"

    print(f"\n{VERDE}¡Has vencido al monstruo!{RESET}")
    monstruo.morir()

    #recompensa del monstruo
    recompensa = monstruo.recompensa

    #oro
    if "oro" in recompensa:
        jugador.dinero += recompensa["oro"]
        print(f"Has ganado {recompensa['oro']} monedas de oro.")

    #objetos
    if "tipo" in recompensa:
        if random.randint(1, 100) <= 35:
            if recompensa["tipo"] == "armas":
                dano = 0
                defensa = 0

                if "dano" in recompensa:
                    dano = recompensa["dano"]

                if "defensa" in recompensa:
                    defensa = recompensa["defensa"]

                arma = Arma("arma", 1, recompensa["nom"], 0, dano, defensa)
                jugador.inventario["armas"].append(arma)
                print(f"Has obtenido un arma: {recompensa['nom']}")

            elif recompensa["tipo"] == "pociones":
                cura = recompensa.get("curacion", 0)
                dano = recompensa.get("dano", 0)
                pocion = Pocion("pocion", 1, recompensa["nom"], 0, cura = cura, dano = dano)
                jugador.inventario["pociones"].append(pocion)
                print(f"Has obtenido una pocion: {recompensa['nom']}")

            else:
                precio_venta = random.randint(15, 35)
                obj = Objeto("otros", recompensa["nom"], precio_venta)
                jugador.inventario["otros"].append(obj)
                print(f"Has obtenido un objeto especial: {recompensa['nom']}")

    #exp y oro
    exp = 20
    oro = random.randint(10, 50)
    jugador.exp += exp
    jugador.dinero += oro

    print(f"¡Ganaste {exp} puntos de experiencia!.")
    return "victoria"



