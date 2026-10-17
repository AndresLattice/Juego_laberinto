# Plan de implementación: Consultar y validar laberintos

**Funcionalidad**: 001-modelo-laberintos | **Fecha**: 2026-10-17
**Rama Git real**: `work`; publicación de la fase en `main`.
**Especificación**: [spec.md](spec.md), incluida la aclaración del contorno.

## Resumen

Implementar un módulo de lógica pura que cargue entradas válidas del catálogo, represente
las paredes sin modificarlas y responda consultas de vecinos y distancias. Usar un tablero
inmutable, validar conectividad y número de conexiones, y calcular distancias con un recorrido
en anchura. No crear ventana, generación, selección aleatoria ni lógica de actores.

Las decisiones y alternativas están en [research.md](research.md), las entidades en
[data-model.md](data-model.md), el contrato en [contracts/laberinto.md](contracts/laberinto.md)
y la validación futura en [quickstart.md](quickstart.md).

## Contexto técnico

- **Lenguaje**: Python 3.10+ según la fuente; intérprete observado en el entorno: 3.12.14.
  Mantener sintaxis y APIs compatibles con 3.10; no afirmar compatibilidad ejecutada sin probarla.
- **Dependencias de ejecución de esta funcionalidad**: solo biblioteca estándar: json,
  pathlib, collections.deque, dataclasses y copy. No importar pygame directa ni indirectamente.
- **Herramientas de desarrollo**: pytest y pytest-cov en requirements-dev.txt. La versión
  compatible se selecciona y registra al implementar; no instalar herramientas para redactar.
- **Producto futuro**: pygame será su única dependencia externa de ejecución; no hace falta
  instalarlo para ejecutar las pruebas de 001.
- **Almacenamiento**: base/laberintos.json, únicamente lectura; no base de datos ni servicios.
- **Plataformas**: macOS, Windows y Linux; pruebas sin pantalla y rutas con pathlib.
- **Tipo de proyecto**: juego de escritorio; esta entrega es su módulo de dominio reutilizable.
- **Escala**: cinco entradas de referencia, 225 casillas, 224 conexiones, grid de 31×31.
  Aceptar un catálogo parcialmente válido sin imponer un número fijo de entradas válidas.
- **Rendimiento**: cada validación o consulta de distancias O(V+E), memoria O(V).
  No inventar límites temporales: los 50 ms de generación y 10 ms de búsqueda son de 002 y 004.
- **Restricciones**: contorno cerrado salvo grid[1][0] y grid[29][30], resultados independientes,
  sin alterar base/, sin aleatoriedad y sin ampliar las reglas de metadatos de la fuente.

## Comprobación de la constitución

| Principio | Antes de investigación | Después del diseño |
|---|---|---|
| Lógica sin pygame | Cumple: solo biblioteca estándar | Cumple: módulo y pruebas sin interfaz |
| Pruebas primero | Exigido en cada comportamiento | Fallo observado → código mínimo → refactorización |
| Cobertura mínima | 80 % por módulo, no solo global | Un módulo lógico: laberinto; medición explícita |
| Dependencia única del juego | No se añaden dependencias de ejecución | Pruebas/cobertura separadas en requirements-dev.txt |
| Español | Documentos y código propio en español | Campos externos grid/id conservados por compatibilidad |
| Simplicidad | Un módulo, sin capas genéricas | Tipos de datos mínimos y funciones directas |
| Aceptación completa | CE-01 a CE-06 obligatorios | Matriz de pruebas; CA-27 literal se integra con 004 |
| Sincronización por fase | Repositorio limpio y actualizado antes de comenzar | Commit y push al cerrar; no iniciar tareas |

No hay excepciones a la constitución. Esta comprobación evalúa el diseño, no afirma que
las pruebas del producto ya existan o pasen.

## Estructura del proyecto

### Documentación de esta funcionalidad

```text
specs/001-modelo-laberintos/
├── spec.md
├── checklists/requirements.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/laberinto.md
└── quickstart.md
```

### Código previsto en la implementación posterior

```text
laberinto.py
requirements-dev.txt
tests/
├── conftest.py
└── test_laberinto.py
base/laberintos.json          # existente, permanece intacto
```

Mantener la organización plana prevista por la fuente; no introducir paquetes de servicios,
repositorios de datos ni un segundo modelo de grafo persistente. La configuración compartida
con otras funcionalidades se añade únicamente cuando exista un consumidor real.

## Diseño y secuencia de validación

1. Escribir primero pruebas de carga y validación, observar fallos por comportamiento ausente,
   implementar carga segura y aceptación de entradas individuales; repetir por comportamiento.
2. Aplicar el mismo ciclo para paredes, vecinos, límites y simetría.
3. Aplicar el ciclo para distancias y ausencia de mutaciones. No desarrollar la búsqueda 004.
4. Ejecutar aceptación de catálogo completo, entradas mixtas, contorno y consultas exhaustivas,
   más cobertura. Registrar resultados y limitaciones, y solo entonces declarar implementada 001.

| Resultado | Evidencia prevista |
|---|---|
| CE-01 / CA-01 | Cinco entradas, dimensiones y conservación exacta de los datos |
| CE-02 | Formatos inválidos, ciclos, desconexión, catálogo mixto, errores de lectura y contorno |
| CE-03 / CA-02 | Vecinos esperados desde el grid para las 1 125 casillas y simetría |
| CE-04 | Consultas inválidas rechazan con ValueError sin mutación |
| CE-05 / CA-27 parcial | Distancias para todos los orígenes, oráculo independiente y camino serpenteante |
| CE-06 | Repetición y modificación de resultados externos no alteran el tablero ni otros resultados |

La comparación literal con buscar_camino requiere la funcionalidad 004: permanece como
aceptación integrada pendiente, sin sustituirla por una afirmación de ejecución. El resto
de 001 es comprobable por separado.

## Seguimiento de complejidad

No se requieren desviaciones ni complejidad adicional. Las decisiones técnicas están
resueltas y el diseño queda listo para solicitar la fase de tareas.
