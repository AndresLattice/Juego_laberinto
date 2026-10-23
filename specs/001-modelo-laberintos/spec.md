# Especificación: Consultar y validar laberintos

**Identificador**: 001-modelo-laberintos
**Rama de trabajo**: `work`; publicación de esta fase en `main`.
**Creada**: 2026-10-17
**Revisada**: 2026-10-17
**Estado**: Implementación verificada; CA-27 literal aprobado al integrar 004.
**Entrada**: `$speckit.specify 001`, sobre la descomposición existente.
**Fuente**: [SPEC-LAB-001 v1.3, §3, §4.3 y §13](../../base/SPEC.md).
**Gobierno**: [Constitución 1.0.0](../../.specify/memory/constitution.md).

## Clarifications

### Session 2026-10-17

- Q: ¿Se rechaza un laberinto cuyo interior es válido pero tiene aperturas exteriores
  adicionales o la entrada o salida cerradas? → A: Sí; exigir el contorno cerrado salvo
  entrada izquierda en (0,0) y salida derecha en (14,14).

## Escenarios de usuario y pruebas

### Historia 1 — Disponer de tableros confiables (prioridad P1)

Como responsable del juego quiero cargar los laberintos válidos del catálogo para ofrecer
partidas donde todas las casillas se puedan alcanzar y exista un único camino entre ellas.

**Por qué esta prioridad**: los movimientos y la persecución necesitan un tablero válido.
**Prueba independiente**: cargar el catálogo de referencia y variantes controladas sin iniciar
una partida ni abrir una ventana; comparar las entradas aceptadas y rechazadas.

**Escenarios de aceptación**:

1. Dado el catálogo de referencia con cinco entradas válidas, cuando se carga, entonces se
   obtienen cinco tableros de 15×15, conservando su identificador, tipo y descripción.
2. Dado un catálogo con una entrada válida y otra inválida, cuando se carga, entonces se
   conserva la válida sin alterarla y se ignora la inválida.
3. Dado un archivo inexistente, ilegible, con contenido no interpretable o sin entradas
   válidas, cuando se carga, entonces se informa que no hay catálogo utilizable sin cerrar
   el proceso ni ofrecer un tablero inválido.
4. Dada una entrada con forma incorrecta, caracteres ajenos al formato, centros bloqueados,
   casillas desconectadas o ciclos, cuando se valida, entonces se rechaza esa entrada.
5. Dado un tablero con interior válido y contorno cerrado salvo entrada izquierda en (0,0)
   y salida derecha en (14,14), cuando se valida, entonces se acepta. Si se cierra cualquiera
   de esas aperturas o se abre cualquier otro punto del contorno, se rechaza la entrada.

### Historia 2 — Consultar pasos permitidos (prioridad P1)

Como responsable de las reglas quiero conocer las casillas vecinas accesibles para impedir
que los actores crucen paredes o abandonen el tablero.

**Por qué esta prioridad**: hace comprobables los movimientos sin desarrollar la interfaz.
**Prueba independiente**: comparar consultas en tableros de paredes conocidas con sus
conexiones esperadas, sin dados ni actores.

**Escenarios de aceptación**:

1. Dada la casilla (0,0) del laberinto 1, cuando se consultan sus vecinos accesibles,
   entonces coinciden exactamente con las conexiones abiertas de la fuente (CA-02).
2. Dadas dos casillas vecinas, cuando se consulta su conexión en ambos sentidos,
   entonces se obtiene el mismo resultado; una pared impide el paso en ambos sentidos.
3. Dada una casilla de borde, cuando se consultan vecinos, entonces no se devuelven
   diagonales ni coordenadas exteriores, incluso junto a las aperturas de entrada o meta.
4. Dada una coordenada fuera del dominio o una consulta de pared entre casillas no
   adyacentes, cuando se consulta, entonces se informa que la consulta no es válida,
   sin devolver una conexión ficticia ni modificar el tablero.

### Historia 3 — Conocer distancias por el laberinto (prioridad P2)

Como responsable de la aparición del fantasma quiero conocer la distancia real desde una
casilla hasta todas las demás para poder aplicar después la separación mínima de aparición.

