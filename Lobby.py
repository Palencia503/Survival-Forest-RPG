import pygame
import sys
import os
import math
import random
from Personaje import Personaje
from Colors import *
from Tienda import Pocion, Tienda
import GuardarPartida

#Lista global para particulas de luz en el lobby
lista_luces = []

def mochila(screen, reloj, personaje):
    ANCHO, ALTO = screen.get_size()
    fuente = pygame.font.SysFont("Arial", 26)
    fuente_titulo = pygame.font.SysFont("Georgia", 40, bold=True)

    running = True
    seleccion = None

    while running:
        click = False
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "LOBBY"
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        screen.fill((25, 20, 20))

        #Titulo
        titulo = fuente_titulo.render("MOCHILA", True, (255, 215, 0))
        screen.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 40))

        #Lista de objetos
        y = 150
        botones = []
        img_pocion_vida = pygame.image.load("Tienda/Pociones/P_Vida_Mid.png")
        img_pocion_vida = pygame.transform.scale(img_pocion_vida, (80, 80))

        img_pocion_mana = pygame.image.load("Tienda/Pociones/P_Mana_Mid.png")
        img_pocion_mana = pygame.transform.scale(img_pocion_mana, (80, 80))

        img_pocion_vida_max = pygame.image.load("Tienda/Pociones/P_VidaMax.png")
        img_pocion_vida_max = pygame.transform.scale(img_pocion_vida_max, (80, 80))

        img_pocion_buff_ataque = pygame.image.load("Tienda/Pociones/P_Buff_Ataque.png")
        img_pocion_buff_ataque = pygame.transform.scale(img_pocion_buff_ataque, (80, 80))

        for pocion in personaje.inventario["pociones"]:
            rect = pygame.Rect(100, y, 700, 100)
            botones.append((rect, pocion))
            if pocion.cantidad >= 1:
                #Hover
                color = (70, 50, 30) if rect.collidepoint(pos) else (50, 35, 20)
                pygame.draw.rect(screen, color, rect, border_radius = 12)
                pygame.draw.rect(screen, (255, 215, 0), rect, 2, border_radius = 12)

                #Icono Pocion Vida Mid
                screen.blit(img_pocion_vida, (rect.x + 10, rect.y + 10))
                #Nombre
                txt_PocionVida = fuente.render(pocion.nombre, True, (255, 255, 255))
                screen.blit(txt_PocionVida, (rect.x + 110, rect.y + 10))
                #Cantidad
                txt_canti_vida = fuente.render(f"Cantidad: {pocion.cantidad}", True, (200, 200, 200))
                screen.blit(txt_canti_vida, (rect.x + 550, rect.y + 5))

                #Atributos
                txt_attr = fuente.render(
                    f"Cura: {pocion.cura}   Mana: {pocion.mana}   Ataque+: {pocion.buff_ataque}",
                    True, (200, 200, 200)
                )
                screen.blit(txt_attr, (rect.x + 110, rect.y + 55))

                #icono pocion mana
                #Elegir icono segun el nombre de la pocion
                if "Mana" in pocion.nombre:
                    icono = img_pocion_mana
                elif "Vida Max" in pocion.nombre:
                    icono = img_pocion_vida_max
                elif "Vida" in pocion.nombre:
                    icono = img_pocion_vida
                elif "Buff" in pocion.nombre or "Ataque" in pocion.nombre:
                    icono = img_pocion_buff_ataque
                else:
                    icono = None


                #Dibujar icono
                screen.blit(icono, (rect.x + 10, rect.y + 10))

                #Nombre
                txt_PocionMana = fuente.render(pocion.nombre, True, (255, 255, 255))
                screen.blit(txt_PocionMana, (rect.x + 110, rect.y + 10))
                #Cantidad
                txt_canti_mana = fuente.render(f"Cantidad: {pocion.cantidad}", True, (200, 200, 200))
                screen.blit(txt_canti_mana, (rect.x + 550, rect.y + 5))

                #Atributos
                txt_attr = fuente.render(
                    f"Cura: {pocion.cura}   Mana: {pocion.mana}   Ataque+: {pocion.buff_ataque}",
                    True, (200, 200, 200)
                )
                screen.blit(txt_attr, (rect.x + 110, rect.y + 55))

                #icono pocion vida max
                #Elegir icono segun el nombre de la pocion
                if "Mana" in pocion.nombre:
                    icono = img_pocion_mana
                elif "Vida Max" in pocion.nombre:
                    icono = img_pocion_vida_max
                elif "Vida" in pocion.nombre:
                    icono = img_pocion_vida
                elif "Buff" in pocion.nombre or "Ataque" in pocion.nombre:
                    icono = img_pocion_buff_ataque
                else:
                    icono = None

                #Dibujar icono
                screen.blit(icono, (rect.x + 10, rect.y + 10))

                #Nombre
                txt_PocionVidaMax = fuente.render(pocion.nombre, True, (255, 255, 255))
                screen.blit(txt_PocionVidaMax, (rect.x + 110, rect.y + 10))
                #Cantidad
                txt_canti_vida_max = fuente.render(f"Cantidad: {pocion.cantidad}", True, (200, 200, 200))
                screen.blit(txt_canti_vida_max, (rect.x + 550, rect.y + 5))

                #Atributos
                txt_attr = fuente.render(
                    f"Cura: {pocion.cura}   Mana: {pocion.mana}   Ataque+: {pocion.buff_ataque}",
                    True, (200, 200, 200)
                )
                screen.blit(txt_attr, (rect.x + 110, rect.y + 55))

                #icono pocion buff ataque
                #Elegir icono segun el nombre de la pocion
                if "Mana" in pocion.nombre:
                    icono = img_pocion_mana
                elif "Vida Max" in pocion.nombre:
                    icono = img_pocion_vida_max
                elif "Vida" in pocion.nombre:
                    icono = img_pocion_vida
                elif "Buff" in pocion.nombre or "Ataque" in pocion.nombre:
                    icono = img_pocion_buff_ataque
                else:
                    icono = None

                #Dibujar icono
                screen.blit(icono, (rect.x + 10, rect.y + 10))

                #Nombre
                txt_PocionBuffAtaque = fuente.render(pocion.nombre, True, (255, 255, 255))
                screen.blit(txt_PocionBuffAtaque, (rect.x + 110, rect.y + 10))
                #Cantidad
                txt_canti_buff_ataque = fuente.render(f"Cantidad: {pocion.cantidad}", True, (200, 200, 200))
                screen.blit(txt_canti_buff_ataque, (rect.x + 550, rect.y + 5))

                #Atributos
                txt_attr = fuente.render(
                    f"Cura: {pocion.cura}   Mana: {pocion.mana}   Ataque+: {pocion.buff_ataque}",
                    True, (200, 200, 200)
                )
                screen.blit(txt_attr, (rect.x + 110, rect.y + 55))



            #Seleccion
            if seleccion == pocion:
                pygame.draw.rect(screen, (255, 215, 0), rect, 4, border_radius = 12)

            if click and rect.collidepoint(pos):
                seleccion = pocion

            y += 120

        #Boton USAR
        if seleccion:
            btn_usar = pygame.Rect(850, 350, 200, 60)
            col = (50, 150, 50) if btn_usar.collidepoint(pos) else (30, 100, 30)
            pygame.draw.rect(screen, col, btn_usar, border_radius = 10)
            pygame.draw.rect(screen, (255, 255, 255), btn_usar, 2, border_radius = 10)

            txt_u = fuente.render("USAR", True, (255, 255, 255))
            screen.blit(txt_u, (btn_usar.centerx - txt_u.get_width() // 2,
                                btn_usar.centery - txt_u.get_height() // 2))

            if click and btn_usar.collidepoint(pos) and seleccion.cantidad > 0:
                personaje.usar_pocion(seleccion)
                seleccion = None

        pygame.display.flip()
        reloj.tick(60)

def ejecutar_tienda(screen, reloj, personaje):
    ANCHO, ALTO = screen.get_size()
    fuente = pygame.font.SysFont("Arial", 28)
    fuente_titulo = pygame.font.SysFont("Georgia", 40, bold = True)

    #Cargar iconos
    iconos_pociones = {
        "Pocion de Mana": pygame.image.load("Tienda/Pociones/P_Mana_Mid.png"),
        "Pocion de Vida": pygame.image.load("Tienda/Pociones/P_Vida_Mid.png"),
        "Pocion Vida Max": pygame.image.load("Tienda/Pociones/P_VidaMax.png"),
        "Pocion Buff Ataque": pygame.image.load("Tienda/Pociones/P_Buff_Ataque.png")
    }

    #Pociones disponibles
    pociones = [
        {"obj": Pocion("Pocion de Mana", 50, 0, 0), "precio": 80, "icono": iconos_pociones["Pocion de Mana"]},
        {"obj": Pocion("Pocion de Vida", 0, 40, 0), "precio": 120, "icono": iconos_pociones["Pocion de Vida"]},
        {"obj": Pocion("Pocion Vida Max", 0, 100, 0), "precio": 200, "icono": iconos_pociones["Pocion Vida Max"]},
        {"obj": Pocion("Pocion Buff Ataque", 0, 0, 10), "precio": 150, "icono": iconos_pociones["Pocion Buff Ataque"]}
    ]

    botones = []
    y = 200
    for p in pociones:
        rect = pygame.Rect(150, y, 500, 80)
        botones.append((rect, p))
        y += 100

    running = True
    while running:
        click = False
        pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return "LOBBY"

        screen.fill((40, 20, 10))

        #Titulo
        titulo = fuente_titulo.render("TIENDA", True, (255, 215, 0))
        screen.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 50))

        #Dinero del jugador
        txt_dinero = fuente.render(f"Oro: {personaje.dinero}", True, (255, 255, 255))
        screen.blit(txt_dinero, (50, 120))

        #Mostrar pociones
        for rect, p in botones:
            color = (120, 80, 40) if rect.collidepoint(pos) else (90, 60, 30)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            pygame.draw.rect(screen, (255, 215, 0), rect, 2, border_radius=10)

            #Icono
            icono = pygame.transform.scale(p["icono"], (60, 60))
            screen.blit(icono, (rect.x + 10, rect.y + 10))

            #Texto
            texto = fuente.render(f"{p['obj'].nombre} - {p['precio']} oro", True, (255, 255, 255))
            screen.blit(texto, (rect.x + 90, rect.y + 25))

            #Comprar
            if click and rect.collidepoint(pos):
                if personaje.dinero >= p["precio"]:
                    personaje.dinero -= p["precio"]
                    personaje.agregar_pocion_a_inventario(p["obj"])
                else:
                    print("No tienes suficiente oro")

        pygame.display.flip()
        reloj.tick(60)

