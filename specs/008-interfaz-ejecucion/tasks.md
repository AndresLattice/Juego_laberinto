# Tareas: Iniciar, controlar y reiniciar el juego

**Funcionalidad**: 008-interfaz-ejecucion | **Fecha**: 2026-10-23
**Entrada**: [spec.md](spec.md)

## Alcance reducido

- Un solo mapa: el laberinto 1 de `base/laberintos.json`. No hay tecla G ni modo generado (002).
- ESC tras ganar o perder vuelve al menú.
- R reinicia con el mismo mapa.

## Diseño

`main.py` tiene la clase `Aplicacion` y el bucle de pygame.

| Parte | Qué hace |
|---|---|
| `manejar_tecla(tecla)` | Aplica §10.4 según la pantalla y el estado; ignora las demás teclas |
| `actualizar(segundos)` | Anima dados, espera 1 s de aparición, reproduce la traza y mueve al fantasma cada 0,25 s |
| `mensaje_estado()` | Texto del HUD |
| `dibujar_inicio`, `dibujar_partida` | Menú, juego, HUD y pantallas finales |
| `leer_semilla(argumentos)` | Lee `--semilla N` de la línea de comandos |

`dibujo.texto` guarda una fuente por tamaño, porque crearla en cada cuadro bajaba de 60 FPS.

## Tareas

- [X] T001 Crear `main.py` con menú, partida, HUD y pantallas finales.
- [X] T002 Conectar teclas de juego y del visualizador.
- [X] T003 Leer `--semilla` y compartir un solo `random.Random` con la partida.
- [X] T004 Simular partidas sin ventana y revisar capturas.
- [X] T005 Medir el tiempo por cuadro.
- [X] T006 Registrar resultados en `validacion.md` y cerrar pendientes de 003, 005, 006 y 007.
