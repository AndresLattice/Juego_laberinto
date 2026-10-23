# Validación: Encontrar caminos y explicar el backtracking

**Funcionalidad**: 004-busqueda-con-traza

## Entorno

- Python 3.12, pytest 8.4.2, Linux.

## Fase de fallo (T011)

Comando:

```bash
pytest tests/test_fantasma_ia.py -q
```

Resultado: 10 pruebas fallan con `ModuleNotFoundError: No module named 'fantasma_ia'`.
El fallo se debe a la capacidad ausente, no a un error de instalación.
Las 233 pruebas de 001 siguen pasando.

## Relación de pruebas y criterios

| Criterio | Prueba | Estado |
|---|---|---|
| CA-03 | `test_camino_valido` | Pendiente de implementación |
| CA-04 / RF-04 | `test_origen_igual_destino` | Pendiente de implementación |
| CA-05 | `test_existe_camino_en_los_cinco` | Pendiente de implementación |
| CA-17 | `test_inicio_y_fin_de_traza` | Pendiente de implementación |
| CA-18 | `test_cuenta_de_apilar_y_desapilar` | Pendiente de implementación |
| CA-19 | `test_desapila_solo_la_cima_sin_salidas` | Pendiente de implementación |
| CA-20 | `test_traza_determinista` | Pendiente de implementación |
| RF-02 | `test_origen_igual_destino`, `test_desapila_solo_la_cima_sin_salidas` | Pendiente de implementación |
| RF-06 | `test_destino_inalcanzable` | Pendiente de implementación |
| RF-07 | `test_pila_maxima_en_tablero_serpiente` | Pendiente de implementación |
| CA-27 literal | `test_distancias_coinciden_con_camino` | Pendiente de implementación |

## Fase de éxito y cobertura

No ejecutada todavía.

## Rendimiento (RNF-4)

No medido todavía.