def ejecutar(screen, reloj, personaje):
    ANCHO, ALTO = screen.get_size()
    clase_usuario = personaje.clase.lower()

    #Carga de recursos de fondo
    try:
        img = pygame.image.load("Backgrounds/lobby_bg.png").convert()
        fondo_lobby = pygame.transform.scale(img, (ANCHO, ALTO))
    except:
        fondo_lobby = pygame.Surface((ANCHO, ALTO))
        fondo_lobby.fill((30, 30, 40))

    #Carga del sprite del personaje
    try:
        sprite_pj = pygame.image.load(f"Characters/Personajes/{clase_usuario}.png").convert_alpha()
        sprite_pj = pygame.transform.scale(sprite_pj, (200, 300))
    except:
        sprite_pj = pygame.Surface((200, 300), pygame.SRCALPHA)
        pygame.draw.rect(sprite_pj, (100, 100, 200), (0, 0, 200, 300))

    #Fuentes estilizadas
    fuente_ui = pygame.font.SysFont("Arial", 22, bold = True)
    fuente_botones = pygame.font.SysFont("Verdana", 28, bold = True)
    fuente_titulo = pygame.font.SysFont("Georgia", 32, bold = True, italic = True)

    superficie_luz = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    running = True
    proximo_estado = "LOBBY"
    msg_guardado_timer = 0   #timer para el mensaje de confirmacion

    while running:
        pos_mouse = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        #Simular parpadeo de antorchas en el ambiente oscuro
        flicker = random.randint(160, 200)
        superficie_luz.fill((0, 0, 0, 255 - flicker))

        #DIBUJO DE FONDO
        screen.blit(fondo_lobby, (0, 0))

        #------LOGICA Y DIBUJO DE LUCES (Particulas flotantes magicas)------
        if random.randint(0, 2) == 0 and len(lista_luces) < 120:
            x_luz = random.randint(50, ANCHO - 50)
            y_luz = random.randint(ALTO // 2, ALTO - 50)
            colores = [(255, 215, 0), (100, 200, 255), (200, 100, 255)]
            vida_l = random.randint(100, 250)
            lista_luces.append({
                "x": x_luz, "y": y_luz, "vel_y": random.uniform(-0.4, -1.2), 
                "vida_max": vida_l, "vida_actual": vida_l,
                "radio": random.uniform(1.5, 4.0),
                "color": random.choice(colores)
            })

        for luz in lista_luces[:]:
            luz["y"] += luz["vel_y"]
            luz["vida_actual"] -= 1
            if luz["vida_actual"] <= 0:
                lista_luces.remove(luz)
                continue

            alfa = int((luz["vida_actual"] / luz["vida_max"]) * 180)
            r_size = int(luz["radio"] * 4)
            surf_luz = pygame.Surface((r_size, r_size), pygame.SRCALPHA)
            pygame.draw.circle(surf_luz, ( * luz["color"], alfa), (r_size // 2, r_size // 2), luz["radio"])
            screen.blit(surf_luz, (luz["x"] - r_size // 2, luz["y"] - r_size // 2))
        #--------------------------------------------------------------------------------
        #BARRA SUPERIOR ESTATICA
        pygame.draw.rect(screen, (20, 20, 20), (0, 0, ANCHO, 80)) 
        pygame.draw.line(screen, (255, 215, 0), (0, 80), (ANCHO, 80), 3)

        #Nombre, Nivel y Clase en la barra superior
        txt_lv = fuente_botones.render(f"LV. {personaje.nivel}", True, (255, 215, 0))
        screen.blit(txt_lv, (30, 20))
        txt_clase = fuente_botones.render(f"|  {personaje.clase.upper()}", True, (255, 255, 255))
        screen.blit(txt_clase, (30 + txt_lv.get_width() + 10, 20))

        #Nivel de la mazmorra en la parte derecha de la barra superior
        txt_maz = fuente_botones.render(f"MAZMORRA: NIVEL {personaje.nivel_mazmorra}", True, (255, 100, 100))
        screen.blit(txt_maz, (ANCHO - txt_maz.get_width() - 30, 20))
   
        #Titulo del juego en el centro
        txt_titulo = fuente_titulo.render("SF-RPG", True, (255, 215, 0))
        screen.blit(txt_titulo, (ANCHO//2 - txt_titulo.get_width()//2, 22))

        #PERSONAJE EN MOVIMIENTO GENTIL
        bob = math.sin(pygame.time.get_ticks() * 0.005) * 5
        screen.blit(sprite_pj, (ANCHO // 2 - 100, 330 + bob))
        
        #Sombra en los pies del personaje
        sombra = pygame.Surface((220, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra, (0, 0, 0, 120), (0, 0, 220, 30))
        screen.blit(sombra, (ANCHO // 2 - 110, 620))

        #MENU DERECHO (BOTONES)
        margen_x = 850
        ancho_btn = 300
        alto_btn = 60

        #-----------------BOTON: ENTRAR MAZMORRA--------------------
        btn_jugar = pygame.Rect(margen_x, 300, ancho_btn , alto_btn + 50)
        col_j = (200, 50, 50) if btn_jugar.collidepoint(pos_mouse) else (150, 20, 20)
        pygame.draw.rect(screen, col_j, btn_jugar, border_radius = 12)
        pygame.draw.rect(screen, (255, 215, 0), btn_jugar, 2, border_radius = 12)
        fuente_maz_btn = pygame.font.SysFont("Verdana", 22, bold = True)
        txt_j = fuente_maz_btn.render("ENTRAR MAZMORRA", True, (255, 255, 255))
        screen.blit(txt_j, (btn_jugar.centerx - txt_j.get_width() // 2, btn_jugar.centery - txt_j.get_height() // 2))

        #------------------BOTON: TIENDA--------------------
        btn_tienda = pygame.Rect(margen_x, 450, ancho_btn, alto_btn)
        col_tienda = (200, 140, 60) if btn_tienda.collidepoint(pos_mouse) else (150, 100, 30)
        pygame.draw.rect(screen, col_tienda, btn_tienda, border_radius=12)
        pygame.draw.rect(screen, (255, 215, 0), btn_tienda, 2, border_radius=12)
        txt_tienda = fuente_botones.render("TIENDA", True, (255, 255, 255))
        screen.blit(txt_tienda, (btn_tienda.centerx - txt_tienda.get_width()//2,
                                btn_tienda.centery - txt_tienda.get_height()//2))

        #------------------BOTON: GUARDAR--------------------
        btn_guardar = pygame.Rect(margen_x, 120, ancho_btn, alto_btn)
        col_g = (50, 160, 80) if btn_guardar.collidepoint(pos_mouse) else (30, 110, 55)
        pygame.draw.rect(screen, col_g, btn_guardar, border_radius = 12)
        pygame.draw.rect(screen, (255, 215, 0), btn_guardar, 2, border_radius = 12)
        txt_g = fuente_botones.render("GUARDAR", True, (255, 255, 255))
        screen.blit(txt_g, (btn_guardar.centerx - txt_g.get_width() // 2, btn_guardar.centery - txt_g.get_height() // 2))

        if click and btn_guardar.collidepoint(pos_mouse):
            GuardarPartida.guardar_partida(personaje)
            msg_guardado_timer = 120   #frames que durara el mensaje

        #Mensaje de confirmacion de guardado
        if msg_guardado_timer > 0:
            fuente_msg = pygame.font.SysFont("Arial", 20, bold=True)
            txt_ok = fuente_msg.render("Partida guardada", True, (100, 255, 150))
            screen.blit(txt_ok, (margen_x + ancho_btn // 2 - txt_ok.get_width() // 2, btn_guardar.bottom + 15))
            msg_guardado_timer -= 1

        #----------------------MOCHILA--------------------
        btn_mochila = pygame.Rect(margen_x, 535, ancho_btn, alto_btn)
        col_m = (200, 140, 60) if btn_mochila.collidepoint(pos_mouse) else (150, 100, 30)
        pygame.draw.rect(screen, col_m, btn_mochila, border_radius=12)
        pygame.draw.rect(screen, (255, 215, 0), btn_mochila, 2, border_radius=12)
        txt_m = fuente_botones.render("MOCHILA", True, (255, 255, 255))
        screen.blit(txt_m, (btn_mochila.centerx - txt_m.get_width()//2, btn_mochila.centery - txt_m.get_height()//2))

        if click and btn_mochila.collidepoint(pos_mouse):
            return "MOCHILA"
       
        #------------------BOTON: SALIR--------------------
        btn_s = pygame.Rect(margen_x, 630, ancho_btn, alto_btn)
        col_s = (130, 40, 40) if btn_s.collidepoint(pos_mouse) else (90, 20, 20)
        pygame.draw.rect(screen, col_s, btn_s, border_radius = 12)
        pygame.draw.rect(screen, (255, 215, 0), btn_s, 2, border_radius = 5)
        txt_s = fuente_botones.render("SALIR", True, (255, 255, 255))
        screen.blit(txt_s, (btn_s.centerx - txt_s.get_width()//2, btn_s.centery - txt_s.get_height()//2))

        #---------------------------------------------------------

        #PANEL DE ESTADISTICAS A LA IZQUIERDA
        panel_stats = pygame.Rect(50, 420, 300, 280)
        pygame.draw.rect(screen, (25, 25, 30), panel_stats, border_radius=15)
        pygame.draw.rect(screen, (255, 215, 0), panel_stats, 2, border_radius=15)

        #Mostrar estadisticas actuales del personaje POO
        txt_est = fuente_ui.render("ESTADISTICAS", True, (255, 215, 0))
        screen.blit(txt_est, (panel_stats.x + 20, panel_stats.y + 15))
        pygame.draw.line(screen, (100, 100, 100), (panel_stats.x + 20, panel_stats.y + 45), (panel_stats.right - 20, panel_stats.y + 45), 1)

        detalles_stats = [
            f"Vida: {personaje.hp} / {personaje.hp_max}",
            f"Ataque Base: {personaje.ataque}",
            f"Escudo/Defensa: {personaje.escudo}",
            f"Mana: {personaje.mana}",
            f"Arma: {personaje.arma['nom']}",
            f"Daño de Arma: {personaje.arma['dano']}"
        ]
        
        for i, text in enumerate(detalles_stats):
            t_stat = fuente_ui.render(text, True, (230, 230, 230))
            screen.blit(t_stat, (panel_stats.x + 20, panel_stats.y + 60 + (i * 32)))

        #DIBUJO DE EFECTOS MAGICOS/AMBIENTALES
        screen.blit(superficie_luz, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

        #ORO GLOBAL Y EXP
        screen.blit(fuente_ui.render(f"ORO: {personaje.dinero}", True, (255, 235, 100)), (40, 100))
        
        #Barra de EXP
        exp_ratio = personaje.exp / max(1, personaje.exp_necesaria)
        pygame.draw.rect(screen, (50, 50, 50), (40, 135, 250, 15), border_radius=5)
        pygame.draw.rect(screen, (100, 200, 100), (40, 135, int(250 * exp_ratio), 15), border_radius=5)
        txt_exp = fuente_ui.render(f"EXP: {personaje.exp}/{personaje.exp_necesaria}", True, (255, 255, 255))
        screen.blit(txt_exp, (40, 155))

        #LOGICA DE ENTRADAS
        if click:
            if btn_jugar.collidepoint(pos_mouse):
                GuardarPartida.guardar_partida(personaje)  #Guardado automatico al entrar a mazmorra
                proximo_estado = "COMBATE"
                running = False

            elif btn_tienda.collidepoint(pos_mouse):
                proximo_estado = "TIENDA"
                running = False

            elif btn_s.collidepoint(pos_mouse):
                proximo_estado = "SALIR"
                running = False

        pygame.display.flip()
        reloj.tick(60)

    return proximo_estado