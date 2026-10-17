# Tareas: Consultar y validar laberintos

**Funcionalidad**: 001-modelo-laberintos. **Fecha**: 2026-10-17.
**Entrada**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md),
[data-model.md](data-model.md), [contrato](contracts/laberinto.md) y [quickstart.md](quickstart.md).
**Gobierno**: [constitución](../../.specify/memory/constitution.md).
**Estado**: tareas generadas; ninguna tarea de implementación ejecutada en esta fase.

## Formato y reglas de ejecución

Cada tarea usa `- [ ] TNNN [P opcional] [USn si corresponde] descripción con ruta`.
Las rutas de código son relativas a la raíz del checkout; las rutas documentales se muestran
completas desde esa raíz. [P] solo indica archivos distintos sin dependencia mutua pendiente.
No implica autorización para delegar trabajo ni para iniciar fases nuevas.

Las pruebas son obligatorias por la constitución. En cada pareja prueba/implementación:
primero observar y registrar un fallo por la capacidad ausente, después implementar y obtener
éxito, y finalmente refactorizar manteniendo las pruebas en verde. Un error de instalación
no acredita la fase de fallo. No escribir métodos futuros anticipadamente para evitar ese ciclo.

Antes de implementar, el responsable debe revisar
[checklists/modelo-laberintos.md](checklists/modelo-laberintos.md), cuyos 28 elementos siguen
pendientes. Su revisión no se autoriza por generar tareas y sus marcas no se alteran aquí.
El ciclo de implementación consultará su estado y resolverá ese requisito previo con el revisor.
[checklists/requirements.md](checklists/requirements.md) conserva su ciclo separado.

## Fase 1: Preparación compartida

**Objetivo**: herramientas de desarrollo aisladas, sin pygame para validar 001.

- [ ] T001 [P] Declarar versiones de pytest y pytest-cov compatibles con Python 3.10+ en requirements-dev.txt, instalar en .venv y registrar las versiones realmente usadas en specs/001-modelo-laberintos/validacion.md; no añadir dependencias de ejecución del juego.
- [ ] T002 [P] Crear o ampliar .gitignore conservando contenido previo, para excluir .venv/, __pycache__/, .pytest_cache/, .coverage y htmlcov/; no ignorar fuentes, pruebas, datos base ni evidencias documentales.

## Fase 2: Fundamentos de validación

**Objetivo**: datos y evidencias independientes del código que se probará.
**Dependencia**: fase 1 completa; todavía no implementar laberinto.py.

- [ ] T003 Preparar en tests/conftest.py fixtures que lean base/laberintos.json mediante ruta relativa al archivo de pruebas, copien datos para variaciones y escriban catálogos en tmp_path; preservar la fuente sin importar código de producción para construir valores esperados.
- [ ] T004 Crear specs/001-modelo-laberintos/validacion.md con entorno, estado inicial del catálogo y huella del archivo, matriz RF/CE/CA y espacios para comandos, fallos esperados y resultados reales; distinguir pendiente, aprobado y no ejecutado sin marcar aceptación anticipada.

**Punto de control**: se pueden escribir pruebas de las historias; no existen actores,
ventana, generación ni una implementación de la búsqueda 004 en estos fundamentos.

## Fase 3: US1 — Disponer de tableros confiables (P1, MVP)

**Objetivo**: cargar y conservar entradas válidas, rechazando tableros inválidos sin cerrar.
**Prueba independiente**: catálogo de cinco entradas, catálogos temporales inválidos/mixtos,
construcción de tableros y copias de metadatos; sin partida ni pantalla.

### Pruebas e implementación, en parejas sucesivas

