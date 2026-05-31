import pygame
import os
import json
import math
import random
from Personaje import Personaje, Pocion
import GuardarPartida

COLOR_FONDO_MENU = (18, 18, 18)
COLOR_PANEL_STATS = (30, 30, 30)
COLOR_ORO = (255, 215, 0)
COLOR_TEXTO = (255, 255, 255)
COLOR_BTN = (51, 51, 51)
COLOR_BTN_HOVER = (80, 80, 80)
COLOR_ACENTO = (45, 90, 39)
COLOR_ACENTO_HOVER = (62, 125, 54)

def cargar_datos():
    try:
        if not os.path.exists("Info"): 
            os.makedirs("Info")
        with open("Info/Personajes.json", "r", encoding="utf-8") as f:
            personajes = json.load(f)
            clase_actual = list(personajes.values())[0]
            return personajes, clase_actual
    except Exception:
        personajes = {"5": {"clase": "Guerrero", "hp": 120, "mana": 0, "escudo": 0, "ataque": 15}}
        clase_actual = personajes["5"]
        return personajes, clase_actual

def actualizar_pj_visual(clase_actual):
    nombre = clase_actual["clase"].lower()
    ruta = f"Characters/Personajes/{nombre}.png"
    if os.path.exists(ruta):
        img = pygame.image.load(ruta).convert_alpha()
        return pygame.transform.scale(img, (250, 350))
    return None

def dibujar_luces(screen, luces, ANCHO_PY, ALTO):
    if random.randint(0, 5) == 0 and len(luces) < 50:
        x = random.randint(100, ANCHO_PY - 100)
        y = random.randint(ALTO // 2, ALTO - 100)
        colores = [(255, 215, 0), (100, 200, 255), (200, 100, 255)]
        vida = random.randint(100, 250)
        luces.append({
            "x": x, "y": y, "vel_y": random.uniform(-0.5, -1.5), 
            "vida_max": vida, "vida_actual": vida,
            "radio": random.uniform(2.0, 4.0), "color": random.choice(colores)
        })

    for luz in luces[:]:
        luz["y"] += luz["vel_y"]
        luz["vida_actual"] -= 1
        if luz["vida_actual"] <= 0:
            luces.remove(luz)
            continue

        alfa = int((luz["vida_actual"] / luz["vida_max"]) * 180)
        surf = pygame.Surface((int(luz["radio"]*4), int(luz["radio"]*4)), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*luz["color"], alfa), (luz["radio"]*2, luz["radio"]*2), luz["radio"])
        screen.blit(surf, (luz["x"] - luz["radio"]*2, luz["y"] - luz["radio"]*2))

