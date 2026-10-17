# Constitución de juego-backtracking

## Core Principles

### I. Lógica independiente de la interfaz

Los módulos de lógica del juego NUNCA DEBEN importar pygame, directa ni indirectamente.
La interfaz puede depender de la lógica; la lógica NO DEBE depender de la interfaz.
Todas las pruebas de lógica DEBEN ejecutarse sin abrir ventanas ni inicializar pygame.
Esta separación permite comprobar el comportamiento en un entorno sin pantalla.

### II. Pruebas antes que implementación

Para cada comportamiento nuevo o corregido se DEBE escribir primero una prueba,
ejecutarla y comprobar que falla por el comportamiento aún no implementado.
Solo después se DEBE escribir el código mínimo que la haga pasar y refactorizar
manteniendo las pruebas en verde. NO SE DEBE omitir el ciclo de fallo, éxito y refactorización.

### III. Cobertura mínima de la lógica

Cada módulo de lógica DEBE alcanzar al menos un 80 % de cobertura de líneas ejecutables.
La medición DEBE incluir todos los módulos de lógica, también los que ninguna prueba importe.
Una cobertura global alta NO compensa un módulo por debajo del umbral.
NO SE DEBEN excluir líneas o módulos para eludir este requisito.
El informe de cobertura DEBE acompañar la validación de cada entrega que cambie la lógica.

### IV. Python y dependencia única del juego

El juego DEBE implementarse en Python y pygame DEBE ser su única dependencia externa
necesaria para ejecutarlo. La biblioteca estándar se puede usar libremente.
Las herramientas de pruebas y medición de cobertura DEBEN declararse por separado como
herramientas de desarrollo y NO DEBEN ser necesarias para ejecutar el juego.

### V. Español en textos y código

Los textos visibles, documentación propia, comentarios y nombres de variables, funciones,
clases y módulos del proyecto DEBEN estar en español.
Se permiten los nombres exigidos por Python, pygame y otras interfaces externas,
así como rutas y convenciones de las herramientas instaladas.

### VI. La solución más simple que cumpla la especificación

Se DEBE implementar la solución más simple que satisfaga la especificación vigente.
NO SE DEBEN añadir funcionalidades, dependencias ni abstracciones para necesidades hipotéticas.
Cada decisión de complejidad adicional DEBE justificarse mediante un requisito concreto.

### VII. Terminado significa aceptación completa

Una funcionalidad solo se DEBE declarar terminada cuando TODOS sus criterios de aceptación
hayan sido verificados y pasen, junto con las pruebas pertinentes y el umbral de cobertura.
Los criterios fallidos, omitidos o pendientes impiden declarar la funcionalidad terminada.
Se DEBE conservar evidencia de los resultados y su relación con los criterios de aceptación.

## Restricciones técnicas y validación

El producto es un juego educativo de laberintos y backtracking en Python.
Las reglas y algoritmos DEBEN poder ejercitarse mediante datos y resultados sin interfaz gráfica.
Las pruebas de interfaz, cuando correspondan a criterios de aceptación, DEBEN validarse
por separado sin introducir dependencias de pygame en los módulos de lógica.
La elección de herramientas de desarrollo DEBE respetar la dependencia única de ejecución.

## Flujo de desarrollo y sincronización

Antes de iniciar una especificación o una fase de Spec Kit se DEBE revisar el estado de Git,
consultar los cambios remotos y sincronizar el repositorio sin perder trabajo local.
Si hay cambios pendientes de una fase anterior, se DEBEN revisar, registrar en un commit y
subir antes de iniciar la siguiente. NO SE DEBE iniciar una especificación con trabajo pendiente
sin commit o con commits locales sin sincronizar con el repositorio remoto.
Si no hay cambios, NO es necesario crear un commit vacío.

Al terminar CADA fase de Spec Kit, incluida la constitución, se DEBEN validar sus artefactos,
crear un commit descriptivo en español y subir los cambios al repositorio.
Un fallo de sincronización o de push DEBE resolverse antes de iniciar la fase siguiente;
NO SE DEBE forzar la subida ni descartar cambios para eludirlo.
La autorización de commit y push se mantiene para las fases posteriores solicitadas.
Completar una fase NO autoriza iniciar automáticamente una fase que no se haya solicitado.

Durante la implementación se DEBE seguir el ciclo de pruebas primero y comprobar todos
los criterios de aceptación antes de declarar terminada la funcionalidad.

## Governance

Esta constitución rige las especificaciones, planes, tareas, implementación y revisiones.
Cada fase DEBE comprobar el cumplimiento de los principios que le correspondan.
Un requisito contradictorio DEBE resolverse mediante una enmienda explícita aprobada
por el responsable del proyecto antes de implementar la excepción.

Las enmiendas DEBEN documentar el motivo, los principios afectados y las consecuencias
para los artefactos existentes. Se DEBE aumentar la versión mayor al eliminar o redefinir
reglas de forma incompatible; la menor al añadir principios o ampliar obligaciones;
y la de parche al aclarar redacción sin cambiar las obligaciones.
Cada enmienda DEBE actualizar la fecha, validarse y registrarse mediante commit y push.

**Version**: 1.0.0 | **Ratified**: 2026-10-17 | **Last Amended**: 2026-10-17