**Por qué esta prioridad**: habilita decisiones de juego sin incluirlas en este alcance.
**Prueba independiente**: usar tableros pequeños de referencia conceptual ampliados al formato
admitido o tableros completos con caminos conocidos y comparar las distancias esperadas.

**Escenarios de aceptación**:

1. Dado cualquier origen válido, cuando se consultan distancias, entonces se incluyen las
   225 casillas, el origen tiene distancia cero y cada otra casilla tiene el número de pasos
   de su único camino desde el origen.
2. Dado un recorrido con rodeos impuestos por paredes, cuando se consulta su distancia,
   entonces se cuentan los pasos transitables y no la separación en línea recta.
3. Dada la misma consulta repetida, cuando se ejecuta, entonces devuelve las mismas
   distancias y no cambia el laberinto ni los resultados de consultas anteriores.

### Casos límite

- Catálogo vacío, estructura superior distinta de una lista, entrada que no es un registro
  o campo de tablero ausente: no se debe propagar un fallo de lectura sin controlar.
- Cantidad de filas o columnas distinta de 31, caracteres distintos de pared y espacio,
  un centro bloqueado, un ciclo o una región inaccesible: entrada rechazada.
- Una única entrada válida: se conserva; decidir cómo evitar repeticiones pertenece a 002.
- Coordenadas negativas, 15 o mayores y pares no adyacentes: consulta inválida.
- Aperturas de entrada y meta: no agregan casillas exteriores ni conexiones internas.
- Entrada cerrada, salida cerrada o cualquier apertura adicional en el contorno, incluidas
  las esquinas: entrada rechazada aunque conserve conectividad y 224 conexiones internas.
- Tablero cuyo camino abarca las 225 casillas: las distancias siguen siendo completas.

## Requisitos

### Requisitos funcionales

- **RF-01**: El sistema DEBE representar 225 casillas en un tablero de 15×15, con coordenadas
  (columna, fila) entre 0 y 14, entrada en (0,0) y meta en (14,14).
- **RF-02**: El sistema DEBE leer el catálogo existente y conservar, para cada entrada
  aceptada, su identidad, tipo, descripción, entrada, salida y distribución de paredes,
  sin reescribir el archivo de origen.
- **RF-03**: El sistema DEBE aceptar únicamente tableros con 31 filas de 31 caracteres,
  usando solo `#` para pared y espacio para camino, con los 225 centros transitables,
  todas las casillas conectadas y exactamente 224 conexiones internas abiertas. El contorno
  DEBE ser pared salvo dos espacios obligatorios: entrada izquierda de (0,0) y salida derecha
  de (14,14); cualquier apertura adicional o cierre de una de estas dos invalida la entrada.
- **RF-04**: El sistema DEBE evaluar las entradas por separado e ignorar las inválidas sin
  descartar las válidas por la presencia de otras inválidas.
- **RF-05**: El sistema DEBE informar al consumidor que el catálogo no es utilizable si
  falta, no se puede leer, no tiene una estructura interpretable o no conserva entradas
  válidas. NO DEBE cerrar el proceso como consecuencia de estos casos.
- **RF-06**: El sistema DEBE devolver exclusivamente vecinos ortogonales dentro del tablero
  conectados sin pared y permitir consultar las paredes entre casillas adyacentes.
- **RF-07**: Las consultas de conexión DEBEN ser simétricas. Las aperturas exteriores NO
  DEBEN permitir consultar o devolver una casilla fuera del tablero.
- **RF-08**: El sistema DEBE informar de las consultas inválidas sobre coordenadas fuera
  del dominio o paredes entre casillas no adyacentes, sin inventar resultados transitables.
- **RF-09**: El sistema DEBE proporcionar distancias desde cualquier casilla válida hasta
  las 225 casillas contando únicamente pasos permitidos; el origen DEBE tener distancia cero.
- **RF-10**: Las consultas de vecinos, paredes y distancias NO DEBEN modificar el tablero,
  su identidad ni resultados entregados previamente.

### Entidades principales

- **Casilla**: posición identificada por columna y fila.
- **Laberinto**: conjunto de 225 casillas y sus paredes, con entrada y meta.
- **Conexión**: paso abierto entre dos casillas ortogonales contiguas; se cuenta una vez.
- **Entrada del catálogo**: identidad, tipo, descripción y representación de un laberinto.
- **Catálogo utilizable**: colección de entradas válidas; puede contener menos de cinco si
  la fuente contiene entradas rechazadas.
