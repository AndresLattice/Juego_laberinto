"""Dibujo con pygame del tablero, los personajes, el tarro y los dados."""

import pygame

from config import *


def esquina(casilla):
    columna, fila = casilla
    return MARGEN + columna * TAM_CELDA, MARGEN + fila * TAM_CELDA


def centro(casilla):
    x, y = esquina(casilla)
    return x + TAM_CELDA // 2, y + TAM_CELDA // 2


fuentes = {}


def texto(pantalla, mensaje, x, y, tamano=22, color=NEGRO, centrado=False):
    # Crear una fuente es lento, así que se guarda la de cada tamaño.
    if tamano not in fuentes:
        fuentes[tamano] = pygame.font.Font(None, tamano)
    fuente = fuentes[tamano]
    imagen = fuente.render(mensaje, True, color)
    if centrado:
        x = x - imagen.get_width() // 2
    pantalla.blit(imagen, (x, y))


def dibujar_tablero(pantalla, laberinto, reproductor):
    pygame.draw.rect(pantalla, ENTRADA, (*esquina((0, 0)), TAM_CELDA, TAM_CELDA))
    pygame.draw.rect(pantalla, META, (*esquina((14, 14)), TAM_CELDA, TAM_CELDA))

    # Marcas de la búsqueda, debajo de las paredes.
    camino = reproductor.camino
    for fila in range(N):
        for columna in range(N):
            casilla = (columna, fila)
            estado = reproductor.estado_casilla(casilla)
            color = None
            if casilla in camino:
                color = ENCONTRADO
            elif estado == "en_pila":
                color = EN_PILA
            elif estado == "descartada":
                color = DESCARTADA
            if color is not None:
                pygame.draw.rect(pantalla, color, (*esquina(casilla), TAM_CELDA, TAM_CELDA))
    if len(reproductor.pila_visible) > 0 and not reproductor.terminado:
        cima = reproductor.pila_visible[-1]
        pygame.draw.rect(pantalla, CIMA, (*esquina(cima), TAM_CELDA, TAM_CELDA), 3)
    x, y = centro((14, 14))
    texto(pantalla, "META", x, y - 7, 20, NEGRO, True)

    # En el grid, las filas pares son paredes horizontales y las columnas pares verticales.
    grid = laberinto.grid
    for f in range(31):
        for c in range(31):
            if grid[f][c] != "#":
                continue
            x = MARGEN + (c // 2) * TAM_CELDA
            y = MARGEN + (f // 2) * TAM_CELDA
            if f % 2 == 0 and c % 2 == 1:
                pygame.draw.line(pantalla, NEGRO, (x, y), (x + TAM_CELDA, y), GROSOR_PARED)
            elif f % 2 == 1 and c % 2 == 0:
                pygame.draw.line(pantalla, NEGRO, (x, y), (x, y + TAM_CELDA), GROSOR_PARED)


def dibujar_jugador(pantalla, casilla):
    x, y = centro(casilla)
    pygame.draw.circle(pantalla, JUGADOR, (x, y), 14)
    for dx in (-5, 5):
        pygame.draw.circle(pantalla, BLANCO, (x + dx, y - 3), 3)
        pygame.draw.circle(pantalla, NEGRO, (x + dx, y - 3), 1)


def dibujar_fantasma(pantalla, casilla, mirada):
    x, y = centro(casilla)
    izquierda = x - 15
    arriba = y - 16
    pygame.draw.circle(pantalla, FANTASMA, (x, arriba + 15), 15)
    pygame.draw.rect(pantalla, FANTASMA, (izquierda, arriba + 15, 30, 12))
    # Tres picos en la base.
    for i in range(3):
        base = izquierda + i * 10
        puntos = [(base, arriba + 27), (base + 10, arriba + 27), (base + 5, arriba + 32)]
        pygame.draw.polygon(pantalla, FANTASMA, puntos)
    dx, dy = mirada
    for ojo in (-6, 6):
        pygame.draw.circle(pantalla, BLANCO, (x + ojo, y - 4), 4)
        pygame.draw.circle(pantalla, NEGRO, (x + ojo + dx * 2, y - 4 + dy * 2), 2)


def dibujar_dado(pantalla, x, y, cara, etiqueta):
    texto(pantalla, etiqueta, x + 30, y - 18, 20, NEGRO, True)
    pygame.draw.rect(pantalla, BLANCO, (x, y, 60, 60))
    pygame.draw.rect(pantalla, NEGRO, (x, y, 60, 60), 3)
    if cara is None:
        return
    puntos = {
        1: [(30, 30)],
        2: [(15, 15), (45, 45)],
        3: [(15, 15), (30, 30), (45, 45)],
        4: [(15, 15), (45, 15), (15, 45), (45, 45)],
        5: [(15, 15), (45, 15), (30, 30), (15, 45), (45, 45)],
        6: [(15, 15), (45, 15), (15, 30), (45, 30), (15, 45), (45, 45)],
    }
    for px, py in puntos[cara]:
        pygame.draw.circle(pantalla, NEGRO, (x + px, y + py), 5)


def dibujar_bloque(pantalla, x, y, mensaje, relleno, borde, grosor):
    pygame.draw.rect(pantalla, relleno, (x, y, 140, 20))
    pygame.draw.rect(pantalla, borde, (x, y, 140, 20), grosor)
    texto(pantalla, mensaje, x + 70, y + 3, 20, NEGRO, True)


def dibujar_panel(pantalla, reproductor, tiempo_fin):
    panel_x = 640
    medio = panel_x + ANCHO_PANEL_PILA // 2
    texto(pantalla, "Pila del backtracking", medio, 20, 24, NEGRO, True)

    # Tarro: lados, fondo redondeado y boca más ancha.
    tarro_x = medio - 80
    pygame.draw.rect(pantalla, TARRO, (tarro_x, 60, 160, 460), 3,
                     border_bottom_left_radius=16, border_bottom_right_radius=16)
    pygame.draw.line(pantalla, BLANCO, (tarro_x + 3, 60), (tarro_x + 157, 60), 3)
    pygame.draw.line(pantalla, TARRO, (medio - 90, 60), (tarro_x + 3, 60), 3)
    pygame.draw.line(pantalla, TARRO, (tarro_x + 157, 60), (medio + 90, 60), 3)

    pila = reproductor.pila_visible
    bloque_x = medio - 70
    fondo = 520 - 10 - 20

    if reproductor.esperando:
        texto(pantalla, "Esperando al fantasma...", medio, 560, 22, NEGRO, True)
        return

    # Con más de 20 casillas se dibujan las 19 de arriba y un resumen.
    visibles = list(pila)
    sobran = 0
    if len(visibles) > 20:
        sobran = len(visibles) - 19
        visibles = visibles[-19:]
        dibujar_bloque(pantalla, bloque_x, fondo, "... +" + str(sobran) + " más", BLANCO, GRIS, 1)

    parpadeo = reproductor.terminado and tiempo_fin < 0.8 and int(tiempo_fin / 0.2) % 2 == 1
    # La animación no puede durar más que el tiempo entre eventos.
    duracion = min(ANIMACION_BLOQUE, reproductor.intervalo)
    progreso = min(1, reproductor.tiempo / duracion)
    if reproductor.pausado:
        progreso = 1
    evento = reproductor.evento_actual
    for i in range(len(visibles)):
        posicion = i
        if sobran > 0:
            posicion = i + 1
        y = fondo - posicion * 22
        casilla = visibles[i]
        mensaje = "(" + str(casilla[0]) + "," + str(casilla[1]) + ")"
        if sobran == 0 and i == 0:
            mensaje = mensaje + " inicio"
        relleno = EN_PILA
        if reproductor.terminado and not parpadeo:
            relleno = ENCONTRADO
        es_cima = i == len(visibles) - 1
        if es_cima and evento.tipo == "apilar" and not reproductor.terminado:
            # El bloque nuevo cae desde la boca del tarro.
            y = int(40 + (y - 40) * progreso)
        if es_cima:
            dibujar_bloque(pantalla, bloque_x, y, mensaje, relleno, CIMA, 3)
            texto(pantalla, "<- cima", bloque_x + 152, y + 3, 20)
        else:
            dibujar_bloque(pantalla, bloque_x, y, mensaje, relleno, NEGRO, 1)

    if evento is not None and evento.tipo == "desapilar" and progreso < 1:
        # El bloque que sale sube y se desvanece.
        bloques = len(visibles)
        if sobran > 0:
            bloques = bloques + 1
        y = fondo - bloques * 22 - int(60 * progreso)
        capa = pygame.Surface((140, 20), pygame.SRCALPHA)
        capa.fill((*ROJO_CLARO, int(255 * (1 - progreso))))
        pantalla.blit(capa, (bloque_x, y))

    texto(pantalla, "Apilados: " + str(reproductor.apilados), panel_x + 10, 530, 20)
    texto(pantalla, "Desapilados (retrocesos): " + str(reproductor.retrocesos), panel_x + 10, 550, 20)
    texto(pantalla, "Profundidad actual: " + str(reproductor.profundidad), panel_x + 10, 570, 20)
    texto(pantalla, "Máxima: " + str(reproductor.maximo), panel_x + 190, 570, 20)
    texto(pantalla, mensaje_evento(reproductor), panel_x + 10, 600, 20)


def mensaje_evento(reproductor):
    evento = reproductor.evento_actual
    if evento is None:
        return ""
    casilla = "(" + str(evento.casilla[0]) + "," + str(evento.casilla[1]) + ")"
    if evento.tipo == "apilar":
        return "Apilar " + casilla + ": avanzo a un vecino libre"
    if evento.tipo == "desapilar":
        return "Desapilar " + casilla + ": callejón sin salida"
    return "¡Encontrado! Camino de " + str(len(reproductor.camino)) + " pasos"
