# Validación: Encontrar caminos y explicar el backtracking

**Funcionalidad**: 004-busqueda-con-traza

## Entorno

- Linux, Python 3.14.8 en `.venv` del proyecto.
- pytest 8.4.2 y pytest-cov 7.0.0 de `requirements-dev.txt`.

## Fase de fallo (T011)

Comando:

```bash
pytest tests/test_fantasma_ia.py -q
```

Resultado: 10 pruebas fallan con `ModuleNotFoundError: No module named 'fantasma_ia'`.
El fallo se debe a la capacidad ausente, no a un error de instalación.
Las 233 pruebas de 001 siguen pasando.

## Fase de éxito y cobertura (T013, T014)

Comando:

```bash
pytest --cov=fantasma_ia --cov=laberinto --cov-report=term-missing --cov-fail-under=80
```

Resultado: 243 pruebas pasan. Cobertura de `fantasma_ia.py`: 100 %. Cobertura de `laberinto.py`: 100 %.

## Rendimiento (T015, RNF-4)

Se midió `buscar_camino_con_traza` de `(0,0)` a `(14,14)` 50 veces en cada laberinto.
El peor tiempo fue 1,29 ms, por debajo del límite de 10 ms.

## Relación de pruebas y criterios

| Criterio | Prueba | Estado |
|---|---|---|
| CA-03 | `test_camino_valido` | Aprobado |
| CA-04 / RF-04 | `test_origen_igual_destino` | Aprobado |
| CA-05 | `test_existe_camino_en_los_cinco` | Aprobado |
| CA-17 / RF-03 | `test_inicio_y_fin_de_traza` | Aprobado |
| CA-18 / RF-05 | `test_cuenta_de_apilar_y_desapilar` | Aprobado |
| CA-19 / RF-05 | `test_desapila_solo_la_cima_sin_salidas` | Aprobado |
| CA-20 | `test_traza_determinista` | Aprobado |
| RF-01 | Orden de `vecinos_accesibles` y `test_traza_determinista` | Aprobado |
| RF-02 | `test_origen_igual_destino`, `test_desapila_solo_la_cima_sin_salidas` | Aprobado |
| RF-06 | `test_destino_inalcanzable` | Aprobado |
| RF-07 | `test_pila_maxima_en_tablero_serpiente` | Aprobado |
| CA-27 literal | `test_distancias_coinciden_con_camino` | Aprobado |

El recálculo en cada turno de RF-07 lo hará la spec 005, que llama a `buscar_camino`.