- [ ] T005 [US1] Escribir en tests/test_laberinto.py pruebas de construcción/normalización de lista de filas a tupla, rechazo de tipos y dimensiones incorrectas, caracteres ajenos a «Solo # y espacio» y «Centros transitables»; incluir importación de la lógica sin pygame disponible, observar los fallos y registrarlos en specs/001-modelo-laberintos/validacion.md antes de T006 (RF-01, RF-03).
- [ ] T006 [US1] Crear Laberinto en laberinto.py como valor inmutable con «grid: tupla de 31 cadenas de longitud 31; copia del tablero recibido»; implementar solo normalización, dimensiones, caracteres y centros que exige T005, usando biblioteca estándar y mensajes españoles.
- [ ] T007 [US1] Añadir en tests/test_laberinto.py casos de ciclo, desconexión, conteo distinto de 224 y un tablero desconectado que conserve 224 conexiones; observar fallo antes de T008 para exigir separadamente «Exactamente 224 conexiones internas y 225 casillas conectadas. Sin ciclo ni desconexión.» (RF-03, CE-02).
- [ ] T008 [US1] Implementar en laberinto.py validación de conexiones contadas una vez y recorrido de conectividad, con auxiliares privados mínimos; no adelantar la API pública de US2 ni distancias de US3. Hacer pasar T007 sin ocultar fallos inesperados.
- [ ] T009 [US1] Añadir en tests/test_laberinto.py pruebas parametrizadas que cierren cada apertura obligatoria y abran individualmente cualquier otra posición del contorno, incluidas esquinas, sobre interior válido; observar fallo antes de T010 (aclaración aprobada, RF-03, CE-02).
- [ ] T010 [US1] Completar en laberinto.py la validación «Contorno abierto solo en (fila=1,columna=0) y (fila=29,columna=30). Los demás puntos del contorno son #, incluidas esquinas.»; exigir espacio en ambas aperturas y ValueError español para cualquier incumplimiento.
- [ ] T011 [US1] Añadir en tests/test_laberinto.py pruebas de EntradaCatalogo, copia profunda de datos, conservación de campos presentes sin inventar ausentes ni deduplicar identidades, preservación de entrada/salida como coordenadas del grid, e independencia frente a mutaciones de origen o copias entregadas; observar fallo antes de T012 (RF-02, RF-10).
- [ ] T012 [US1] Implementar EntradaCatalogo en laberinto.py con Laberinto validado y metadatos preservados según el contrato; la propiedad «datos devuelve una copia profunda nueva, incluido el grid original como lista», sin añadir validaciones descriptivas ajenas a la fuente.
- [ ] T013 [US1] Añadir en tests/test_laberinto.py pruebas de cargar_catalogo con las cinco entradas, mezcla válida/inválida, lista vacía, cero válidas, registro no diccionario, grid ausente, estructura superior distinta de lista, archivo inexistente, JSON/UTF-8 inválido y OSError simulado; comprobar orden, rechazadas y aviso del modelo. Observar fallo antes de T014 (RF-02 a RF-05, CE-01, CE-02, CA-01).
- [ ] T014 [US1] Implementar cargar_catalogo y ResultadoCarga en laberinto.py: «entradas: tupla de EntradaCatalogo, en el orden original de las aceptadas», «rechazadas: cantidad de entradas individuales inválidas; cero si no se pudo leer la lista», «aviso: texto español o None; indica catálogo no utilizable cuando entradas está vacía»; controlar solo errores esperados, sin sys.exit, respaldos o escritura de archivos.
- [ ] T015 [US1] Ejecutar las pruebas de US1 de tests/test_laberinto.py, revisar ausencia de importaciones gráficas directas/indirectas y registrar resultados y conservación de base/laberintos.json en specs/001-modelo-laberintos/validacion.md; refactorizar laberinto.py únicamente con pruebas en verde.

**Punto de control**: MVP de lectura y validación sin interfaz. No representa un juego completo.

## Fase 4: US2 — Consultar pasos permitidos (P1)

**Objetivo**: consultas de pared y vecinos con límites y simetría.
**Prueba independiente**: construir tableros válidos directamente y contrastar conexiones
contra el grid, sin depender del cargador, los dados o actores. La ejecución sigue a US1
porque comparte el mismo archivo y la construcción ya validada.

