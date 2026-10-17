# Especificación: Jugar turnos y resolver persecución

**Identificador**: 005-reglas-partida
**Creada**: 2026-10-17
**Estado**: Descompuesta para revisión; no implementada.
**Fuente**: [SPEC-LAB-001 v1.3](../../base/SPEC.md), idéntica al adjunto analizado.
**Gobierno**: [Constitución 1.0.0](../../.specify/memory/constitution.md).

## Escenarios de usuario y pruebas

### Historia 1 — Jugar turnos y resolver persecución (prioridad P1)

Como jugador quiero avanzar con mi tirada y escapar del fantasma respetando turnos, paredes y condiciones de fin.

**Valor**: entregar esta capacidad sin asumir que la interfaz y el juego completos ya existen.
**Prueba independiente**: ejecutar los escenarios siguientes con entradas controladas y dobles de
las dependencias; para la vista, una demostración visual aislada. Las pruebas integradas se
realizan cuando estén disponibles los consumidores correspondientes.

1. Dado un jugador con cinco pasos, cuando avanza dos y termina voluntariamente el turno, entonces aparece el fantasma si corresponde y comienza su turno.
2. Dado un fantasma a tres pasos con tirada cinco, cuando persigue, entonces captura exactamente en su tercer paso y la partida termina inmediatamente.

### Casos límite

- ENTER antes de tirar no termina el turno; ENTER después de tirar permite usar cero pasos.
- Victoria antes de terminar el primer turno: no aparece ni juega el fantasma.
- Captura intermedia con pasos sobrantes, teclas fuera de estado y reinicio tras derrota/victoria.

## Requisitos

### Requisitos funcionales

- **RF-01**: Se DEBE comenzar en (0,0), turno 1, sin fantasma; permitir tirar solo antes del movimiento y terminar anticipadamente solo después de tirar.
- **RF-02**: Se DEBE descontar un paso por movimiento válido; ignorar paredes, límites y movimientos sin pasos, permitiendo volver por casillas visitadas.
- **RF-03**: Se DEBE al finalizar el primer turno, elegir uniformemente una casilla a distancia de camino al menos seis del jugador y distinta de la meta; mostrar la aparición durante un segundo antes de su tirada.
- **RF-04**: Se DEBE alternar tirada del fantasma, búsqueda, reproducción terminada y movimiento; bloquear entradas ajenas al estado.
- **RF-05**: Se DEBE avanzar por el camino min(dado, longitud) pasos, uno cada 0,25 s; detectar captura después de cada paso de cualquiera de los actores.
- **RF-06**: Se DEBE resolver victoria al entrar a la meta y derrota al ocupar la casilla del otro actor; no continuar moviendo tras terminar.
- **RF-07**: Se DEBE después del turno del fantasma volver a la tirada del jugador e incrementar el contador.
- **RF-08**: Se DEBE reiniciar desde pantalla final con nuevo tablero en el mismo modo, turno 1, sin fantasma ni marcas; avisar al consumidor que debe limpiar el reproductor.
- **RF-09**: Se DEBE abandonar al menú sin confirmar, y permitir terminar el proceso desde cualquier estado por cierre de ventana.

### Entidades

Partida, actor, posición, pasos restantes, turno, estado y resultado.

### Fuera de alcance

No dibuja personajes ni procesa eventos de pygame. Recibe órdenes y tiempo; puede sustituir reproducción y azar por dobles de prueba.

## Criterios de éxito

- Todos los escenarios y requisitos anteriores tienen una comprobación que pasa antes de
  declarar implementada esta funcionalidad; esta descomposición no afirma que ya pasen.
- Se conservan los siguientes criterios originales, sin renumerarlos:

