# Checklist de calidad de requisitos: Modelo y validación de laberintos

**Propósito**: revisar integridad del modelo, errores de catálogo y trazabilidad antes de tareas.
**Creada**: 2026-10-17
**Funcionalidad**: [spec.md](../spec.md)
**Profundidad**: estándar. **Destinatario**: responsable de revisión documental previa a tareas.
**Enfoque inferido**: integridad de datos y manejo de errores, dentro del alcance de 001.

**Nota**: lista personalizada generada mediante `$speckit-checklist`.
**Responsabilidad**: las casillas pertenecen al revisor. `[x]` acredita revisión satisfactoria
sobre la calidad del requisito; no significa implementación completa ni prueba del producto.
Todos los elementos se generan pendientes y no han sido evaluados en esta fase.

Referencias: [plan](../plan.md), [modelo](../data-model.md),
[contrato](../contracts/laberinto.md), [investigación](../research.md) y
[constitución](../../../.specify/memory/constitution.md).
Los identificadores RF/CE y los nombres de sección permiten localizar cada criterio.

## Integridad y completitud de los datos

- [ ] CHK001 ¿Están definidos el tamaño del tablero, el dominio de coordenadas y las posiciones lógicas de entrada y meta? [Completitud, Spec §RF-01]
- [ ] CHK002 ¿El requisito de formato distingue dimensiones, caracteres permitidos y centros transitables? [Completitud, Spec §RF-03]
- [ ] CHK003 ¿Se exigen por separado conectividad completa y exactamente 224 conexiones internas, sin confundir una condición con la otra? [Claridad, Spec §RF-03]
- [ ] CHK004 ¿La regla aprobada del contorno identifica las dos aperturas obligatorias y rechaza cierres y aperturas adicionales, incluidas las esquinas? [Cobertura, Spec §Clarifications; Spec §RF-03; Spec §CE-02]
- [ ] CHK005 ¿Se especifica qué información del registro original se conserva y que el archivo fuente no se reescribe? [Completitud, Spec §RF-02]
- [ ] CHK006 ¿Está clara la diferencia entre coordenadas de casilla y coordenadas de entrada/salida en el archivo? [Claridad, Spec §Supuestos; Modelo §EntradaCatalogo; Investigación §5]

## Claridad de consultas y resultados

- [ ] CHK007 ¿Los requisitos delimitan vecinos ortogonales, paredes y prohibición de casillas exteriores sin depender de la interfaz? [Claridad, Spec §RF-06; Spec §RF-07]
- [ ] CHK008 ¿La simetría de las consultas de conexión se exige explícitamente y es consistente con la definición de pared? [Consistencia, Spec §RF-07; Contrato §Garantías de consultas]
- [ ] CHK009 ¿Se definen las consultas inválidas, incluidos origen igual a destino para pared, diagonales, no adyacencia y coordenadas fuera del dominio? [Cobertura, Spec §RF-08; Contrato §Precondiciones y errores]
- [ ] CHK010 ¿El contrato precisa forma y tipos de coordenadas y distingue enteros de booleanos sin contradecir el dominio de la especificación? [Claridad, Spec §RF-01; Modelo §Casilla; Contrato §Precondiciones y errores]
- [ ] CHK011 ¿La distancia está definida como número de pasos permitidos y exige origen cero y cobertura de las 225 casillas? [Claridad, Spec §RF-09; Spec §CE-05]
- [ ] CHK012 ¿Se especifica la independencia de resultados sucesivos y la preservación del tablero y sus metadatos? [Completitud, Spec §RF-10; Spec §CE-06]

## Errores, alternativas y recuperación