- [ ] T016 [US2] Añadir en tests/test_laberinto.py pruebas de coordenadas y pares inválidos: «Tupla (columna, fila) de dos enteros, excluyendo booleanos, cada uno entre 0 y 14», tipo/forma incorrectos, negativos, 15 o más, igualdad, diagonal y separación mayor que uno para hay_pared; incluir pruebas de pares adyacentes válidos con pared (True) y paso abierto (False), contrastados directamente con el grid. Para cada consulta inválida, comparar antes y después el grid, metadatos y resultados anteriores y exigir que permanezcan iguales. Observar y registrar los fallos de argumentos inválidos y paredes válidas antes de T017 (RF-06, RF-08, RF-10, CE-03, CE-04).
- [ ] T017 [US2] Añadir en laberinto.py validación de argumentos y la interfaz hay_pared, interpretando el separador grid[fA+fB+1][cA+cB+1]; rechazar coordenadas y pares inválidos con ValueError español antes de indexar; implementar únicamente las consultas válidas e inválidas de paredes probadas primero en T016, sin añadir vecinos ni distancias.
- [ ] T018 [US2] Añadir en tests/test_laberinto.py pruebas de vecinos_accesibles, orden arriba/derecha/abajo/izquierda, simetría de paredes, aperturas que no crean vecinos exteriores y comparación directa con el grid de las 1 125 casillas; incluir expectativa explícita de vecinos de (0,0) del laberinto 1 y rechazo de coordenadas inválidas por vecinos_accesibles, comprobando que el grid, metadatos y resultados anteriores no cambian tras cada rechazo. Observar fallos antes de T019 (RF-06, RF-07, CE-03, CA-02).
- [ ] T019 [US2] Implementar vecinos_accesibles y completar hay_pared en laberinto.py para pasar T018: «lista nueva de Casilla, en orden arriba/derecha/abajo/izquierda», «booleano para un par adyacente válido; simétrico», sin vecinos diagonales ni fuera de 0..14.
- [ ] T020 [US2] Añadir en tests/test_laberinto.py pruebas de repetición de vecinos, modificación de listas devueltas y comprobación de que ni el grid, metadatos ni resultados anteriores cambian (RF-10, CE-06); ejecutarlas antes de cualquier corrección de T021.
- [ ] T021 [US2] Ajustar laberinto.py solo si T020 descubre referencias mutables compartidas, observando primero ese fallo; si el diseño ya pasa, registrar esa evidencia y refactorizar únicamente si aporta claridad, sin introducir código innecesario.
- [ ] T022 [US2] Ejecutar US1 y US2 en tests/test_laberinto.py y registrar simetría, límites, CA-02 y ausencia de regresiones en specs/001-modelo-laberintos/validacion.md, sin iniciar aún la búsqueda de caminos 004.

## Fase 5: US3 — Conocer distancias por el laberinto (P2)

**Objetivo**: distancias transitables completas sin mutación.
**Prueba independiente**: tablero serpenteante conocido y referencia de caminos calculada
solo desde el grid, usando un recorrido con pila en las pruebas, distinto del recorrido en
anchura de producción. No importar fantasma_ia ni llamar a funciones futuras de 004.

- [ ] T023 [US3] Añadir en tests/conftest.py el tablero serpenteante de 225 casillas con ruta de 224 pasos y el oráculo de caminos independiente; añadir en tests/test_laberinto.py comparación de las 225 distancias para cada origen de cada uno de los cinco tableros, rodeos, origen cero, repetibilidad y origen inválido; para cada origen inválido comprobar que grid, metadatos y resultados anteriores permanecen iguales tras el rechazo. Observar fallos antes de T024 (RF-09, CE-05, validación independiente de CA-27).
- [ ] T024 [US3] Implementar distancias_desde en laberinto.py mediante recorrido en anchura con collections.deque, validación inicial del origen y resultados «diccionario nuevo Casilla → entero no negativo, de 225 entradas; origen cero», sin consumo de azar, pygame ni cachés mutables.
- [ ] T025 [US3] Añadir en tests/test_laberinto.py pruebas que alteren diccionarios de distancias devueltos, repitan consultas desde orígenes distintos y comparen grid y resultados anteriores para completar RF-10/CE-06; ejecutarlas antes de T026.
- [ ] T026 [US3] Ajustar laberinto.py solo ante fallos observados en T025, para mantener resultados independientes; si las garantías existentes bastan, registrar que las nuevas pruebas ya pasan y no añadir una capa de código para reproducir lo que ya cumple.
- [ ] T027 [US3] Ejecutar las tres historias en tests/test_laberinto.py y registrar en specs/001-modelo-laberintos/validacion.md los resultados exhaustivos de CE-05 y CE-06; mantener CA-27 literal con buscar_camino como pendiente de integración con 004, sin crear ni simular su aprobación.

## Fase 6: Validación transversal y cierre

**Dependencia**: US1, US2 y US3 completas; no incluye funcionalidad de otras specs.

