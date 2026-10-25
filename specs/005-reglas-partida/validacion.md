# Validación: Jugar turnos y resolver persecución

**Funcionalidad**: 005-reglas-partida

## Entorno

- Linux, Python 3.14.8 en `.venv` del proyecto.
- pytest 8.4.2 y pytest-cov 7.0.0 de `requirements-dev.txt`.

## Fase de fallo

```bash
pytest tests/test_juego.py -q
```

Resultado: 17 pruebas fallan con `ModuleNotFoundError: No module named 'juego'`.
Las 250 pruebas anteriores siguen pasando.

## Relación de pruebas y criterios

| Criterio | Prueba | Estado |
|---|---|---|
| RF-01 | `test_inicio_de_partida`, `test_tirar_da_pasos_y_permite_mover`, `test_no_se_tira_dos_veces` | Aprobado |
| CA-07 | `test_pared_no_mueve_ni_gasta` | Aprobado |
| CA-08 | `test_sin_pasos_no_se_mueve` | Aprobado |
| RF-02 | `test_paso_valido_descuenta` | Aprobado |
| CA-09 | `test_fantasma_aparece_al_terminar_el_primer_turno` | Aprobado |
| CA-10 / RF-03 | `test_diez_mil_apariciones` | Aprobado |
| CA-11 / RF-05 | `test_captura_en_el_tercer_paso` | Aprobado |
| CA-12 / RF-07 | `test_avanza_cuatro_sin_captura` | Aprobado |
| CA-13 / RF-06 | `test_victoria_con_pasos_de_sobra` | Aprobado |
| CA-14 | `test_jugador_entra_al_fantasma` | Aprobado |
| CA-15 | `test_enter_antes_de_tirar_no_hace_nada`, `test_enter_tras_dos_de_cinco_pasa_al_fantasma` | Aprobado |
| Fin por pasos | `test_pasos_en_cero_terminan_el_turno` | Aprobado |
| CA-24 / RF-08 | `test_reiniciar` | Aprobado |
| RF-04 | `test_acciones_fuera_de_estado` | Aprobado |
| RF-03 mensaje 1 s, RF-05 0,25 s, RF-09 | `main.py`, comprobado en partidas simuladas (ver 008) | Aprobado |

## Fase de éxito y cobertura

```bash
pytest --cov=juego --cov=dado --cov=fantasma_ia --cov=laberinto --cov-report=term-missing --cov-fail-under=80
```

Resultado: 267 pruebas pasan. Cobertura de `juego.py`: 100 %.