- [ ] CHK013 ¿Los requisitos cubren archivo inexistente, ilegible, contenido mal formado y estructura superior no admitida? [Cobertura, Spec §Historia 1; Spec §RF-05; Spec §Supuestos]
- [ ] CHK014 ¿Se distingue una lista vacía de una lista sin entradas válidas y se define en ambos casos que el catálogo no es utilizable? [Completitud, Spec §Casos límite; Modelo §ResultadoCarga]
- [ ] CHK015 ¿Está definido el rechazo individual de entradas inválidas sin perder las válidas de un catálogo mixto? [Cobertura, Spec §RF-04; Spec §Historia 1]
- [ ] CHK016 ¿El resultado de carga parcial distingue entradas aceptadas, rechazadas y aviso global de indisponibilidad? [Claridad, Spec §RF-04; Spec §RF-05; Modelo §ResultadoCarga]
- [ ] CHK017 ¿La ausencia de cierre del proceso por errores esperados está exigida sin imponer que se oculten defectos inesperados? [Consistencia, Spec §RF-05; Contrato §Precondiciones y errores]
- [ ] CHK018 ¿La responsabilidad del respaldo queda asignada al consumidor y separada de la validación del catálogo? [Consistencia, Spec §Supuestos; Contrato §Uso previsto por consumidores]

## Criterios de aceptación y trazabilidad

- [ ] CHK019 ¿CE-01 a CE-06 proporcionan una comprobación objetiva para todos los requisitos RF-01 a RF-10? [Medibilidad, Spec §Resultados medibles; Plan §Diseño y secuencia de validación]
- [ ] CHK020 ¿La población de referencia de cinco laberintos se distingue del número variable de entradas válidas de otros catálogos? [Consistencia, Spec §CE-01; Spec §RF-04; Spec §Entidades principales]
- [ ] CHK021 ¿Los CA-01, CA-02 y CA-27 mantienen su significado respecto de la fuente y tienen responsables identificados? [Trazabilidad, Spec §Trazabilidad de los criterios originales]
- [ ] CHK022 ¿Se diferencia la aceptación independiente de distancias de la comparación literal de CA-27 pendiente de integración con 004? [Dependencias, Spec §CE-05; Spec §Supuestos; Plan §Diseño y secuencia de validación]

## Restricciones, supuestos y límites

- [ ] CHK023 ¿La prohibición de dependencias gráficas en lógica y la separación de herramientas de desarrollo son consistentes entre constitución y plan? [Consistencia, Constitución §I y §IV; Plan §Contexto técnico]
- [ ] CHK024 ¿Se exige el ciclo de pruebas primero y un mínimo de cobertura del 80 % por módulo, sin confundirlo con el porcentaje global? [Medibilidad, Constitución §II y §III; Plan §Comprobación de la constitución]
- [ ] CHK025 ¿Las decisiones de Python, ventana, generación y ejecución están asignadas a la funcionalidad correspondiente sin ampliar 001? [Alcance, Plan §Decisiones técnicas confirmadas por el usuario; Spec §Supuestos]
- [ ] CHK026 ¿Los requisitos de escala y rendimiento distinguen las obligaciones de 001 de los límites temporales de generación y persecución? [Claridad, Plan §Contexto técnico; Spec §RF-01]
- [ ] CHK027 ¿Las reglas sobre metadatos faltantes o identidades repetidas son coherentes entre preservación y exclusión de validaciones nuevas? [Supuestos, Spec §RF-02; Spec §Supuestos; Investigación §5; Modelo §EntradaCatalogo]
- [ ] CHK028 ¿La definición documental de terminado distingue requisitos revisados, implementación aceptada e integración pendiente? [Consistencia, Constitución §VII; Spec §Estado; Spec §Supuestos; Plan §Diseño y secuencia de validación]

## Notas

- Marcar casillas únicamente tras revisar los requisitos y documentar hallazgos.
- Mantener pendiente lo que requiera evaluación, aclaración o corrección.
- `$speckit-implement` consulta este estado como condición previa y no modifica sus marcas.
- requirements.md mantiene su ciclo propio mediante specify/clarify; no se modifica aquí.
- No se añaden criterios sobre pantallas, generación o persecución fuera de 001; solo se
  revisa que sus límites y dependencias estén documentados.
- Esta lista no crea tareas, no ejecuta pruebas y no modifica especificaciones o código.
