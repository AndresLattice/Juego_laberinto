# Validación: Ver tablero, actores y pila sincronizada

**Funcionalidad**: 007-tablero-visualizador

## Entorno

- Linux, Python 3.14.8 en `.venv` del proyecto.
- pygame 2.6.1 compilado con SDL2_ttf 2.24.0.

## Revisión visual

Se dibujó el laberinto 1 con una búsqueda de `(7,7)` a `(2,3)` de 283 eventos.
Las capturas se generaron con `SDL_VIDEODRIVER=dummy` y `pygame.image.save`.

| Captura | Momento |
|---|---|
| [captura_busqueda.png](captura_busqueda.png) | Mitad de la traza, justo después de un desapilar |
| [captura_encontrado.png](captura_encontrado.png) | Traza terminada |

| Criterio | Resultado | Estado |
|---|---|---|
| CA-23 ventana | La captura mide 920 × 740 px | Aprobado |
| CA-23 paredes | Líneas de 4 px | Aprobado |
| CA-23 tarro | 19 bloques y `... +K más` con pilas de 43 y 110 | Aprobado |
| RF-02 colores y capas | Entrada azul, META verde, marcas debajo de paredes y actores | Aprobado |
| RF-03 personajes | Jugador azul con ojos; fantasma morado con tres picos | Aprobado |
| RF-04 tarro | Título, cima con borde y flecha, base "inicio", contadores y mensaje | Aprobado |
| RF-05 animaciones | Cuadro intermedio de caída revisado en `captura_partida.png` de 008; la caída dura como máximo un intervalo | Aprobado en captura; falta verlo jugando |
| RF-06 primitivas | Solo `pygame.draw` y la fuente por defecto | Aprobado |
| RF-07 solo representa | `dibujo.py` no busca caminos ni cambia reglas | Aprobado |

## Pruebas de lógica

`pytest`: 277 pruebas pasan. Ningún módulo de lógica importa pygame.
