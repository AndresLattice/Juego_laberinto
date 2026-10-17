# Guía de validación futura: 001

Esta guía se ejecutará después de implementar; laberinto.py y las pruebas todavía no existen.
No describe comandos ya ejecutados ni resultados del producto acreditados en esta fase.

## Preparación

Desde la raíz del checkout existente /workspace/juego-backtracking (o su ruta local):

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
```

En Windows activar con `.venv\Scripts\Activate.ps1`. Requisitos: Python 3.10+ y las
herramientas de desarrollo declaradas al implementar. No hace falta instalar pygame ni abrir
una ventana para esta funcionalidad. Usar el checkout existente; no crear un worktree.

## Ciclo de pruebas primero

Para cada comportamiento, añadir primero la prueba y observar su fallo por la capacidad
faltante. Escribir después el código mínimo y refactorizar con pruebas en verde. Guardar
la evidencia de ese ciclo en la entrega de implementación.

```bash
python -m pytest tests/test_laberinto.py -q
python -m pytest tests/test_laberinto.py --cov=laberinto --cov-report=term-missing --cov-fail-under=80
```

La primera ejecución durante TDD debe fallar por el comportamiento ausente; la final debe
terminar con todas las pruebas pasando y cobertura de laberinto al menos 80 %. No aceptar
cero pruebas. Al existir otros módulos lógicos se medirá el mínimo por cada uno, no solo total.

## Escenarios verificables

1. Cargar base/laberintos.json: cinco entradas; comprobar los datos originales preservados
   y dimensiones. Consultar todos los vecinos de las 1 125 casillas contra paredes de la fuente.
2. Crear archivos temporales vacíos, JSON inválido, UTF-8 inválido, estructura distinta de lista,
   entradas no diccionario y mezcla de válidas/invalidas. Simular OSError para el archivo
   ilegible. Esperar resultado controlado; conservar todas las válidas en orden.
3. Mutar copias de grids: dimensión, carácter, centro cerrado, ciclo y desconexión. Exigir rechazo;
   probar conectividad independientemente del conteo para evitar validar solo 224 conexiones.
4. En un tablero de interior válido, cerrar por separado cada apertura obligatoria y abrir por
   separado cada otra posición del contorno, incluidas esquinas. Cada variante debe rechazarse.
5. Probar paredes simétricas y rechazar coordenadas fuera de dominio, diagonales, igualdad y
   no adyacentes. Las dos aperturas exteriores no deben devolver vecinos exteriores.
6. Para cada origen de los cinco tableros, comparar las 225 distancias con un recorrido de
   referencia independiente en tests. Añadir un tablero serpenteante con distancias conocidas
   y una ruta que alcance 224 pasos; no usar la función de producción como oráculo.
7. Repetir consultas, modificar sus listas/diccionarios y las copias de datos del catálogo:
   comprobar que no se altera el modelo ni resultados anteriores ni el archivo base.
8. Ejecutar las pruebas de lógica en un proceso sin pygame instalado y sin inicializar pantalla.
   Revisar imports para evitar dependencias gráficas indirectas.

## Ejecución del juego completo cuando 008 esté implementada

Las condiciones confirmadas son Python 3.10+, pygame 2.x y ventana 920×740.
Los comandos previstos desde la carpeta de main.py son:

```bash
python -m pip install -r requirements.txt
python main.py
```

requirements.txt solo requiere pygame>=2,<3 como dependencia externa del juego.
pytest y pytest-cov pertenecen a requirements-dev.txt y no son necesarios para jugar.
No se construye un ejecutable ni un paquete de distribución. El cargador recibe la ruta
resuelta de laberintos.json; el catálogo actual de pruebas sigue en base/laberintos.json.
El modo generado usará backtracking con pila explícita de 002. La vista 007 y la integración
008 comprobarán la ventana de 920×740; esas capacidades no se acreditan con pruebas de 001.

Estos comandos no son ejecutables todavía: no existen main.py ni la interfaz del juego.
La validación presente del plan es documental.

## Cierre

Usar la matriz de [plan.md](plan.md) para acreditar CE-01 a CE-06. Adjuntar resultados reales
y cobertura. CA-27 con buscar_camino queda pendiente de integración con 004 y debe reportarse
como tal. No declarar completado ese criterio integrado antes de ejecutarlo.

Antes de una nueva fase: revisar Git y sincronizar sin perder trabajo. Al terminar: commit y
push de la fase, sin forzar. No ejecutar planes de 002 ni crear código gráfico como parte de 001.
