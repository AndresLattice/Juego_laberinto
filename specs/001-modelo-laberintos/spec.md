# Especificación: Consultar y validar laberintos

**Identificador**: 001-modelo-laberintos
**Creada**: 2026-10-17
**Estado**: Descompuesta para revisión; no implementada.
**Fuente**: [SPEC-LAB-001 v1.3](../../base/SPEC.md), idéntica al adjunto analizado.
**Gobierno**: [Constitución 1.0.0](../../.specify/memory/constitution.md).

## Escenarios de usuario y pruebas

### Historia 1 — Consultar y validar laberintos (prioridad P1)

Como responsable del juego quiero cargar y consultar los laberintos para que todo movimiento respete sus paredes.

**Valor**: entregar esta capacidad sin asumir que la interfaz y el juego completos ya existen.
**Prueba independiente**: ejecutar los escenarios siguientes con entradas controladas y dobles de
las dependencias; para la vista, una demostración visual aislada. Las pruebas integradas se
realizan cuando estén disponibles los consumidores correspondientes.

1. Dado el catálogo válido, cuando se carga, entonces se obtienen los cinco tableros de 15×15 y sus vecinos coinciden con el grid.
2. Dada cualquier casilla, cuando se consultan sus distancias, entonces su distancia es cero y las demás coinciden con el número de pasos de su camino.

### Casos límite

- Archivo inexistente, JSON mal formado, catálogo vacío o mezcla de entradas válidas e inválidas.
- Tableros desconectados, con ciclos, centros bloqueados y coordenadas fuera del dominio.

## Requisitos

### Requisitos funcionales

- **RF-01**: Se DEBE representar coordenadas (columna, fila) en 0..14 y mapearlas a grid[2*fila+1][2*columna+1].
- **RF-02**: Se DEBE consultar paredes y vecinos ortogonales sin permitir posiciones fuera del tablero; las aperturas exteriores no crean casillas jugables.
- **RF-03**: Se DEBE cargar las cinco entradas de base/laberintos.json y conservar identidad, nombre y grid.
- **RF-04**: Se DEBE validar 31 filas de 31 caracteres, solo # y espacio, 225 centros transitables, conectividad y exactamente 224 conexiones entre casillas; ignorar entradas inválidas.
- **RF-05**: Se DEBE calcular distancias por caminos accesibles desde cualquier casilla; no usar distancia en línea recta.
- **RF-06**: Se DEBE informar al consumidor si el catálogo falta, es ilegible, contiene JSON inválido o no tiene entradas válidas; no cerrar el proceso.

### Entidades

Laberinto, casilla, conexión y catálogo validado.

### Fuera de alcance

No genera tableros ni decide modos, turnos, aparición o presentación de errores.

## Criterios de éxito

- Todos los escenarios y requisitos anteriores tienen una comprobación que pasa antes de
  declarar implementada esta funcionalidad; esta descomposición no afirma que ya pasen.
- Se conservan los siguientes criterios originales, sin renumerarlos:

| ID | Criterio original |
|---|---|
| CA-01 | `Laberinto` carga los 5 laberintos del JSON; cada uno tiene 15×15 casillas. |
| CA-02 | `vecinos_accesibles((0,0))` del laberinto 1 coincide con las paredes del `grid`. |
| CA-27 | `distancias_desde(c)` da 0 en `c` y, para cada casilla, el mismo valor que `len(buscar_camino(c, casilla))`. |

- Cada requisito funcional adicional a los CA originales se verifica con prueba automatizada
  si es lógica, o revisión visual/funcional documentada si es presentación.
- La implementación cumple pruebas primero, lógica sin pygame y al menos 80 % de cobertura
  por cada módulo de lógica, incluso cuando el comando original solo comprueba el total.

## Dependencias y supuestos

- No requiere implementar otras especificaciones para validar su contrato.

Las reglas de formato de §4.3 se aplican a la validación. El consumidor decide el respaldo. CA-27 usa caminos conocidos como referencia y se integra también con 004.

## Referencia y límites de esta división

Los contratos y valores numéricos originales de las secciones referenciadas se mantienen.
La arquitectura de §12 es orientación para la planificación, no nuevas funciones del producto.
Los archivos de base son material de referencia y no se modifican en esta fase.
Las contradicciones señaladas requieren decisión antes de planificar el aspecto afectado.
Las mejoras futuras de §15 y alternativas descartadas de §8.6 permanecen fuera de alcance.

### Extractos originales de referencia


> ## 3. Glosario
>
> | Término | Definición |
> |---|---|
> | Casilla (celda) | Unidad del tablero. Coordenada `(col, fila)`, ambas en `0..14`. `(0,0)` es arriba-izquierda. |
> | Paso | Movimiento de una casilla a una casilla vecina (arriba, abajo, izquierda, derecha) sin cruzar pared. No hay movimiento en diagonal. |
> | Entrada | Casilla `(0,0)`. Su pared izquierda está abierta. |
> | Meta | Casilla `(14,14)`. Su pared derecha está abierta. |
> | Turno | Tirada del dado + movimiento de un actor (jugador o fantasma). |
> | Ronda | Turno del jugador seguido del turno del fantasma. |
> | Captura | El actor que se mueve entra a la casilla donde está el otro actor (ver 6.4). |
> | Pila | Estructura LIFO donde el backtracking guarda el camino que está explorando. Se dibuja como un tarro. |
> | Apilar / Desapilar | Meter una casilla en la cima de la pila / sacar la casilla de la cima (retroceso). |
> | Traza | Lista ordenada de eventos (apilar, desapilar, encontrado) que produce la búsqueda. Se usa para animar el visualizador. |
