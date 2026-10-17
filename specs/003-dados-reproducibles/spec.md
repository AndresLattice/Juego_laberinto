# Especificación: Tirar dados y reproducir partidas

**Identificador**: 003-dados-reproducibles
**Creada**: 2026-10-17
**Estado**: Descompuesta para revisión; no implementada.
**Fuente**: [SPEC-LAB-001 v1.3](../../base/SPEC.md), idéntica al adjunto analizado.
**Gobierno**: [Constitución 1.0.0](../../.specify/memory/constitution.md).

## Escenarios de usuario y pruebas

### Historia 1 — Tirar dados y reproducir partidas (prioridad P1)

Como jugador o docente quiero tiradas válidas y partidas reproducibles para repetir y explicar una sesión.

**Valor**: entregar esta capacidad sin asumir que la interfaz y el juego completos ya existen.
**Prueba independiente**: ejecutar los escenarios siguientes con entradas controladas y dobles de
las dependencias; para la vista, una demostración visual aislada. Las pruebas integradas se
realizan cuando estén disponibles los consumidores correspondientes.

1. Dada una tirada, cuando se resuelve, entonces entrega un entero de 1 a 6 y la cara final no cambia después de mostrarse.
2. Dada la misma semilla y la misma secuencia de acciones, cuando repito la partida cambiando la cantidad de cuadros de animación, entonces obtengo el mismo laberinto, dados y aparición.

### Casos límite

- Tirada pendiente y acciones repetidas durante la animación.
- Actualizaciones de tiempo de distinto tamaño no deben consumir azar lógico adicional.
- La repetibilidad exige las mismas acciones y opciones; no se comparan partidas con decisiones distintas.

## Requisitos

### Requisitos funcionales

- **RF-01**: Se DEBE producir cada cara con igual probabilidad y permitir inyectar la fuente aleatoria lógica.
- **RF-02**: Se DEBE mantener la última tirada de cada actor por separado.
- **RF-03**: Se DEBE exponer la animación de 0,6 s con caras visuales nuevas cada 0,06 s y después fijar el resultado lógico.
- **RF-04**: Se DEBE compartir una sola fuente aleatoria de lógica entre selección/generación, dados y aparición; usar una fuente aparte para las caras visuales.
- **RF-05**: Se DEBE la semilla opcional controla la lógica; sin ella la partida recibe una semilla aleatoria.

### Entidades

Dado, resultado, animación y fuente aleatoria lógica/visual.

### Fuera de alcance

No representa puntos del dado ni interpreta argumentos del programa. La comprobación integrada de CA-16 requiere 002, 005 y 008.

## Criterios de éxito

- Todos los escenarios y requisitos anteriores tienen una comprobación que pasa antes de
  declarar implementada esta funcionalidad; esta descomposición no afirma que ya pasen.
- Se conservan los siguientes criterios originales, sin renumerarlos:

| ID | Criterio original |
|---|---|
| CA-06 | 10 000 tiradas de `Dado` producen solo valores en `1..6` y aparecen las 6 caras. |
| CA-16 | Con la misma `--semilla`, la secuencia de dados y la casilla de aparición del fantasma son idénticas. |

- Cada requisito funcional adicional a los CA originales se verifica con prueba automatizada
  si es lógica, o revisión visual/funcional documentada si es presentación.
- La implementación cumple pruebas primero, lógica sin pygame y al menos 80 % de cobertura
  por cada módulo de lógica, incluso cuando el comando original solo comprueba el total.

## Dependencias y supuestos

- No requiere implementar otras especificaciones para validar su contrato.

Las dependencias de integración no impiden probar tiradas y separación del azar mediante consumidores simulados.

## Referencia y límites de esta división

Los contratos y valores numéricos originales de las secciones referenciadas se mantienen.
La arquitectura de §12 es orientación para la planificación, no nuevas funciones del producto.
Los archivos de base son material de referencia y no se modifican en esta fase.
Las contradicciones señaladas requieren decisión antes de planificar el aspecto afectado.
Las mejoras futuras de §15 y alternativas descartadas de §8.6 permanecen fuera de alcance.

### Extractos originales de referencia


> ## 9. El dado
>
> - **D-1** Valores enteros uniformes en `1..6` (`random.randint(1, 6)`).
> - **D-2** Se dibuja en el panel inferior: cuadrado blanco de 60 × 60 px con borde negro de 3 px y puntos negros según la cara.
> - **D-3** Animación de tirada: durante `0.6 s` se muestran caras aleatorias cambiando cada `0.06 s`; luego se fija el valor.
> - **D-4** Hay un dado por actor, con la etiqueta "Jugador" o "Fantasma", para que se vea la última tirada de cada uno.
> - **D-5** Se puede pasar una semilla por línea de comandos (`--semilla 123`) para partidas reproducibles (necesario para pruebas). La misma semilla controla el laberinto elegido o generado, los dados y la casilla de aparición del fantasma. Hay un único `random.Random(semilla)` compartido para la lógica; sin semilla se usa una aleatoria.
> - **D-6** Las caras que giran durante la animación (D-3) son solo visuales y salen de un **generador aparte** (`random.Random()` sin semilla). Nunca consumen números del generador de la lógica, así que la animación no cambia los resultados de una partida con semilla.