- [ ] T028 Ejecutar tests/test_laberinto.py en un entorno sin pygame instalado, con pytest y pytest-cov, usando --cov=laberinto --cov-report=term-missing --cov-fail-under=80; exigir pruebas realmente ejecutadas y ≥80 % de líneas de laberinto.py sin exclusiones para eludir el umbral. Registrar informe y estado de salida en specs/001-modelo-laberintos/validacion.md; si se añade otro módulo lógico, acreditar también el mínimo de cada módulo.
- [ ] T029 Recorrer specs/001-modelo-laberintos/quickstart.md y actualizar solo los comandos que la implementación realmente requiera, registrando versiones/plataformas ejecutadas y limitaciones en specs/001-modelo-laberintos/validacion.md; no afirmar pruebas de Python 3.10, Windows o macOS si no se ejecutaron.
- [ ] T030 Revisar laberinto.py, tests/test_laberinto.py y tests/conftest.py para confirmar español, separación lógica/interfaz, simplicidad y alcance; resolver cualquier defecto mediante prueba fallida primero y documentar cumplimiento en specs/001-modelo-laberintos/validacion.md sin añadir dependencias o generación.
- [ ] T031 Completar la matriz de specs/001-modelo-laberintos/validacion.md con evidencias de RF-01 a RF-10, CE-01 a CE-06 y CA-01/CA-02; mantener CA-27 literal como integración pendiente y verificar que base/ permanece intacta; actualizar specs/001-modelo-laberintos/tasks.md únicamente según trabajo efectivamente completado, sin modificar checklists ajenos.
- [ ] T032 Cerrar la fase de implementación con revisión del diff de laberinto.py y demás archivos autorizados, commit descriptivo y push al repositorio sin forzar; comprobar sincronización y registrar el identificador de commit en el informe final de la fase, sin iniciar otra spec ni crear commits vacíos.

## Dependencias y orden de ejecución

```text
T001 + T002 → T003 → T004
  → US1: T005 → T006 → T007 → T008 → T009 → T010 → T011 → T012 → T013 → T014 → T015
  → US2: T016 → T017 → T018 → T019 → T020 → T021 → T022
  → US3: T023 → T024 → T025 → T026 → T027
  → T028 → T029 → T030 → T031 → T032
```

Si una validación detecta un defecto, se corrige y se repite lo afectado antes de avanzar.
Si una prueba de garantía ya pasa con un diseño correcto, se registra y no se inventa código
para forzar una nueva implementación. Cada comportamiento aún ausente requiere su fallo previo.

### Paralelismo real y ejemplos por historia

- Preparación: T001 y T002 pueden editar archivos distintos sin dependencia entre sí;
  T003 espera a ambas. El informe inicial de T004 conserva las versiones registradas en T001.
- US1: no hay ediciones [P]; todas las tareas se apoyan en las mismas pruebas y laberinto.py.
  Tras congelar esos archivos, la lectura de resultados de carga y de contornos puede revisarse
  en paralelo, sin marcar por ello tareas de código como independientes.
- US2: no hay ediciones [P]; las revisiones de resultados de vecinos y límites pueden
  compararse en paralelo después de T019, sin cambiar los archivos compartidos.
- US3: no hay ediciones [P]; tras T024, distintas particiones por origen del conjunto ya
  escrito pueden ejecutarse en procesos separados, si hiciera falta, sin editar en paralelo.

No se dividen archivos ni se añade infraestructura solo para fabricar paralelismo.

## Matriz de cobertura de requisitos

| Requisito/criterio | Tareas principales |
|---|---|
| RF-01 / CE-01 / CA-01 | T005–T006, T013–T015 |
| RF-02 | T011–T015 |
| RF-03 / CE-02 | T005–T010, T013–T015 |
| RF-04 y RF-05 | T013–T015 |
| RF-06 y RF-07 / CE-03 / CA-02 | T016–T019, T022 |
| RF-08 / CE-04 | T016–T019, T023–T024 |
| RF-09 / CE-05 | T023–T024, T027 |
| RF-10 / CE-06 | T011–T012, T016–T019, T020–T021, T023–T027 |
| CA-27 independiente / integración literal | T023–T027 / pendiente explícito en T031 |
| Constitución: independencia, pruebas primero, cobertura y cierre | T005, cada pareja TDD, T028–T032 |

## Estrategia de entrega

MVP: fases 1–3, que entregan lectura y validación con datos preservados; su aceptación
se limita a US1. A continuación añadir consultas y distancias con regresión de lo ya hecho.
No declarar el juego terminado por completar ese MVP ni la implementación aislada de 001.

Las fases enumeradas aquí son agrupaciones del trabajo futuro dentro de implementación,
no órdenes para ejecutar fases de Spec Kit ahora. Mantener commits revisables por grupo de
trabajo y cumplir commit/push al cerrar cada fase solicitada. Esta generación de tareas se
cierra con su propio commit y push; no ejecuta T001 ni inicia automáticamente implementación.
