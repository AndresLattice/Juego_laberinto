# Especificación: Encontrar caminos y explicar el backtracking

**Identificador**: 004-busqueda-con-traza
**Creada**: 2026-10-17
**Estado**: Implementada y verificada; ver [validacion.md](validacion.md).
**Fuente**: [SPEC-LAB-001 v1.3](../../base/SPEC.md), idéntica al adjunto analizado.
**Gobierno**: [Constitución 1.0.0](../../.specify/memory/constitution.md).

## Escenarios de usuario y pruebas

### Historia 1 — Encontrar caminos y explicar el backtracking (prioridad P1)

Como docente quiero un camino acompañado de los pasos de búsqueda para explicar avance, retroceso y pila.

**Valor**: entregar esta capacidad sin asumir que la interfaz y el juego completos ya existen.
**Prueba independiente**: ejecutar los escenarios siguientes con entradas controladas y dobles de
las dependencias; para la vista, una demostración visual aislada. Las pruebas integradas se
realizan cuando estén disponibles los consumidores correspondientes.

1. Dado un origen y un destino alcanzable, cuando se busca, entonces el camino excluye el origen, incluye el destino y solo cruza conexiones abiertas.
2. Dado un laberinto con ramas sin salida, cuando se busca dos veces desde las mismas casillas, entonces se obtiene la misma traza con retrocesos coherentes.

### Casos límite

- Origen igual a destino.
- Destino desconectado en un tablero de prueba.
- Ramas que exigen múltiples retrocesos y camino que ocupa todo el tablero.

## Requisitos

### Requisitos funcionales

- **RF-01**: Se DEBE buscar con pila explícita y visitados en orden fijo arriba, derecha, abajo, izquierda.
- **RF-02**: Se DEBE emitir eventos apilar, desapilar y encontrado; cada evento contiene la casilla y una copia inmutable de la pila después de aplicarlo.
- **RF-03**: Se DEBE empezar apilando el origen y terminar con encontrado; la pila final sin el origen debe coincidir con el camino.
- **RF-04**: Se DEBE para origen igual a destino devolver camino vacío y traza apilar/origen, encontrado/origen.
- **RF-05**: Se DEBE desapilar únicamente la cima cuando no queden vecinos accesibles sin visitar; no desapilar una pila vacía.
- **RF-06**: Se DEBE ofrecer consulta del camino sin traza y notificar con ValueError un destino inalcanzable.
- **RF-07**: Se DEBE no superar 225 casillas en la pila; recalcular la búsqueda cuando el consumidor solicite un nuevo destino.

### Entidades

Camino, evento de traza, pila y visitados.

### Fuera de alcance

No mueve al fantasma, no consume dados y no anima ni dibuja eventos.

## Criterios de éxito

- Todos los escenarios y requisitos anteriores tienen una comprobación que pasa antes de
  declarar implementada esta funcionalidad; esta descomposición no afirma que ya pasen.
- Se conservan los siguientes criterios originales, sin renumerarlos:

| ID | Criterio original |
|---|---|
| CA-03 | `buscar_camino` devuelve un camino donde cada par de casillas consecutivas es vecino sin pared, empieza junto al origen y termina en el destino. |
| CA-04 | `buscar_camino(a, a)` devuelve `[]`. |
| CA-05 | Desde `(0,0)` hasta `(14,14)` existe camino en los 5 laberintos. |
| CA-17 | La traza empieza con `apilar(origen)` y termina con `encontrado(destino)`; la pila del último evento, sin el origen, es igual al camino devuelto. |
| CA-18 | En la traza, `#apilar − #desapilar = len(camino) + 1`, y nunca se desapila con la pila vacía. |
| CA-19 | Cada `desapilar(c)` en la traza ocurre cuando `c` es la cima y ya no tiene vecinos accesibles sin visitar. |
| CA-20 | Para el mismo laberinto, origen y destino, la traza es idéntica en dos ejecuciones (determinista). |

