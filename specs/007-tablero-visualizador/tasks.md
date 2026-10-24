# Tareas: Ver tablero, actores y pila sincronizada

**Funcionalidad**: 007-tablero-visualizador | **Fecha**: 2026-10-23
**Entrada**: [spec.md](spec.md)

## Diseño

- `config.py`: tamaños y colores de §4.1, §4.2 y §8.2.
- `dibujo.py`: funciones que solo pintan lo que reciben. Es el único módulo, con `main.py`, que importa pygame.

| Función | Qué dibuja |
|---|---|
| `dibujar_tablero(pantalla, laberinto, reproductor)` | Entrada, meta, marcas de búsqueda y paredes |
| `dibujar_jugador(pantalla, casilla)` | Círculo azul con ojos |
| `dibujar_fantasma(pantalla, casilla, mirada)` | Cuerpo morado con tres picos y ojos hacia `mirada` |
| `dibujar_dado(pantalla, x, y, cara, etiqueta)` | Dado de 60 × 60 con puntos |
| `dibujar_panel(pantalla, reproductor, tiempo_fin)` | Tarro, bloques, cima, contadores y mensaje |

Las animaciones de 0,12 s usan `reproductor.tiempo`, que es el tiempo desde el último evento.
El parpadeo de "encontrado" usa `tiempo_fin`, los segundos desde que terminó la búsqueda.
La base de la pila usa la etiqueta "inicio", porque la fuente por defecto no tiene emoji (RF-06).

## Requisito del sistema

Con Python 3.14, pygame 2.6.1 se compila desde el código fuente.
Si falta la librería `SDL2_ttf`, pygame queda sin módulo de fuentes.
En Arch o CachyOS se instala con `sudo pacman -S sdl2_ttf sdl2_image sdl2_mixer`.

## Tareas

- [X] T001 Crear `config.py` con las constantes.
- [X] T002 Crear `dibujo.py` con tablero, actores, dados y panel.
- [X] T003 Generar capturas con datos de prueba sin abrir ventana.
- [X] T004 Revisar las capturas y registrar el resultado en `validacion.md`.
- [X] T005 Comprobar que los módulos de lógica siguen sin importar pygame.