- **Distancias**: correspondencia entre cada casilla y el número de pasos desde un origen.

## Criterios de éxito

### Resultados medibles

- **CE-01**: El catálogo de referencia entrega exactamente cinco laberintos de 225 casillas
  y conserva todos sus datos descriptivos (CA-01; historia 1; RF-01 y RF-02).
- **CE-02**: Todos los casos de entrada inválida de historia 1 y casos límite son rechazados;
  cada entrada válida de un catálogo mixto se conserva y ninguno de los errores de lectura
  enumerados cierra el proceso (RF-03 a RF-05). La validación del contorno acepta únicamente
  las dos aperturas obligatorias; se comprueba el rechazo al cerrar cada una o abrir
  individualmente cualquier otro punto del contorno de un tablero con interior válido.
- **CE-03**: Para las 225 casillas de cada uno de los cinco tableros de referencia, el
  conjunto de vecinos coincide con las conexiones abiertas, sin diagonales ni salidas del
  dominio; cada conexión es simétrica (CA-02; historia 2; RF-06 y RF-07).
- **CE-04**: Todas las consultas inválidas enumeradas se notifican sin alterar el tablero
  ni declarar un paso inexistente (historia 2; RF-08).
- **CE-05**: Para cada origen de cada tablero de referencia, las distancias cubren las
  225 casillas y coinciden con longitudes de caminos de referencia; origen cero en todos
  los casos. Cuando 004 esté disponible, se verifica también CA-27 por integración
  (historia 3; RF-09).
- **CE-06**: Repetir las consultas de las historias 2 y 3 conserva el contenido original del
  tablero y de los resultados anteriores (RF-10).

### Trazabilidad de los criterios originales

| ID | Criterio original | Comprobación en esta funcionalidad |
|---|---|---|
| CA-01 | `Laberinto` carga los 5 laberintos del JSON; cada uno tiene 15×15 casillas. | CE-01 |
| CA-02 | `vecinos_accesibles((0,0))` del laberinto 1 coincide con las paredes del `grid`. | CE-03 |
| CA-27 | `distancias_desde(c)` da 0 en `c` y, para cada casilla, el mismo valor que `len(buscar_camino(c, casilla))`. | CE-05; comparación literal con 004 al integrarla |

## Supuestos

- La fuente del catálogo es [base/laberintos.json](../../base/laberintos.json), una lista
  de cinco registros con campos `id`, `tipo`, `descripcion`, `entrada`, `salida` y `grid`.
  El formato de datos de §4.3 se conserva; seleccionar APIs y algoritmos corresponde al plan.
- Los centros de casilla y paredes se interpretan conforme a §4.3 del documento fuente.
  Las aperturas del contorno no forman parte de las 224 conexiones internas. En el formato
  de 31×31, las únicas posiciones abiertas del contorno son `grid[1][0]` y `grid[29][30]`;
  todas las demás posiciones del contorno, incluidas sus cuatro esquinas, contienen `#`.
- Se considera inválida la estructura superior que no sea una lista. Los registros sin
  tablero se rechazan individualmente. El detalle del mecanismo para informar errores se
  define en el plan, manteniendo los resultados observables de esta especificación.
- No se añaden obligaciones sobre datos decorativos o metadatos ajenas a la fuente.
- No se requiere implementar otras funcionalidades para probar este contrato. Para CA-27
  se usan caminos conocidos o una referencia independiente durante esta fase; no se inicia
  la implementación de la búsqueda 004 para cerrar esta especificación.
- No se incluyen generación, selección aleatoria, modos, respaldo mediante generación,
  dados, actores, turnos, interfaz, textos de error en pantalla ni exportación de imágenes.
  El consumidor aplica el respaldo y sus mensajes según 002 y 008.
- La implementación posterior DEBE cumplir la constitución: pruebas antes del código,
  lógica sin dependencias gráficas, cobertura mínima del 80 % por módulo y español.
  Esta fase valida el documento; no acredita ejecución ni cobertura del producto.
