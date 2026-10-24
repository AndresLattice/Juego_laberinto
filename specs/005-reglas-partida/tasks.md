# Tareas: Jugar turnos y resolver persecución

**Funcionalidad**: 005-reglas-partida | **Fecha**: 2026-10-23
**Entrada**: [spec.md](spec.md)

## Diseño

Una clase `Partida` en `juego.py`, sin pygame y sin reloj.
Las esperas de 0,6 s, 1 s y 0,25 s las maneja `main.py` en 008.
La lógica solo cambia de estado cuando recibe una orden.

| Método | Estado en que funciona | Qué hace |
|---|---|---|
| `tirar()` | `JUGADOR_TIRAR` | Tira el dado del jugador y pasa a `JUGADOR_MOVER` |
| `mover(direccion)` | `JUGADOR_MOVER` | Avanza si no hay pared y quedan pasos; revisa meta y captura |
| `terminar_turno()` | `JUGADOR_MOVER` | Hace aparecer al fantasma en el turno 1 y pasa a `FANTASMA_TIRAR` |
| `aparecer_fantasma()` | Lo usa `terminar_turno` | Elige una casilla a 6 pasos o más, que no sea la meta |
| `tirar_fantasma()` | `FANTASMA_TIRAR` | Tira el dado, busca el camino y devuelve la traza |
| `paso_fantasma()` | `FANTASMA_MOVER` | Avanza una casilla y revisa la captura |
| `reiniciar(laberinto)` | Cualquiera | Vuelve al inicio con otro tablero |

Las direcciones son `"arriba"`, `"derecha"`, `"abajo"` e `"izquierda"`.
`aparecio` queda en `True` el turno en que sale el fantasma, para mostrar el mensaje.
Los estados `INICIO`, `DADO_*` y `APARECE_FANTASMA` de §11 son de la interfaz y van en 008.

## Fase 1: Pruebas (deben fallar)

- [X] T001 Crear `tests/test_juego.py` con el inicio de partida (RF-01).
- [X] T002 Pruebas de tirar, mover, pared y pasos (CA-07, CA-08, RF-02).
- [X] T003 Pruebas de ENTER antes y después de tirar (CA-15).
- [X] T004 Pruebas de aparición del fantasma (CA-09, CA-10, RF-03).
- [X] T005 Pruebas de persecución y captura (CA-11, CA-12, RF-05, RF-07).
- [X] T006 Pruebas de victoria y derrota del jugador (CA-13, CA-14, RF-06).
- [X] T007 Prueba de reinicio (CA-24, RF-08) y de acciones fuera de estado (RF-04).
- [X] T008 Ejecutar y registrar el fallo en `validacion.md`.

## Fase 2: Implementación

- [ ] T009 Crear `juego.py` con la clase `Partida`.
- [ ] T010 Ejecutar todas las pruebas y medir cobertura de `juego`.
- [ ] T011 Completar `validacion.md` y actualizar el estado de `spec.md`.
