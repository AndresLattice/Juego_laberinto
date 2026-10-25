"""El Laberinto del Fantasma: menú, bucle principal y teclado."""

import random
import sys
from pathlib import Path

import pygame

from config import *
import dibujo
from juego import Partida
from laberinto import cargar_catalogo
from visualizador import ReproductorTraza

RUTA_LABERINTOS = Path(__file__).resolve().parent / "base" / "laberintos.json"
APARICION = 1.0
PASO_FANTASMA = 0.25

FLECHAS = {
    pygame.K_UP: "arriba",
    pygame.K_RIGHT: "derecha",
    pygame.K_DOWN: "abajo",
    pygame.K_LEFT: "izquierda",
}


class Aplicacion:
    def __init__(self, semilla):
        self.azar = random.Random(semilla)
        resultado = cargar_catalogo(RUTA_LABERINTOS)
        self.laberinto = resultado.entradas[0].laberinto
        self.partida = Partida(self.laberinto, self.azar)
        self.reproductor = ReproductorTraza()
        self.pantalla_actual = "INICIO"
        self.visualizador = True
        self.espera = 0
        self.tiempo_fin = 0
        self.mirada = (0, 1)
        self.salir = False

    def comenzar(self):
        self.partida.reiniciar(self.laberinto)
        self.reproductor.limpiar()
        self.pantalla_actual = "PARTIDA"
        self.espera = 0
        self.mirada = (0, 1)

    def manejar_tecla(self, tecla):
        if self.pantalla_actual == "INICIO":
            if tecla == pygame.K_ESCAPE:
                self.salir = True
            elif tecla == pygame.K_v:
                self.visualizador = not self.visualizador
            elif tecla == pygame.K_RETURN:
                self.comenzar()
            return

        partida = self.partida
        if tecla == pygame.K_ESCAPE:
            self.pantalla_actual = "INICIO"
        elif partida.estado in ("VICTORIA", "DERROTA"):
            if tecla == pygame.K_r:
                self.comenzar()
            elif tecla == pygame.K_m:
                self.pantalla_actual = "INICIO"
        elif partida.estado == "JUGADOR_TIRAR":
            if tecla == pygame.K_SPACE:
                partida.tirar()
                self.reproductor.limpiar()
        elif partida.estado == "JUGADOR_MOVER":
            # Mientras gira el dado no se puede mover.
            if partida.dado_jugador.animando:
                return
            if tecla in FLECHAS:
                partida.mover(FLECHAS[tecla])
            elif tecla == pygame.K_RETURN:
                partida.terminar_turno()
            if partida.estado == "FANTASMA_TIRAR" and partida.aparecio:
                self.espera = APARICION
        elif self.buscando():
            if tecla == pygame.K_p:
                self.reproductor.pausar()
            elif tecla == pygame.K_n:
                self.reproductor.paso()
            elif tecla == pygame.K_s:
                self.reproductor.saltar()
            elif tecla in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                self.reproductor.mas_rapido()
            elif tecla in (pygame.K_MINUS, pygame.K_KP_MINUS):
                self.reproductor.mas_lento()

    def buscando(self):
        return (self.partida.estado == "FANTASMA_MOVER"
                and not self.partida.dado_fantasma.animando
                and not self.reproductor.terminado)

    def actualizar(self, segundos):
        if self.pantalla_actual != "PARTIDA":
            return
        partida = self.partida
        partida.dado_jugador.actualizar(segundos)
        partida.dado_fantasma.actualizar(segundos)
        if self.reproductor.terminado:
            self.tiempo_fin += segundos

        if partida.estado == "FANTASMA_TIRAR":
            # Primero se muestra el aviso de aparición durante 1 s.
            if self.espera > 0:
                self.espera -= segundos
                return
            traza = partida.tirar_fantasma()
            self.reproductor.cargar(traza)
            self.tiempo_fin = 0
            if not self.visualizador:
                self.reproductor.saltar()
            self.espera = PASO_FANTASMA
        elif partida.estado == "FANTASMA_MOVER":
            if partida.dado_fantasma.animando:
                return
            if not self.reproductor.terminado:
                self.reproductor.actualizar(segundos)
                return
            self.espera -= segundos
            if self.espera <= 0:
                antes = partida.fantasma
                partida.paso_fantasma()
                self.mirada = (partida.fantasma[0] - antes[0], partida.fantasma[1] - antes[1])
                self.espera = PASO_FANTASMA

    def mensaje_estado(self):
        partida = self.partida
        if partida.estado == "JUGADOR_TIRAR":
            return "Tu turno: pulsa ESPACIO para tirar"
        if partida.estado == "JUGADOR_MOVER":
            if partida.dado_jugador.animando:
                return "Tirando el dado..."
            return "Mueve con las flechas: quedan " + str(partida.pasos) + " pasos · ENTER para terminar"
        if partida.estado == "FANTASMA_TIRAR" and self.espera > 0:
            return "¡Apareció el fantasma!"
        if partida.dado_fantasma.animando:
            return "El fantasma tira el dado..."
        if self.buscando():
            return "El fantasma busca tu rastro...  (P pausa · N paso · S saltar · +/- velocidad)"
        return "El fantasma avanza..."


