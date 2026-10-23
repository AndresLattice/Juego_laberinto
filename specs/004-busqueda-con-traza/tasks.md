# Tareas: Encontrar caminos y explicar el backtracking

**Funcionalidad**: 004-busqueda-con-traza | **Fecha**: 2026-10-23
**Entrada**: [spec.md](spec.md), [plan.md](plan.md)

Cada prueba se ejecuta primero y debe fallar. Después se escribe el código mínimo.

## Fase 1: Pruebas (deben fallar)

- [ ] T001 Crear `tests/test_fantasma_ia.py` con prueba de CA-04: `buscar_camino(a, a) == []` y traza apilar/encontrado.
- [ ] T002 Prueba CA-03: cada par consecutivo del camino es vecino sin pared, empieza junto al origen y termina en el destino.
- [ ] T003 Prueba CA-05: existe camino de `(0,0)` a `(14,14)` en los 5 laberintos.
- [ ] T004 Prueba CA-17: la traza empieza con `apilar(origen)`, termina con `encontrado(destino)` y la última pila sin el origen es el camino.
- [ ] T005 Prueba CA-18: `#apilar - #desapilar == len(camino) + 1` y nunca se desapila con pila vacía.
- [ ] T006 Prueba CA-19: cada `desapilar(c)` ocurre con `c` en la cima y sin vecinos accesibles sin visitar.
- [ ] T007 Prueba CA-20: dos ejecuciones iguales dan la misma traza.
- [ ] T008 Prueba RF-06: destino inalcanzable lanza `ValueError` usando un doble con `vecinos_accesibles`.
- [ ] T009 Prueba RF-07: la pila nunca supera 225 casillas.
- [ ] T010 Prueba CA-27 literal: `distancias_desde(c)[x] == len(buscar_camino(c, x))` para todas las casillas.
- [ ] T011 Ejecutar `pytest tests/test_fantasma_ia.py` y registrar el fallo en `validacion.md`.

## Fase 2: Implementación

- [ ] T012 Crear `fantasma_ia.py` con `Evento`, `buscar_camino_con_traza` y `buscar_camino` según el plan.
- [ ] T013 Ejecutar todas las pruebas y comprobar que pasan.
- [ ] T014 Medir cobertura con `pytest --cov=fantasma_ia --cov-report=term-missing --cov-fail-under=80`.
- [ ] T015 Medir el tiempo de una búsqueda 15×15 y registrarlo frente a los 10 ms de RNF-4.

## Fase 3: Cierre

- [ ] T016 Completar `validacion.md` con comandos, resultados y relación con cada CA.
- [ ] T017 Actualizar el estado de `spec.md` de 004 y la nota de CA-27 en 001.
