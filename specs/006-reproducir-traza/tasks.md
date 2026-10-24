# Tareas: Reproducir y controlar la explicación

**Funcionalidad**: 006-reproducir-traza | **Fecha**: 2026-10-23
**Entrada**: [spec.md](spec.md)

## Decisión de duración

Se eligió la opción A: cada evento dura `max(0.03, 4 / eventos)` segundos, como dice §8.4.
Con trazas largas la búsqueda dura más de 4 s. La tecla S permite saltarla.

## Diseño

Una clase `ReproductorTraza` en `visualizador.py`, sin pygame.

| Miembro | Qué hace |
|---|---|
| `cargar(traza)` | Empieza una reproducción nueva y calcula el intervalo |
| `actualizar(segundos)` | Consume los eventos que tocan según el tiempo y la velocidad |
| `pausar()` | Pausa o reanuda (P) |
| `paso()` | Con pausa, consume un evento (N) |
| `saltar()` | Llega al estado final (S); también se usa con el visualizador apagado |
| `mas_rapido()`, `mas_lento()` | Velocidad entre ×0,25 y ×4 (+ y -) |
| `limpiar()` | Borra marcas y vuelve a "esperando" al tirar el jugador |
| `estado_casilla(c)` | `"en_pila"`, `"descartada"` o `None` |
| `pila_visible`, `evento_actual`, `camino` | Datos para el tarro y el tablero |
| `apilados`, `retrocesos`, `profundidad`, `maximo` | Contadores |
| `esperando`, `terminado` | Estado de la reproducción |

## Fase 1: Pruebas (deben fallar)

- [X] T001 Crear `tests/test_visualizador.py` con espera sin traza (RF-06) e intervalo de la spec.
- [X] T002 Prueba CA-21: pila y contadores en un instante dado.
- [X] T003 Prueba RF-02: marcas en pila y descartadas.
- [X] T004 Prueba CA-22: `saltar()` deja el estado final.
- [X] T005 Pruebas RF-03: pausa, paso, pasos al terminar y límites de velocidad.
- [X] T006 Prueba RF-05: `limpiar()` borra las marcas.
- [X] T007 Prueba de traza con origen igual a destino.
- [X] T008 Ejecutar y registrar el fallo en `validacion.md`.

## Fase 2: Implementación

- [X] T009 Crear `visualizador.py` con `ReproductorTraza`.
- [X] T010 Ejecutar todas las pruebas y medir cobertura de `visualizador`.
- [X] T011 Completar `validacion.md` y actualizar el estado de `spec.md`.