| ID | Criterio original |
|---|---|
| CA-07 | Un movimiento del jugador contra una pared no cambia su posición ni los pasos restantes. |
| CA-08 | El jugador no puede moverse con 0 pasos restantes. |
| CA-09 | El fantasma **no existe** antes de que termine el primer turno del jugador y aparece justo después. |
| CA-10 | En 10 000 apariciones simuladas (jugador en posiciones al azar), el fantasma **nunca** aparece a menos de 6 pasos del jugador ni en la meta. |
| CA-11 | Con el jugador a distancia 3 del fantasma y un dado de 5, el fantasma lo captura **en su 3.er paso** y el estado pasa a `DERROTA` (cruce = captura). |
| CA-12 | Con el jugador a distancia 8 y un dado de 4, el fantasma avanza exactamente 4 casillas por el camino y no hay captura. |
| CA-13 | Si el jugador entra a `(14,14)` con pasos de sobra, el estado pasa a `VICTORIA`. |
| CA-14 | Si el jugador entra a la casilla del fantasma, el estado pasa a `DERROTA` aunque le queden pasos. |
| CA-15 | Tras tirar un 5 y moverse 2 pasos, `ENTER` termina el turno y pasa al fantasma. `ENTER` antes de tirar el dado no hace nada. |
| CA-24 | `R` reinicia: jugador en `(0,0)`, sin fantasma, sin marcas de búsqueda, turno 1, y un laberinto nuevo elegido al azar. |

- Cada requisito funcional adicional a los CA originales se verifica con prueba automatizada
  si es lógica, o revisión visual/funcional documentada si es presentación.
- La implementación cumple pruebas primero, lógica sin pygame y al menos 80 % de cobertura
  por cada módulo de lógica, incluso cuando el comando original solo comprueba el total.

## Dependencias y supuestos

- [001-modelo-laberintos](../001-modelo-laberintos/spec.md).
- [002-generar-elegir-laberintos](../002-generar-elegir-laberintos/spec.md).
- [003-dados-reproducibles](../003-dados-reproducibles/spec.md).
- [004-busqueda-con-traza](../004-busqueda-con-traza/spec.md).

La lógica conserva los estados de §11. El acoplamiento temporal con reproducción y dados se valida por integración sin ventana.

## Referencia y límites de esta división

Los contratos y valores numéricos originales de las secciones referenciadas se mantienen.
La arquitectura de §12 es orientación para la planificación, no nuevas funciones del producto.
Los archivos de base son material de referencia y no se modifican en esta fase.
Las contradicciones señaladas requieren decisión antes de planificar el aspecto afectado.
Las mejoras futuras de §15 y alternativas descartadas de §8.6 permanecen fuera de alcance.

### Extractos originales de referencia


> ### 5.2 Fantasma
> - **Forma:** cuerpo morado de 30 × 32 px centrado en la casilla: semicírculo superior (cabeza) + rectángulo + borde inferior ondulado de 3 picos. Dos ojos blancos con pupilas que **miran hacia la dirección de su último paso**.
> - **Aparición:** **no existe** al inicio. Aparece cuando termina el **primer turno del jugador**, en una **casilla elegida al azar** (uniforme) entre todas las casillas del tablero, **excepto**:
>   - toda casilla a **menos de 6 pasos** del jugador, medidos por el camino del laberinto (no en línea recta). Esto incluye la casilla del jugador y evita que lo atrape en la primera tirada sin opción de reaccionar. La constante es `DISTANCIA_MIN_FANTASMA = 6` en `config.py`;
>   - la meta `(14,14)` (si el fantasma se quedara ahí, el jugador no podría ganar).
> - La distancia se calcula con un recorrido en anchura (BFS) desde el jugador. Las casillas válidas son las de distancia ≥ 6, sin la meta. En un laberinto perfecto de 225 casillas siempre existen casillas válidas.
> - Al aparecer se muestra durante 1 s el mensaje "¡Apareció el fantasma!" con un destello en su casilla. Luego juega su primer turno.
> - **Control:** automático (IA con backtracking, sección 7).

