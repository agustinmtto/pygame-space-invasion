import random
import pygame
import math

# Inicializar a Pygame
pygame.init()


# Crear la pantalla con un tamaño de 800x600
pantalla = pygame.display.set_mode((800, 600))


# Música y sonidos
pygame.mixer.music.load("musicaFondo.mp3")  # Cargar música de fondo
pygame.mixer.music.play(-1)  # Reproducir en bucle infinito
sonido_impacto = pygame.mixer.Sound("Impacto.mp3")  # Cargar sonido de impacto
sonido_laser = pygame.mixer.Sound("Laser.mp3")

# Titulo e Icono
pygame.display.set_caption(("Invacion Espacial")) # Definimos el titulo
icono = pygame.image.load("ovni.png") # Guardamos la imagen en una variable
pygame.display.set_icon(icono) # Establecemos como icono
fondo = pygame.image.load("fondo.jpg")


# VARIABLES DE JUGADOR
img_jugador = pygame.image.load("nave.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# PUNTAJE
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10


# texto final de juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)


def texto_final():
    mi_fuente_final = fuente_final.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (60, 200))

def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto,(x,y))

# FUNCIOJ JUGADOR
def spawn_jugador(x, y):
    pantalla.blit(img_jugador, (x, y)) # spawn del jugador en la pantalla


# VARIABLES ENEMIGO
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8


for enemigo in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(4)
    enemigo_y_cambio.append(40)



# FUNCION ENEMIGO
def spawn_enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y)) # spawn del enemigo en la pantalla


# VARIABLES BALA
img_bala= pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 10
bala_visible = False


# FUNCION BALA
def spawn_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10)) # spawn de la bala desde la nave

# COLISIONES --------------------------------------------------------------------------
def detectar_colision(x1, y1, x2, y2):
    distancia = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego -------------------------------------------------------------------------------------
se_ejecuta = True
while se_ejecuta:
    pantalla.blit(fondo, (0, 0))  # Fondo

    # Iterar Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT: # Evento para cerrar
            se_ejecuta = False
        if evento.type == pygame.KEYDOWN:  # Al Presionar una tecla cambiar desplazamiento en x (+ o -)
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -8
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 8
            if evento.key == pygame.K_SPACE: # Al presionar espacio y la bala no esta en la pantalla
                if not bala_visible:
                    bala_x = jugador_x # Definimos ubicacion de la bala desde el jugador
                    spawn_bala(bala_x, bala_y) # Spawn de la bala en la poscion (x = jugador; y = 50)
                    sonido_laser.play()  # Reproducir sonido de impacto

        if evento.type == pygame.KEYUP:  # Al soltar una flecha definir desplazamiento en x = 0
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # JUGADOR --------------------------------------------------------------------------

    # Modificar ubicacion jugador con los desplazamientos actualizados
    jugador_x += jugador_x_cambio

    # Mantener dentro de bordes al jugador validando los limites de los desplazamientos
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # ENEMIGO --------------------------------------------------------------------------

    # Modificar ubicacion enemigo con los desplazamientos actualizados
    for enemigo in range(cantidad_enemigos):
        # Fin del juego
        if enemigo_y[enemigo] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[enemigo] += enemigo_x_cambio[enemigo]

    # Mantener dentro de bordes al enemigo

        if enemigo_x[enemigo] <= 0:
            enemigo_x_cambio[enemigo] = 3
            enemigo_y[enemigo] += enemigo_y_cambio[enemigo]
        elif enemigo_x[enemigo] >= 736:
            enemigo_x_cambio[enemigo] = -3
            enemigo_y[enemigo] += enemigo_y_cambio[enemigo]

    # COLISION -----------------------------------------------------------------------

        colision = detectar_colision(enemigo_x[enemigo], enemigo_y[enemigo], bala_x, bala_y)
        if colision:
            sonido_impacto.play()  # Reproducir sonido de impacto
            bala_visible = False
            bala_x = jugador_x  # Restablecer bala
            bala_y = 500
            puntaje += 1
            enemigo_x[enemigo] = random.randint(0, 736)  # Reaparecer enemigo
            enemigo_y[enemigo] = random.randint(50, 200)
        spawn_enemigo(enemigo_x[enemigo], enemigo_y[enemigo], enemigo)
    # BALA --------------------------------------------------------------------------

    # Movimiento Bala
    if bala_y <= -64: # Cuando la bala se va de la pantalla (-64), ponerla en la ubicacion del jugador y ocultarla (False)
        bala_y = 500
        bala_visible = False

    if bala_visible:   # Si la bala esta visible realizar spawn con el desplazamiento actualizado
        spawn_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio


    # APARECER ENTIDADES ------------------------------------------------------------------
    spawn_jugador(jugador_x, jugador_y)
    spawn_enemigo(enemigo_x[enemigo], enemigo_y[enemigo], enemigo)
    mostrar_puntaje(texto_x, texto_y)
    pygame.display.update() # Se actualiza para mostrar el color de fondo
    pygame.time.Clock().tick(60)  # Limitar el bucle a 60 FPS