# Validación: Reproducir y controlar la explicación

**Funcionalidad**: 006-reproducir-traza

## Entorno

- Linux, Python 3.14.8 en `.venv` del proyecto.
- pytest 8.4.2 y pytest-cov 7.0.0 de `requirements-dev.txt`.

## Fase de fallo

```bash
pytest tests/test_visualizador.py -q
```

Resultado: 10 pruebas fallan porque no existe el módulo `visualizador`.

## Fase de éxito y cobertura

```bash
pytest --cov=visualizador --cov=juego --cov=dado --cov=fantasma_ia --cov=laberinto --cov-report=term-missing --cov-fail-under=80
```

Resultado: 277 pruebas pasan. Cobertura de `visualizador.py`: 100 %.

## Relación de pruebas y criterios

| Criterio | Prueba | Estado |
|---|---|---|
| CA-21 / RF-01 | `test_pila_visible_en_el_tiempo` | Aprobado |
| CA-22 | `test_saltar_llega_al_final` | Aprobado |
| RF-02 | `test_marcas_del_tablero` | Aprobado |
| RF-03 | `test_pausa_y_paso`, `test_pasos_al_terminar_no_hacen_nada`, `test_velocidad_entre_limites` | Aprobado |
| RF-04 | `saltar()` sin animación, misma prueba de CA-22 | Aprobado |
| RF-05 | `test_limpiar_borra_marcas` | Aprobado |
| RF-06 | `test_espera_sin_traza` | Aprobado |
| Duración A | `test_intervalo_de_la_spec` | Aprobado |
| Caso límite origen = destino | `test_traza_de_origen_igual_destino` | Aprobado |
| Pila de 225 | La traza serpiente de 004 cubre la pila; el reproductor solo copia `evento.pila` | Aprobado por diseño |
| Teclas P, N, S, + y - | Las conecta `main.py` | Pendiente de 008 |