def dibujar_inicio(pantalla, app):
    pantalla.fill(BLANCO)
    estado = "ACTIVADO"
    if not app.visualizador:
        estado = "DESACTIVADO"
    dibujo.texto(pantalla, "El Laberinto del Fantasma", ANCHO // 2, 200, 64, FANTASMA, True)
    dibujo.texto(pantalla, "Laberinto: predefinido 1 (backtracking)", ANCHO // 2, 330, 30, NEGRO, True)
    dibujo.texto(pantalla, "V: visualizador de backtracking [" + estado + "]", ANCHO // 2, 380, 30, NEGRO, True)
    dibujo.texto(pantalla, "ENTER para comenzar", ANCHO // 2, 460, 36, NEGRO, True)
    dibujo.texto(pantalla, "ESC para salir", ANCHO // 2, 510, 26, GRIS, True)


def dibujar_partida(pantalla, app):
    partida = app.partida
    pantalla.fill(BLANCO)
    dibujo.dibujar_tablero(pantalla, partida.laberinto, app.reproductor)
    dibujo.dibujar_jugador(pantalla, partida.jugador)
    if partida.fantasma is not None:
        if partida.estado == "FANTASMA_TIRAR" and app.espera > 0:
            # Destello en la casilla donde aparece.
            x, y = dibujo.esquina(partida.fantasma)
            pygame.draw.rect(pantalla, ENCONTRADO, (x, y, TAM_CELDA, TAM_CELDA))
        dibujo.dibujar_fantasma(pantalla, partida.fantasma, app.mirada)
    dibujo.dibujar_panel(pantalla, app.reproductor, app.tiempo_fin)

    # HUD
    pygame.draw.line(pantalla, NEGRO, (0, 640), (ANCHO, 640), 2)
    dibujo.texto(pantalla, "Turno: " + str(partida.turno), 20, 680, 30)
    dibujo.dibujar_dado(pantalla, 150, 665, partida.dado_jugador.cara, "Jugador")
    dibujo.dibujar_dado(pantalla, 240, 665, partida.dado_fantasma.cara, "Fantasma")
    if partida.estado not in ("VICTORIA", "DERROTA"):
        dibujo.texto(pantalla, app.mensaje_estado(), 330, 685, 22)
        return

    capa = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    capa.fill((0, 0, 0, 160))
    pantalla.blit(capa, (0, 0))
    if partida.estado == "VICTORIA":
        dibujo.texto(pantalla, "¡HAS GANADO!", ANCHO // 2, 280, 64, (60, 200, 60), True)
        subtitulo = "Llegaste a la meta en " + str(partida.turno) + " turnos"
    else:
        dibujo.texto(pantalla, "GAME OVER", ANCHO // 2, 280, 64, (220, 40, 40), True)
        subtitulo = "El fantasma te atrapó"
    dibujo.texto(pantalla, subtitulo, ANCHO // 2, 350, 30, BLANCO, True)
    dibujo.texto(pantalla, "R: jugar de nuevo · M: menú · ESC: menú", ANCHO // 2, 400, 26, BLANCO, True)


def leer_semilla(argumentos):
    if "--semilla" in argumentos:
        posicion = argumentos.index("--semilla")
        if posicion + 1 < len(argumentos):
            return int(argumentos[posicion + 1])
    return None


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("El Laberinto del Fantasma")
    reloj = pygame.time.Clock()
    app = Aplicacion(leer_semilla(sys.argv))

    while not app.salir:
        segundos = reloj.tick(FPS) / 1000
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                app.salir = True
            elif evento.type == pygame.KEYDOWN:
                app.manejar_tecla(evento.key)
        app.actualizar(segundos)
        if app.pantalla_actual == "INICIO":
            dibujar_inicio(pantalla, app)
        else:
            dibujar_partida(pantalla, app)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