def ejecutar(screen, reloj):
    ANCHO, ALTO = screen.get_size()
    ANCHO_PY = 800
    
    personajes, clase_actual = cargar_datos()
    img_pj = actualizar_pj_visual(clase_actual)
    bg_img = None
    luces = []
    
    if os.path.exists("Backgrounds/lobby_bg.png"):
        bg = pygame.image.load("Backgrounds/lobby_bg.png").convert()
        bg_img = pygame.transform.scale(bg, (ANCHO_PY, ALTO))
    else:
        bg_img = pygame.Surface((ANCHO_PY, ALTO))
        bg_img.fill((20, 20, 20))
        
    fuente_titulo = pygame.font.SysFont("Georgia", 36, bold=True, italic=True)
    fuente_nombre = pygame.font.SysFont("Verdana", 28, bold=True)
    fuente_stats = pygame.font.SysFont("Courier New", 20, bold=True)
    fuente_btn = pygame.font.SysFont("Arial", 18, bold=True)
    fuente_btn_play = pygame.font.SysFont("Verdana", 20, bold=True)
    
    running = True
    personaje_seleccionado = None
    
    while running:
        pos_mouse = pygame.mouse.get_pos()
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
                
        #Dibuja Zona Izquierda
        screen.blit(bg_img, (0, 0))
        dibujar_luces(screen, luces, ANCHO_PY, ALTO)
        
        t = pygame.time.get_ticks()
        offset_y = math.sin(t * 0.005) * 5
        pj_x = (ANCHO_PY // 1.6) - 200
        pj_y = (ALTO // 1.4) - 150 + offset_y
        
        #sombra dinamica en piso
        sombra_surf = pygame.Surface((300, 50), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra_surf, (0, 0, 0, 100), (0, 0, 300, 50))
        screen.blit(sombra_surf, (pj_x + 50, ALTO - 200))
        
        if img_pj:
            screen.blit(img_pj, (pj_x, pj_y))
            
        #Dibuja UI que separa la pantalla y muestra info del personaje
        rect_derecho = pygame.Rect(ANCHO_PY, 0, ANCHO - ANCHO_PY, ALTO)
        pygame.draw.rect(screen, COLOR_FONDO_MENU, rect_derecho)
        pygame.draw.line(screen, COLOR_ORO, (ANCHO_PY, 0), (ANCHO_PY, ALTO), 3)
        
        t_tit = fuente_titulo.render("SURVIVAL FOREST", True, COLOR_ORO)
        screen.blit(t_tit, (ANCHO_PY + (400 - t_tit.get_width())//2, 40))
        
        t_nom = fuente_nombre.render(clase_actual["clase"].upper(), True, COLOR_ORO)
        screen.blit(t_nom, (ANCHO_PY + (400 - t_nom.get_width())//2, 120))
        
        rect_stats = pygame.Rect(ANCHO_PY + 40, 180, 320, 200)
        pygame.draw.rect(screen, COLOR_PANEL_STATS, rect_stats, border_radius=10)
        pygame.draw.rect(screen, COLOR_ORO, rect_stats, 2, border_radius=10)
        
        stats_textos = [
            f"HP  : {clase_actual['hp']}",
            f"ATK : {clase_actual['ataque']}",
            f"MANA: {clase_actual['mana']}",
            f"DEF : {clase_actual['escudo']}"
        ]
        for i, st in enumerate(stats_textos):
            t_st = fuente_stats.render(st, True, COLOR_TEXTO)
            screen.blit(t_st, (rect_stats.left + 50, rect_stats.top + 30 + (i*40)))
            
        #lista de Clases a Elegir
        start_y = 420
        for i, (key, info) in enumerate(personajes.items()):
            rect_btn = pygame.Rect(ANCHO_PY + 80, start_y + (i * 60), 240, 45)
            color = COLOR_BTN
            if rect_btn.collidepoint(pos_mouse):
                color = COLOR_BTN_HOVER
                if click:
                    clase_actual = info
                    img_pj = actualizar_pj_visual(clase_actual)
            
            borde = 1
            if clase_actual["clase"] == info["clase"]:
                color = COLOR_ORO
                borde = 0
                
            pygame.draw.rect(screen, color, rect_btn, border_radius = 5)
            if borde > 0: 
                pygame.draw.rect(screen, COLOR_ORO, rect_btn, 1, border_radius = 5)
            
            col_txt = (0, 0, 0) if clase_actual["clase"] == info["clase"] else COLOR_TEXTO
            t_clase = fuente_btn.render(info["clase"].upper(), True, col_txt)
            screen.blit(t_clase, (rect_btn.centerx - t_clase.get_width() // 2, rect_btn.centery - t_clase.get_height() // 2))

        #confirma Seleccion - NUEVA AVENTURA
        btn_play = pygame.Rect(ANCHO_PY + 60, ALTO - 80, 280, 55)
        c_play = COLOR_ACENTO_HOVER if btn_play.collidepoint(pos_mouse) else COLOR_ACENTO
        pygame.draw.rect(screen, c_play, btn_play, border_radius = 10)
        pygame.draw.rect(screen, COLOR_ORO, btn_play, 2, border_radius = 10)
        t_play = fuente_btn_play.render("NUEVA AVENTURA", True, COLOR_TEXTO)
        screen.blit(t_play, (btn_play.centerx - t_play.get_width()//2, btn_play.centery - t_play.get_height()//2))

        if click and btn_play.collidepoint(pos_mouse):
            personaje_seleccionado = clase_actual
            running = False

        #CONTINUAR PARTIDA(solo visible si ya existe partida guardada)
        if GuardarPartida.existe_partida_guardada():
            btn_continuar = pygame.Rect(ANCHO_PY + 60, ALTO - 145, 280, 55)
            c_cont = (40, 180, 100) if btn_continuar.collidepoint(pos_mouse) else (25, 130, 70)
            pygame.draw.rect(screen, c_cont, btn_continuar, border_radius = 10)
            pygame.draw.rect(screen, COLOR_ORO, btn_continuar, 2, border_radius = 10)
            t_cont = fuente_btn_play.render("CONTINUAR", True, COLOR_TEXTO)
            screen.blit(t_cont, (btn_continuar.centerx - t_cont.get_width()//2, btn_continuar.centery - t_cont.get_height()//2))

            if click and btn_continuar.collidepoint(pos_mouse):
                return "CONTINUAR"
        
        pygame.display.flip()
        reloj.tick(60)

    #Si se selecciono una clase, instanciamos la clase Personaje real y equipamos arma inicial
    if personaje_seleccionado:
        clase_nom = personaje_seleccionado["clase"]
        pj = Personaje(
            clase=clase_nom,
            hp=personaje_seleccionado["hp"],
            hp_max=personaje_seleccionado["hp"],
            mana=personaje_seleccionado["mana"],
            mana_max=personaje_seleccionado["mana"],
            escudo=personaje_seleccionado["escudo"],
            escudo_base=personaje_seleccionado["escudo"],
            ataque=personaje_seleccionado["ataque"]
        )
        pj.dinero += 1000  #Otorga 1000 de oro inicial para pruebas
        
        #Carga el arma inicial
        try:
            with open("Info/ArmasIniciales.json", "r", encoding="utf-8") as f:
                armas_iniciales = json.load(f)
            arma_info = armas_iniciales.get(clase_nom)
            
            if arma_info:
                pj.equipar_arma(arma_info["nom"], arma_info["dano"], arma_info["defensa"])
        except Exception as e:
            print("Error equipando arma inicial:", e)
            
        return pj

    return None
