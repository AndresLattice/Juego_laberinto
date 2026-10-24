# Validación: Tirar dados y reproducir partidas

**Funcionalidad**: 003-dados-reproducibles

## Entorno

- Linux, Python 3.14.8 en `.venv` del proyecto.
- pytest 8.4.2 y pytest-cov 7.0.0 de `requirements-dev.txt`.

## Fase de fallo

```bash
pytest tests/test_dado.py -q
```

Resultado: 7 pruebas fallan con `ModuleNotFoundError: No module named 'dado'`.

## Fase de éxito y cobertura

```bash
pytest --cov=dado --cov=fantasma_ia --cov=laberinto --cov-report=term-missing --cov-fail-under=80
```

Resultado: 250 pruebas pasan. Cobertura de `dado.py`: 100 %.

## Relación de pruebas y criterios

| Criterio | Prueba | Estado |
|---|---|---|
| CA-06 / RF-01 | `test_diez_mil_tiradas` | Aprobado |
| RF-02 | `test_cada_actor_guarda_su_tirada` | Aprobado |
| RF-03 | `test_animacion_cambia_cada_006_y_fija_el_valor` | Aprobado |
| RF-04 | `test_animacion_no_consume_azar_logico` | Aprobado |
| RF-05 | `test_misma_semilla_misma_secuencia` | Aprobado |
| Escenario 2 | `test_cuadros_distintos_misma_partida` | Aprobado |
| CA-16 integrado | Requiere 005 y 008 | Pendiente de integración |

RF-01 pide igual probabilidad. Se usa `randint(1, 6)` como fija D-1; la prueba solo comprueba rango y caras.
