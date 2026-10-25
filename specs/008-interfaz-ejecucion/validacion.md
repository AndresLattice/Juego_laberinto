# Validación: Iniciar, controlar y reiniciar el juego

**Funcionalidad**: 008-interfaz-ejecucion

## Entorno

- Linux (CachyOS), Intel Core i7-12700H, Python 3.14.8.
- pygame 2.6.1 compilado con SDL2_ttf 2.24.0.
- Pruebas sin ventana con `SDL_VIDEODRIVER=dummy`. Los scripts de simulación no forman parte del repositorio.

## Capturas

| Captura | Qué muestra |
|---|---|
| [captura_inicio.png](captura_inicio.png) | Menú con visualizador activado |
| [captura_partida.png](captura_partida.png) | Búsqueda del fantasma con HUD y bloque cayendo al tarro |
| [captura_fin.png](captura_fin.png) | Pantalla de GAME OVER |

## Resultados

| Comprobación | Resultado | Estado |
|---|---|---|
| CA-16 | Semilla 42 jugada a 60 y a 30 FPS: mismos dados, misma aparición y mismo final | Aprobado |
| Partidas completas | 20 partidas con teclas al azar terminan sin errores | Aprobado |
| Victoria por teclado | El jugador entra a la meta con las flechas y aparece ¡HAS GANADO! | Aprobado |
| R tras ganar | Turno 1, sin fantasma, mismo mapa | Aprobado |
| M y ESC | En partida y en pantallas finales vuelven al menú; ESC en el menú sale | Aprobado |
| `--semilla 123` | Se lee 123; sin el argumento la semilla es aleatoria | Aprobado |
| Visualizador apagado | 30 partidas terminan sin animar la búsqueda | Aprobado |
| RF-08 60 FPS | 1,58 ms por cuadro dibujado | Aprobado en Linux; macOS y Windows no probados |
| RF-01 tecla G | Fuera del alcance reducido de un mapa | No aplica |
| RF-02 aviso de catálogo | Fuera del alcance reducido de un mapa | No aplica |
| Prueba jugando en ventana real | Pendiente de revisión manual | Pendiente |

## Observación de dificultad

En el laberinto 1 hay 98 pasos de la entrada a la meta. Un jugador que sigue el camino más corto
perdió las 30 partidas simuladas. Esto viene de las reglas de la spec, no de un error del código.

## Pruebas de lógica

`pytest`: 277 pruebas pasan. Ningún módulo de lógica importa pygame.
