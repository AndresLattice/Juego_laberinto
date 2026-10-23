# Evidencia de implementación: 001

**Fecha**: 2026-10-17. **Entorno**: Linux, Python 3.12.14, .venv sin pygame instalado.
**Herramientas reales**: coverage 7.16.2, pytest 8.4.2, pytest-cov 7.0.0. `pip check`: sin dependencias rotas.

El usuario autorizó continuar con el checklist personalizado pendiente (28 elementos).
Se mantienen sus marcas originales y las del checklist básico (16 aprobadas).
No se declara terminado el juego. CA-27 literal se aprobó al integrar 004.

## Integridad de datos y alcance

base/laberintos.json permanece idéntico al original; SHA-256:
`b88940659028289cbcd3d7bd56112ccd880100e21ba90f5be5bc7f0034dea084`.
Ningún archivo de base/ se modificó. Solo se implementan modelo, carga, paredes, vecinos
y distancias. No se añadieron actores, generación, ventanas ni dependencias de ejecución.

## Evidencia del ciclo de pruebas primero

Comando de cada etapa: `.venv/bin/python -m pytest tests/test_laberinto.py -q`;
algunas fases de fallo usaron --tb=no/--tb=short para abreviar la salida.
Los estados siguientes corresponden al estado del código en cada etapa, no a fallos actuales.

| Etapa | Estado de salida | Resultado observado |
|---|---|---|
| T005-rojo | 1 | 14 failed in 0.12s |
| T006-verde | 0 | 14 passed in 0.10s |
| T007-rojo | 1 | 3 failed, 15 passed in 0.13s |
| T008-verde | 0 | 18 passed in 0.18s |
| T009-rojo | 1 | 120 failed, 18 passed in 2.56s |
| T010-verde | 0 | 138 passed in 0.43s |
| T011-rojo | 1 | 3 failed, 138 passed in 0.36s |
| T012-verde | 0 | 141 passed in 0.27s |
| T013-rojo | 1 | 21 failed, 141 passed in 0.35s |
| T014-verde | 0 | 162 passed in 0.47s |
| T016-rojo | 1 | 33 failed, 162 passed in 0.64s |
| T017-verde | 0 | 195 passed in 0.68s |
| T018-rojo | 1 | 16 failed, 195 passed in 0.76s |
| T019-verificacion | 1 | 1 failed, 210 passed in 0.52s |
| T019-verde | 0 | 211 passed in 0.66s |
| T020-garantia | 0 | 212 passed in 0.53s |
| T023-rojo | 1 | 20 failed, 212 passed in 0.85s |
| T024-verde | 0 | 232 passed in 1.45s |
| T025-garantia | 0 | 233 passed in 1.62s |
| T028-cobertura | 0 | 233 passed in 5.03s |

Las fases rojas identificaron capacidades ausentes: módulo inicial, validación de grafos,
contorno, metadatos, cargador, paredes, vecinos y distancias. Cada implementación se escribió
después del fallo correspondiente y se verificó con las pruebas acumuladas.
T020/T021 y T025/T026 añadieron garantías de independencia que ya cumplía el diseño;
se registró el éxito sin añadir código innecesario ni simular fallos.

En T019 hubo una expectativa incorrecta de prueba para la entrada del laberinto 1.
Se contrastaron directamente grid[1][2] (espacio) y grid[2][1] (#), se conservaron esas
aserciones en la prueba y se corrigió la expectativa a [(1,0)]. No se alteró la lógica ni
los datos para obtener un resultado artificial.

## Resultado final de pruebas y cobertura

```text
.venv/bin/python -m pytest tests/test_laberinto.py --cov=laberinto --cov-report=term-missing --cov-fail-under=80 -q
233 passed in 5.03s
laberinto.py: 107 sentencias, 0 sin ejecutar, 100 % de cobertura de líneas.
Estado de salida: 0. Sin pruebas omitidas ni fallidas en la ejecución final.
```

Es el único módulo de lógica implementado, por lo que la medición acredita su umbral
individual, sin exclusiones de líneas ni dependencias de interfaz. La importación se comprueba
también con python -S (biblioteca estándar sin paquetes del entorno).

## Matriz de aceptación

| Referencia | Evidencia | Estado |
|---|---|---|
| RF-01, RF-02 / CE-01 / CA-01 | Cinco tableros, normalización, metadatos preservados y lectura sin escritura | Aprobado |
| RF-03 / CE-02 | Formato, centros, ciclos, desconexión aun con 224 conexiones y 120 alteraciones individuales del contorno | Aprobado |
| RF-04, RF-05 / CE-02 | Carga mixta ordenada, catálogo vacío, errores JSON/UTF-8 y OSError simulado, sin ocultar RuntimeError | Aprobado |
| RF-06, RF-07 / CE-03 / CA-02 | Vecinos y paredes de las 1 125 casillas, simetría y expectativa literal de entrada | Aprobado |
| RF-08 / CE-04 | Tipos, forma, rango, pares no adyacentes y ausencia de mutación tras rechazo en las tres consultas | Aprobado |
| RF-09 / CE-05 | 225 destinos para 225 orígenes de cada uno de los cinco tableros; referencia independiente con pila | Aprobado |
| RF-10 / CE-06 | Mutación de copias no cambia fuente, modelo, metadatos ni resultados previos | Aprobado |
| CA-27: distancias independientes | Comparación con oráculo y serpiente de 224 pasos; total de 253 125 pares de referencia | Aprobado en aislamiento |
| CA-27 literal con buscar_camino | `test_distancias_coinciden_con_camino` en tests/test_fantasma_ia.py | Aprobado al integrar 004 |

## Restricciones verificadas y limitaciones

- Biblioteca estándar únicamente en laberinto.py. Pruebas ejecutadas sin pygame y sin ventana.
- Dependencias de pruebas separadas en requirements-dev.txt; no se requieren para usar el módulo.
- Sintaxis del módulo comprobada con ast.parse(feature_version=(3,10)). La suite completa se
  ejecutó en Python 3.12.14; no se afirma ejecución bajo 3.10, Windows ni macOS.
- Código propio, mensajes y documentación en español; nombres externos de Python y grid
  conservados por compatibilidad. Implementación plana de un módulo, sin capas adicionales.
- Guía quickstart recorrida para preparación y pruebas de 001. Sus comandos futuros de
  main.py siguen señalados como no disponibles hasta la funcionalidad 008.
- Hooks de implementación: no existe .specify/extensions.yml.
- El checklist de revisión pendiente impide presentar la aceptación global
  como completa; la implementación y validación aislada de esta entrega están acreditadas.
