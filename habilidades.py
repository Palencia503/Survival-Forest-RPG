import pygame

#-------------------ATAQUES PERSONAJES------------------
a_mago = [
    "Ataques/Personajes/Mago/bola_fuego.png",
    "Ataques/Personajes/Mago/ataque_baston.png"
]

a_tanque = [
    "Ataques/Personajes/Tanque/ataque_escudo.png"
]

a_guerrero = [
    "Ataques/Personajes/Guerrero/corte.png"
]

a_tirador = [
    "Ataques/Personajes/Tirador/flecha.png",
    "Ataques/Personajes/Tirador/ataque_arco.png"
]

a_asesino = [
    "Ataques/Personajes/Asesino/corteAsesino.png"
]

#diccionario de ataques
ataques = {
    "mago": a_mago,
    "tanque": a_tanque,
    "guerrero": a_guerrero,
    "tirador": a_tirador,
    "asesino": a_asesino
}

#Cargar y escalar correctamente
for clase in ataques:
    for i in range(len(ataques[clase])):
        img = pygame.image.load(ataques[clase][i])
        ataques[clase][i] = pygame.transform.scale(img, (80, 80))


#-------------------ATAQUES ENEMIGOS----------------------
slime_ataque = [
    "Ataques/Enemigos/slime/ataque_slime.png"
]

ataques_enemigos = {
    "slime": slime_ataque
}

for enemigo in ataques_enemigos:
    for i in range(len(ataques_enemigos[enemigo])):
        img = pygame.image.load(ataques_enemigos[enemigo][i])
        ataques_enemigos[enemigo][i] = pygame.transform.scale(img, (80, 80))

