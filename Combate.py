import pygame
import sys
import random
from habilidades import ataques, ataques_enemigos
from Colors import *
from Mazmorra import *
from Personaje import Personaje, Monstruo
import GuardarPartida

#----------------------------------Pantalla de victoria------------------------------------------
def mostrar_victoria(screen, reloj, personaje, enemigo):
    ANCHO, ALTO = screen.get_size()
    fuente_grande = pygame.font.SysFont("Georgia", 60, bold=True, italic=True)
    fuente_media  = pygame.font.SysFont("Arial", 28, bold=True)
    fuente_small  = pygame.font.SysFont("Verdana", 22)

    #aplica recompensas
    personaje.dinero += enemigo["recompensa"]
    personaje.ganar_exp(enemigo["exp"])

    continuar = False

    while not continuar:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:   # SOLO ENTER
                    continuar = True

        #fondo oscuro
        overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        #titulo
        txt_vic = fuente_grande.render("¡VICTORIA!", True, (255, 215, 0))
        screen.blit(txt_vic, (ANCHO//2 - txt_vic.get_width()//2, ALTO//2 - 140))

        #enemigo derrotado
        txt_der = fuente_media.render(f"{enemigo['nombre']} derrotado", True, (255, 255, 255))
        screen.blit(txt_der, (ANCHO//2 - txt_der.get_width()//2, ALTO//2 - 60))

        #texto de proximo nivel no disponible
        txt_proximo_nivel = fuente_media.render("Proximo Nivel: ¡No Disponible!", True, (RED))
        screen.blit(txt_proximo_nivel, (ANCHO//2 - txt_proximo_nivel.get_width()//2, ALTO//2 - 20))

        #Oro
        txt_oro = fuente_media.render(f"+ {enemigo['recompensa']} Oro", True, (255, 220, 50))
        screen.blit(txt_oro, (ANCHO//2 - txt_oro.get_width()//2, ALTO//2 + 20))

        #EXP
        txt_exp = fuente_media.render(f"+ {enemigo['exp']} EXP", True, (100, 220, 255))
        screen.blit(txt_exp, (ANCHO//2 - txt_exp.get_width()//2, ALTO//2 + 75))

        #Texto de continuar
        txt_skip = fuente_small.render("Pulsa ENTER para continuar", True, (180, 180, 180))
        screen.blit(txt_skip, (ANCHO//2 - txt_skip.get_width()//2, ALTO//2 + 165))

        pygame.display.flip()
        reloj.tick(60)


#------------------------------------------------------------------------------------------------------

#----------------------------Numeros de daño flotantes-------------------------------------------------
def agregar_numero(lista, x, y, valor, color):
    lista.append({"x": x, "y": y, "valor": valor, "color": color,
                  "vida": 60, "vida_max": 60})  #60 frames = 1 seg

def actualizar_numeros(lista, screen, fuente):
    #Recorre una copia de la lista para poder eliminar elementos sin problemas
    for numero in lista[:]:

        #Reduce la vida del numero (cuanto tiempo le queda en pantalla)
        numero["vida"] -= 1

        #Hace que el numero suba lentamente
        numero["y"] -= 1.2

        #Si ya no tiene vida, lo quita de la lista
        if numero["vida"] <= 0:
            lista.remove(numero)
            continue

        #Calcula la transparencia (alfa) segun la vida que le queda
        vida_actual = numero["vida"]
        vida_maxima = numero["vida_max"]
        alfa = int(255 * (vida_actual / vida_maxima))

        #Renderiza el texto del numero(-10)
        texto = f"-{numero['valor']}"
        superficie = fuente.render(texto, True, numero["color"])

        #Aplica la transparencia
        superficie.set_alpha(alfa)

        #Dibuja el numero en pantalla, centrado horizontalmente
        x = int(numero["x"]) - superficie.get_width() // 2
        y = int(numero["y"])
        screen.blit(superficie, (x, y))

#──-------------------------------Combate principal---------------------------------------------------------
def seleccion_piso(screen, reloj, personaje):
    ANCHO, ALTO = screen.get_size()
    fuente_titulo = pygame.font.SysFont("Arial", 20, bold = True)
    fuentePTitulo = pygame.font.SysFont("Arial", 50, bold = True)

    #carga de imagen del personaje
    imagen = pygame.image.load(f"Characters/Personajes/{personaje.clase}.png")
    personaje_img  = pygame.transform.scale(imagen, (120, 160))

    #Fondo
    fondo = pygame.image.load("Backgrounds/Fondo_SeleccionModo.png")
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    #Variables para los pisos
    pisos_x = ANCHO // 2 - 500
    pisos_y = ALTO // 2 - 250

    #Menu pisos
    menu_pisos = True

    while menu_pisos:
        #Definicion de areas
        btn_volver = pygame.Rect(ANCHO // 2 - 100, ALTO // 2 + 200, 200, 50)
        piso1 = pygame.Rect(pisos_x, pisos_y, 280, 210)
        
        pos_mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "LOBBY"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_volver.collidepoint(event.pos):
                    return "LOBBY"
                if piso1.collidepoint(event.pos): 
                    return "COMBATE"

        #Fondo
        screen.blit(fondo, (0, 0))

        #Texto de titulo
        txt_titulo = fuentePTitulo.render("Mazmorra", True, (255, 255, 255))
        screen.blit(txt_titulo, (ANCHO // 2 - txt_titulo.get_width() // 2, 40))

        #piso 1 cuadrado (Dibujo)
        fondo_piso1 = pygame.image.load("Characters/Enemigos/slime.png")
        borde = pygame.draw.rect(screen, (BLACK), piso1, border_radius = 20)
        borde.inflate(20, 20)
        pygame.draw.rect(screen, (VerdeOscuro), borde, border_radius = 20)
        fondo_piso1 = pygame.transform.scale(fondo_piso1, (180, 140))
        screen.blit(pygame.transform.flip(fondo_piso1, True, False), (piso1.x + 50, piso1.y + 40))    
        txt_piso1 = fuente_titulo.render("Piso 1", True, (255, 255, 255))
        screen.blit(txt_piso1, (piso1.x + 110, piso1.y + 5))
        #hover
        if borde.collidepoint(pos_mouse):
            pygame.draw.rect(screen, (255, 255, 255), borde, 2, border_radius = 20)

        #piso 2 cuadrado
        piso2 = pygame.Rect(pisos_x + 350, pisos_y, 280, 210)
        borde = pygame.draw.rect(screen, (BLACK), piso2, border_radius = 20)
        borde.inflate(20, 20)
        pygame.draw.rect(screen, (GrisOscuro), borde, border_radius = 20)
        fondo_piso2 = pygame.image.load("UI/bloqueado.png")
        fondo_piso2 = pygame.transform.scale(fondo_piso2, (150, 150))
        screen.blit(pygame.transform.flip(fondo_piso2, True, False), (piso2.x + 65, piso2.y + 40))    
        txt_piso2 = fuente_titulo.render("Piso 2", True, (255, 255, 255))
        screen.blit(txt_piso2, (piso2.x + 110, piso2.y + 5))
        #hover
        if borde.collidepoint(pos_mouse):
            pygame.draw.rect(screen, (255, 255, 255), borde, 2, border_radius = 20)

        #piso 3 cuadrado
        piso3 = pygame.Rect(pisos_x + 700, pisos_y, 280, 210)
        borde = pygame.draw.rect(screen, (GrisOscuro), piso3, border_radius = 20)
        borde.inflate(20, 20)
        pygame.draw.rect(screen, (GrisOscuro), borde, border_radius = 20)
        fondo_piso3 = pygame.image.load("UI/bloqueado.png")
        fondo_piso3 = pygame.transform.scale(fondo_piso3, (150, 150))
        screen.blit(pygame.transform.flip(fondo_piso3, True, False), (piso3.x + 65, piso3.y + 40))    
        txt_piso3 = fuente_titulo.render("Piso 3", True, (255, 255, 255))
        screen.blit(txt_piso3, (piso3.x + 110, piso3.y + 5))
        #hover
        if borde.collidepoint(pos_mouse):
            pygame.draw.rect(screen, (255, 255, 255), borde, 2, border_radius = 20)

        #piso 4 cuadrado
        piso4 = pygame.Rect(pisos_x, pisos_y + 280, 280, 210)
        borde = pygame.draw.rect(screen, (GrisOscuro), piso4, border_radius = 20)
        borde.inflate(20, 20)
        pygame.draw.rect(screen, (GrisOscuro), borde, border_radius = 20)
        fondo_piso4 = pygame.image.load("UI/bloqueado.png")
        fondo_piso4 = pygame.transform.scale(fondo_piso4, (150, 150))
        screen.blit(pygame.transform.flip(fondo_piso4, True, False), (piso4.x + 65, piso4.y + 40))    
        txt_piso4 = fuente_titulo.render("Piso 4", True, (255, 255, 255))
        screen.blit(txt_piso4, (piso4.x + 110, piso4.y + 5))
        #hover
        if borde.collidepoint(pos_mouse):
            pygame.draw.rect(screen, (255, 255, 255), borde, 2, border_radius = 20)

        #piso 5 cuadrado
        piso5 = pygame.Rect(pisos_x + 350, pisos_y + 280, 280, 210)
        borde = pygame.draw.rect(screen, (GrisOscuro), piso5, border_radius = 20)
        borde.inflate(20, 20)
        pygame.draw.rect(screen, (GrisOscuro), borde, border_radius = 20)
        fondo_piso5 = pygame.image.load("UI/bloqueado.png")
        fondo_piso5 = pygame.transform.scale(fondo_piso5, (150, 150))
        screen.blit(pygame.transform.flip(fondo_piso5, True, False), (piso5.x + 65, piso5.y + 40))    
        txt_piso5 = fuente_titulo.render("Piso 5", True, (255, 255, 255))
        screen.blit(txt_piso5, (piso5.x + 110, piso5.y + 5))
        #hover
        if borde.collidepoint(pos_mouse):
            pygame.draw.rect(screen, (255, 255, 255), borde, 2, border_radius = 20)

        pygame.display.flip()
        reloj.tick(60)

def ejecutar(screen, reloj, personaje):
    ANCHO, ALTO = screen.get_size()
    nivel_mazmorra = personaje.nivel_mazmorra   #usa el nivel guardado del personaje

    #Fuentes
    fuente_titulo = pygame.font.SysFont("Georgia", 40, bold = True, italic = True)
    fuente_subtitulo = pygame.font.SysFont("Arial", 24)
    fuente_ayuda = pygame.font.SysFont("Verdana", 20, bold = True)
    fuente_dano = pygame.font.SysFont("Arial", 28, bold = True)

    #Spawn personaje
    imagen = pygame.image.load(f"Characters/Personajes/{personaje.clase}.png")
    personaje_img  = pygame.transform.scale(imagen, (120, 160))
    personaje_rect = personaje_img.get_rect()
    personaje_rect.center = (250, int(ALTO // 1.5))

    #Generar enemigo
    enemigo = generar_enemigo(nivel_mazmorra)
    img_raw = enemigos[enemigo["nombre"]]
    #convert_alpha() solo si tiene canal alpha(PNG), convert() para Surfaces de color
    if img_raw.get_flags() & pygame.SRCALPHA:
        imagen_enemigo = img_raw.convert_alpha()
    else:
        imagen_enemigo = img_raw.convert()

    enemigo_img = pygame.transform.scale(imagen_enemigo, (200, 200))
    enemigo_rect = enemigo_img.get_rect()
    enemigo_rect.center = (ANCHO - 300, int(ALTO // 1.5))

    #Movimiento personaje
    velocidad_salto_p = 2
    saltando_p = False

    #Plataformas
    pisos_p = {
        1: int(ALTO * 0.75),
        2: int(ALTO * 0.65),
        3: int(ALTO * 0.45),
        4: int(ALTO * 0.25),
        5: int(ALTO * 0.05),
    }
    plataformas = [
        pygame.Rect(50,  pisos_p[1] - 30, 300, 30),
        pygame.Rect(400, pisos_p[2] - 30, 300, 30),
        pygame.Rect(50,  pisos_p[3] - 30, 300, 30),
        pygame.Rect(400, pisos_p[4] - 30, 300, 30),
        pygame.Rect(50,  pisos_p[5] - 30, 300, 30),
    ]

    #Ataque del enemigo
    ataque_enemigo_cooldown = random.randint(500, 1500)
    ultimo_ataque_enemigo = pygame.time.get_ticks()
    proyectiles_enemigos = []
    velocidad_proyectil_enemigo = -10

    #cooldown de ataque del personaje
    ultimo_ataque_personaje = pygame.time.get_ticks()
    personaje.cooldown = 100
    personaje.cooldown_max = 500 

    #Daño por contacto con el slime
    ultimo_contacto_slime = 0
    cooldown_contacto = 600

    #Proyectiles del personaje
    proyectiles = []
    velocidad_proyectil = 15

    #Enemigos activos
    enemigos_activos = []

    #Colocar enemigo en el suelo
    enemigo_rect.bottom = int(ALTO // 1.2)
    enemigo_rect.x = ANCHO - 300

    enemigo["img"] = enemigo_img
    enemigo["rect"] = enemigo_rect

    #Movimiento del slime
    slime_vel_x = 2
    slime_vel_y = 0
    slime_saltando = False
    slime_suelo_y = int(ALTO // 1.5)
    slime_zona_min = ANCHO // 2
    slime_zona_max = ANCHO - 60
    ultimo_salto_slime = pygame.time.get_ticks()
    intervalo_salto_slime = random.randint(1200, 2500)

    #Flash rojo del slime al recibir daño
    slime_flash_timer = 0   #frames que queda el flash activo
    FLASH_DURACION = 8   #frames de parpadeo rojo

    #piso
    piso_actual = 1

    #Numeros flotantes de daño
    numeros_dano = []

    enemigos_activos.append(enemigo)

    fps = 60
    running = True
    proximo_estado = "LOBBY"

    #Agacharse
    agachado = False
    altura_normal = personaje_rect.height
    altura_agachado = int(altura_normal * 0.6)  #40% mas bajo


    boton_atacar = pygame.Rect(ANCHO // 2 - 75, ALTO - 80, 150, 50)

    #---------------------INICIO DEL BUCLE PRINCIPAL--------------------------------
    while running:
        click = False
        pos_mouse_tuple = pygame.mouse.get_pos()
        pos_mouse = pygame.Rect(pos_mouse_tuple[0], pos_mouse_tuple[1], 1, 1)

        #--------------------------------eventos-teclas----------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    proximo_estado = "LOBBY"
                    running = False
                if (event.key == pygame.K_UP or event.key == pygame.K_SPACE) and not saltando_p and not agachado:
                    velocidad_salto_p = -18
                    saltando_p = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
            #Agacharse
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    agachado = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    agachado = False


            #Ataque con click izquierdo
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if personaje.cooldown <= 0:
                    dano = personaje.atacar()
                    clase = personaje.clase.lower()
                    img   = ataques[clase][0]
                    proyectil_rect = img.get_rect()
                    proyectil_rect.center = personaje_rect.center
                    proyectiles.append({"img": img, "rect": proyectil_rect, "dano": dano})

                    personaje.cooldown = personaje.cooldown_max  # activar cooldown

        #Reduce el cooldown del personaje
        if personaje.cooldown > 0:
            personaje.cooldown -= reloj.get_time()

        #piso 1
        if piso_actual == 1:
            #---------------------------------Movimiento personaje---------------------
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: personaje_rect.x -= 6
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: personaje_rect.x += 6

            velocidad_salto_p += 1
            personaje_rect.y  += velocidad_salto_p
            suelo_y = int(ALTO // 1.45) - personaje_rect.height
            if personaje_rect.y >= suelo_y:
                personaje_rect.y = suelo_y
                velocidad_salto_p = 0
                saltando_p = False
            for plat in plataformas:
                if personaje_rect.colliderect(plat) and velocidad_salto_p > 0:
                    if personaje_rect.bottom <= plat.top:
                        personaje_rect.bottom = plat.top
                        velocidad_salto_p = 0
                        saltando_p = False
            if personaje_rect.left < 0: 
                personaje_rect.left = 0
            if personaje_rect.right > ANCHO: 
                personaje_rect.right = ANCHO

            #---------------------------------Movimiento slime-------------------------
            ahora_slime = pygame.time.get_ticks()
            if not slime_saltando and ahora_slime - ultimo_salto_slime > intervalo_salto_slime:
                slime_vel_y = -14
                slime_saltando = True
                ultimo_salto_slime = ahora_slime
                intervalo_salto_slime = random.randint(1200, 2500)

            slime_vel_y += 1
            enemigo["rect"].y += slime_vel_y
            if enemigo["rect"].bottom >= slime_suelo_y:
                enemigo["rect"].bottom = slime_suelo_y
                slime_vel_y   = 0
                slime_saltando = False

            #movimiento horizontal
            enemigo["rect"].x += slime_vel_x
            if enemigo["rect"].right >= slime_zona_max:
                enemigo["rect"].right = slime_zona_max
                slime_vel_x = -abs(slime_vel_x)
            if enemigo["rect"].left <= slime_zona_min:
                enemigo["rect"].left = slime_zona_min
                slime_vel_x = abs(slime_vel_x)

            #---------------------------------Daño por contacto------------------------
            ahora_contacto = pygame.time.get_ticks()
            if personaje_rect.colliderect(enemigo["rect"]):
                if ahora_contacto - ultimo_contacto_slime > cooldown_contacto:
                    dano_contacto         = enemigo["ataque"]
                    personaje.hp         -= dano_contacto
                    ultimo_contacto_slime = ahora_contacto
                    #Numero flotante rojo sobre el personaje
                    agregar_numero(numeros_dano,
                                personaje_rect.centerx, personaje_rect.top - 10,
                                dano_contacto, (255, 80, 80))
                    if personaje.hp <= 0:
                        return "GAMEOVER"

            #---------------------------------Background----------------------------------
            #Piso
            piso_y = int(ALTO)

            fondo_piso = pygame.image.load("Backgrounds/pisos/fondo_piso1.png")
            alto_fondo = fondo_piso.get_height()
            screen.blit(fondo_piso, (0, piso_y - alto_fondo))

            #Linea del suelo
            pygame.draw.line(screen, (136, 200, 50), (0, piso_y - 10), (ANCHO, piso_y), 2)
            #-------------------------------------------------------------------------
            #Piso
            piso_text = fuente_subtitulo.render(f"PISO: {nivel_mazmorra}", True, WHITE)
            screen.blit(piso_text, (ANCHO/2 - piso_text.get_width()/2, 20))

            #----------------------barra vida personaje----------------------
            bvw = 200
            bvh = 20
            bvx = 50
            bvy = 60
            barra_vida = pygame.Rect(bvx + 50, bvy, bvw, bvh)

            if personaje.hp_max > 0:
                porcentaje_hp = personaje.hp / personaje.hp_max
            else:
                porcentaje_hp = 0

            #Evitar que se pase del 100%
            porcentaje_hp = max(0, min(1, porcentaje_hp))

            pygame.draw.rect(screen, (200, 50, 50), (bvx+50, bvy, bvw, bvh))  
            pygame.draw.rect(screen, (50, 220, 80), (bvx+50, bvy, int(bvw * porcentaje_hp), bvh))
            pygame.draw.rect(screen, WHITE, barra_vida, 2)


            #----------------------barra mana personaje----------------------
            bmw = 200   #ancho de la barra de mana
            bmh = 20    #alto de la barra de mana
            bmx = 50    #posición X donde empieza la barra
            bmy = 90    #posición Y donde empieza la barra

            barra_mana = pygame.Rect(bmx + 50, bmy + 45, bmw, bmh)

            if personaje.mana_max > 0:
                porcentaje_mana = personaje.mana / personaje.mana_max
            else:
                porcentaje_mana = 0

            #Evita que se pase del 100%
            porcentaje_mana = max(0, min(1, porcentaje_mana))

            pygame.draw.rect(screen, (30, 30, 150), (bmx + 50, bmy + 45, bmw, bmh))
            pygame.draw.rect(screen, (80, 130, 255), (bmx + 50, bmy + 45, int(bmw * porcentaje_mana), bmh))
            pygame.draw.rect(screen, WHITE, barra_mana, 2)


            #----------------------barra vida enemigo----------------------
            bew = 200
            beh = 20
            bex = ANCHO - bew - 50
            bey = 60
            barra_enemigo_hp = pygame.Rect(bex - 50, bey, bew, beh)

            if enemigo["hp_max"] > 0:
                porcentaje_enemigo_hp = enemigo["salud"] / enemigo["hp_max"]
            else:
                porcentaje_enemigo_hp = 0

            #Evita que se pase del 100%
            porcentaje_enemigo_hp = max(0, min(1, porcentaje_enemigo_hp))

            pygame.draw.rect(screen, (200, 50, 50), (bex-50, bey, bew, beh))
            pygame.draw.rect(screen, (50, 220, 80), (bex-50, bey, int(bew * porcentaje_enemigo_hp), beh))
            pygame.draw.rect(screen, WHITE, barra_enemigo_hp, 2)

            #Textos HUD
            screen.blit(fuente_subtitulo.render(f"{personaje.hp}/{personaje.hp_max}", True, WHITE),(bvx + 50, bvy - 25))
            screen.blit(fuente_subtitulo.render(f"{personaje.mana}/{personaje.mana_max}", True, (150,200,255)), (bmx + 50, bmy + 20))
            screen.blit(fuente_subtitulo.render(f"{enemigo['salud']}/{enemigo['hp_max']}", True, WHITE), (bex - 50, bey - 25))
            screen.blit(fuente_subtitulo.render(personaje.clase, True, WHITE), (bvx + 50, bvy - 55))
            screen.blit(fuente_subtitulo.render(enemigo["nombre"], True, WHITE), (bex - 50, bey - 55))
            screen.blit(fuente_subtitulo.render(f"Nv.{personaje.nivel}", True, (255,230,80)),(bvx - 20, bvy))
            screen.blit(fuente_subtitulo.render(f"Nv.{enemigo['nivel']}", True, (255,230,80)),(bex - bew + 80, bey))
            
            if agachado:
                #Guarda posicion del suelo
                suelo = personaje_rect.bottom

                #Cambia altura del collider
                personaje_rect.height = altura_agachado
                personaje_rect.bottom = suelo

                #Imagen aplastada
                personaje_agachado = pygame.transform.scale(personaje_img, (120, altura_agachado))
                screen.blit(personaje_agachado, personaje_rect)

            else:
                #Restaura altura normal
                suelo = personaje_rect.bottom
                personaje_rect.height = altura_normal
                personaje_rect.bottom = suelo

                screen.blit(personaje_img, personaje_rect)



            #--------------------ENEMIGOS (con flash rojo) -----------------------------------------
            for e in enemigos_activos:
                if slime_flash_timer > 0:
                    #Crear copia roja de la imagen
                    flash_surf = e["img"].copy()
                    flash_surf.fill((255, 0, 0, 160), special_flags=pygame.BLEND_RGBA_MULT)
                    screen.blit(flash_surf, e["rect"])
                    slime_flash_timer -= 1
                else:
                    screen.blit(e["img"], e["rect"])
            #Colision entre proyectiles
            for p_jugador in proyectiles[:]:
                for p_slime in proyectiles_enemigos[:]:
                    if p_jugador["rect"].colliderect(p_slime["rect"]):
                        proyectiles.remove(p_jugador)
                        proyectiles_enemigos.remove(p_slime)
                        break

            #--------------------PROYECTILES DEL PERSONAJE ----------------------------------------
            for p in proyectiles[:]:
                p["rect"].x += velocidad_proyectil
                screen.blit(p["img"], p["rect"])

                for e in enemigos_activos:
                    if p["rect"].colliderect(e["rect"]):
                        e["salud"] -= p["dano"]
                        if p in proyectiles:
                            proyectiles.remove(p)
                        #Numero flotante amarillo sobre el enemigo
                        agregar_numero(numeros_dano,
                                    e["rect"].centerx, e["rect"].top - 10,
                                    p["dano"], (255, 230, 50))
                        #Activar flash rojo
                        slime_flash_timer = FLASH_DURACION

                        #Murio
                        if e["salud"] <= 0:
                            mostrar_victoria(screen, reloj, personaje, e)
                            GuardarPartida.guardar_partida(personaje)  #guarda progreso tras victoria
                            return "LOBBY"

                if p["rect"].x > ANCHO:
                    if p in proyectiles:
                        proyectiles.remove(p)

            #--------------------ATAQUE AUTOMATICO ENEMIGO---------------------------------------
            ahora = pygame.time.get_ticks()
            if ahora - ultimo_ataque_enemigo > ataque_enemigo_cooldown:
                ataque_enemigo_cooldown = random.randrange(500, 3001, 500)
                ultimo_ataque_enemigo = ahora
                img  = ataques_enemigos["slime"][0]
                rect = img.get_rect()
                rect.center = enemigo["rect"].center
                proyectiles_enemigos.append({"img": img, "rect": rect, "dano": enemigo["ataque"]})

            for p in proyectiles_enemigos[:]:
                p["rect"].x += velocidad_proyectil_enemigo
                screen.blit(p["img"], p["rect"])
                if p["rect"].colliderect(personaje_rect):
                    personaje.hp -= p["dano"]
                    proyectiles_enemigos.remove(p)

                    #Numero flotante rojo sobre el personaje
                    agregar_numero(numeros_dano,
                                personaje_rect.centerx, personaje_rect.top - 10,
                                p["dano"], (255, 80, 80))
                    if personaje.hp <= 0:
                        return "GAMEOVER"
                elif p["rect"].x < 0:
                    proyectiles_enemigos.remove(p)

        #--------------------NUMEROS FLOTANTES ----------------------------------------
        actualizar_numeros(numeros_dano, screen, fuente_dano)

        pygame.display.flip()
        reloj.tick(fps)

    return proximo_estado