- Cada requisito funcional adicional a los CA originales se verifica con prueba automatizada
  si es lógica, o revisión visual/funcional documentada si es presentación.
- La implementación cumple pruebas primero, lógica sin pygame y al menos 80 % de cobertura
  por cada módulo de lógica, incluso cuando el comando original solo comprueba el total.

## Dependencias y supuestos

- [001-modelo-laberintos](../001-modelo-laberintos/spec.md).

RNF-4 exige menos de 10 ms para una búsqueda de 15×15; registrar entorno y medición. La condición de laberinto perfecto garantiza camino único.

## Referencia y límites de esta división

Los contratos y valores numéricos originales de las secciones referenciadas se mantienen.
La arquitectura de §12 es orientación para la planificación, no nuevas funciones del producto.
Los archivos de base son material de referencia y no se modifican en esta fase.
Las contradicciones señaladas requieren decisión antes de planificar el aspecto afectado.
Las mejoras futuras de §15 y alternativas descartadas de §8.6 permanecen fuera de alcance.

### Extractos originales de referencia


> ## 7. Algoritmo del fantasma: backtracking
>
> ### 7.1 Idea
> Búsqueda en profundidad desde la casilla del fantasma, guardando el camino actual en una **pila**:
> - **Apilar:** avanzar a un vecino accesible no visitado.
> - **Desapilar (retroceder):** si la casilla de la cima no tiene más vecinos por probar (callejón sin salida o ramas ya agotadas), se saca de la pila y se vuelve a la anterior.
> - **Encontrado:** cuando la cima es la casilla del jugador, el contenido de la pila (de abajo hacia arriba) **es** el camino.
>
> Como el laberinto es perfecto, el camino encontrado es el único posible y por lo tanto el más corto.
>
> ### 7.2 Contrato
>
> ```python
> from typing import Literal, NamedTuple
>
> Casilla = tuple[int, int]
>
> class Evento(NamedTuple):
>     tipo: Literal["apilar", "desapilar", "encontrado"]
>     casilla: Casilla          # casilla apilada / desapilada / destino
>     pila: tuple[Casilla, ...] # copia de la pila DESPUÉS del evento (de base a cima)
>
> def buscar_camino_con_traza(laberinto, origen: Casilla, destino: Casilla
>                             ) -> tuple[list[Casilla], list[Evento]]:
>     """Devuelve (camino, traza).
>     camino: casillas desde el paso siguiente a `origen` hasta `destino` (incluido);
>             [] si origen == destino.
>     traza:  eventos en orden; el primero es apilar(origen) y el último es encontrado(destino).
>     Lanza ValueError si no existe camino (no debe ocurrir en un laberinto perfecto)."""
>
> def buscar_camino(laberinto, origen: Casilla, destino: Casilla) -> list[Casilla]:
>     """Atajo: devuelve solo el camino."""
> ```
>
> ### 7.3 Pseudocódigo (versión iterativa con pila explícita)
>
> Se usa **pila explícita** en vez de recursión, porque así la pila que se dibuja en el tarro es literalmente la estructura del algoritmo. Es equivalente a la versión recursiva: la pila de llamadas se vuelve visible.
>
> ```
> pila      ← [origen];  visitados ← {origen};  registrar apilar(origen)
> mientras pila no esté vacía:
>     actual ← cima(pila)
>     si actual == destino:
>         registrar encontrado(destino);  retornar pila[1:]
>     vecino ← primer vecino accesible de actual NO visitado
>              (orden fijo: arriba, derecha, abajo, izquierda)
>     si existe vecino:
>         apilar(vecino);  visitados += {vecino};  registrar apilar(vecino)
>     si no:
>         desapilar();  registrar desapilar(actual)          # <- backtracking
> lanzar ValueError
> ```
>
> - Tamaño máximo de la pila: 225 casillas.
> - El camino se recalcula **en cada turno** del fantasma, porque el jugador se mueve.
> - El orden fijo de vecinos hace la traza **determinista**: misma posición = misma animación (útil para explicar en clase).
