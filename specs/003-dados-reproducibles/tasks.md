# Tareas: Tirar dados y reproducir partidas

**Funcionalidad**: 003-dados-reproducibles | **Fecha**: 2026-10-23
**Entrada**: [spec.md](spec.md)

## Diseño

Una clase `Dado` en `dado.py`, sin pygame.

- `Dado(azar_logico, azar_visual=None)`: recibe el `random.Random` de la partida.
  Si no se pasa un generador visual, crea uno aparte sin semilla.
- `tirar()`: saca el valor del azar lógico y empieza la animación.
- `actualizar(segundos)`: cambia `cara` con el azar visual cada 0,06 s y la fija en `valor` a los 0,6 s.
- Cada actor tiene su propio `Dado`. Todos comparten el mismo azar lógico.

La semilla `--semilla` la lee `main.py` en 008 y crea `random.Random(semilla)`.

## Fase 1: Pruebas (deben fallar)

- [X] T001 Crear `tests/test_dado.py` con CA-06: 10 000 tiradas en 1..6 y aparecen las 6 caras.
- [X] T002 Prueba RF-02: cada actor conserva su última tirada.
- [X] T003 Prueba RF-05: la misma semilla da la misma secuencia.
- [X] T004 Prueba RF-03: la cara cambia a los 0,06 s y se fija en el valor a los 0,6 s.
- [X] T005 Prueba RF-04: la animación no consume el azar lógico.
- [X] T006 Prueba de escenario 2: cuadros de distinto tamaño dan las mismas tiradas.
- [X] T007 Ejecutar y registrar el fallo en `validacion.md`.

## Fase 2: Implementación

- [X] T008 Crear `dado.py` con la clase `Dado`.
- [X] T009 Ejecutar todas las pruebas y medir cobertura de `dado`.
- [X] T010 Completar `validacion.md` y actualizar el estado de `spec.md`.