> ## 6. Reglas del juego
>
> ### 6.1 Flujo de una partida
> 1. El jugador está en la entrada; el fantasma aún no aparece.
> 2. **Turno del jugador:** pulsa `ESPACIO` para tirar el dado → obtiene `d ∈ {1..6}`.
> 3. El jugador mueve su personaje paso a paso con las flechas. Cada paso válido descuenta 1 de los pasos restantes.
> 4. El turno termina cuando los pasos restantes llegan a 0 **o** cuando el jugador pulsa `ENTER`.
> 5. Si era el primer turno del jugador, **aparece el fantasma** en una casilla al azar (5.2).
> 6. **Turno del fantasma:** tira el dado, busca al jugador con backtracking (mostrado en el visualizador) y avanza.
> 7. Se repite desde el paso 2 hasta que haya victoria o derrota.
>
> ### 6.2 Reglas de movimiento del jugador
> - **RJ-1** Solo puede moverse a una casilla vecina sin pared de por medio. Un intento contra una pared se ignora y **no** descuenta pasos.
> - **RJ-2** Puede usar **entre 0 y `d`** pasos. Termina su turno antes de tiempo con `ENTER` (solo después de tirar el dado). Puede devolverse y pisar casillas ya visitadas.
> - **RJ-3** No puede salir del tablero, salvo por la meta, que termina la partida.
> - **RJ-4** Si llega a la **meta** aunque le sobren pasos → **gana inmediatamente**.
> - **RJ-5** Si entra a la casilla donde está el fantasma → **pierde inmediatamente** (captura).
>
> ### 6.3 Reglas de movimiento del fantasma
> - **RF-1** El fantasma tira el dado y obtiene `d ∈ {1..6}`.
> - **RF-2** Calcula, con backtracking, el camino desde su casilla hasta la casilla **actual** del jugador. La búsqueda se anima en el visualizador (sección 8) antes de moverse.
> - **RF-3** Avanza `min(d, longitud_del_camino)` pasos por ese camino, un paso cada `0.25 s` (animado). El fantasma siempre usa todos sus pasos disponibles.
> - **RF-4** Si en cualquiera de sus pasos entra a la casilla del jugador → **captura → GAME OVER**, aunque le sobren puntos del dado.
> - **RF-5** El fantasma respeta las paredes igual que el jugador (no las atraviesa).
>
> ### 6.4 Captura y cruce (decisión confirmada)
> - Los actores se mueven **por turnos**: mientras uno se mueve, el otro está quieto.
> - **Cruzarse cuenta como captura.** Como el otro actor está quieto, cruzarse equivale a que el actor que se mueve **pase por** la casilla del otro en cualquier paso, no solo en el último. Ejemplo: el fantasma saca 6, el jugador está a 2 casillas → captura en el paso 2.
> - Esto aplica en los dos sentidos: RJ-5 (el jugador se mete al fantasma) y RF-4 (el fantasma alcanza al jugador).
> - La comprobación se hace **después de cada paso individual**, no al final del turno.
>
> ### 6.5 Condiciones de fin
> | Resultado | Condición | Mensaje |
> |---|---|---|
> | Victoria | El jugador entra a la casilla meta `(14,14)` | **"¡HAS GANADO!"** + "Llegaste a la meta en X turnos" |
> | Derrota | Captura (6.4) | **"GAME OVER"** + "El fantasma te atrapó" |
>
> En ambas pantallas: `R` = jugar de nuevo (**nuevo laberinto al azar**, sección 4.3), `M` = volver al menú, `ESC` = salir.

> ## 11. Máquina de estados
>
> ```
> INICIO --ENTER (elige/genera laberinto al azar)--> JUGADOR_TIRAR
> JUGADOR_TIRAR --ESPACIO--> DADO_JUGADOR (0.6 s) --> JUGADOR_MOVER
> JUGADOR_MOVER --llega a meta--> VICTORIA
> JUGADOR_MOVER --entra a la casilla del fantasma--> DERROTA
> JUGADOR_MOVER --pasos=0 o ENTER, turno 1--> APARECE_FANTASMA (1 s) --> DADO_FANTASMA
> JUGADOR_MOVER --pasos=0 o ENTER, turno>1--> DADO_FANTASMA
> DADO_FANTASMA (0.6 s) --> FANTASMA_BUSCA
> FANTASMA_BUSCA (animación de la traza; S la salta) --> FANTASMA_MOVER
> FANTASMA_MOVER (0.25 s/paso) --alcanza al jugador--> DERROTA
> FANTASMA_MOVER --termina pasos--> JUGADOR_TIRAR (turno + 1)
> VICTORIA / DERROTA --R (nuevo laberinto al azar)--> JUGADOR_TIRAR | --M o ESC--> INICIO
> (cualquier estado de partida) --ESC--> INICIO
> INICIO --ESC--> salir
> (cualquier estado) --cerrar ventana--> salir
> ```
