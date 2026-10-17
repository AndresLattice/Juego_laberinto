# Investigación y decisiones: modelo de laberintos

**Fecha**: 2026-10-17. Investigación basada en código/datos del repositorio y biblioteca
estándar; sin servicios externos necesarios. No se implementa el módulo en esta fase.

## 1. Representación y ausencia de mutaciones

**Decisión**: representar Laberinto como valor inmutable con grid de tupla de cadenas.
Mantener los metadatos del catálogo en una entrada separada que conserva una copia profunda
del registro y entrega copias al consumidor. Los vecinos y distancias devuelven resultados nuevos.
**Motivo**: el grid ya describe todas las conexiones; duplicarlo en otro grafo añade riesgo
de inconsistencias. frozen=True por sí solo no hace inmutables listas o diccionarios anidados.
**Alternativas**: listas compartidas (rechazadas por RF-10); grafo duplicado y caché global
(rechazados por complejidad y mutación); validar metadatos con un esquema externo (innecesario).

## 2. Validación como grafo de casillas

**Decisión**: comprobar forma y caracteres antes de indexar; 225 centros abiertos; contorno
con exactamente las dos aperturas aprobadas; 224 conexiones internas contadas hacia derecha
y abajo una vez; recorrer y exigir 225 casillas alcanzables.
**Motivo**: número de conexiones por sí solo no garantiza conectividad. Un grafo conectado
con V−1 conexiones es un árbol y garantiza camino único. Las aperturas no cuentan como aristas.
**Alternativas**: solo contar conexiones (insuficiente); union-find (válido pero añade una
estructura cuando ya se necesita recorrer vecinos). No imponer validación nueva a posiciones
interiores decorativas que no son centros ni separadores: la fuente no la exige.

## 3. Distancias

**Decisión**: recorrido en anchura con deque desde un origen válido, sin aleatoriedad.
Vecinos en orden arriba, derecha, abajo, izquierda, compatible con el consumidor 004.
**Motivo**: calcula distancias de pasos sin introducir pygame ni implementar la persecución.
**Alternativas**: distancia geométrica (incorrecta ante paredes); llamar a la futura IA
(crea dependencia innecesaria); resolver un camino por destino (repite trabajo).

## 4. Errores y carga parcial

**Decisión**: construcción/consulta inválida lanza ValueError en español. La carga devuelve
ResultadoCarga con entradas válidas, cantidad rechazada y aviso opcional. Atrapar únicamente
errores esperados de lectura, decodificación y validación; no ocultar defectos del programa.
**Motivo**: el consumidor puede aplicar el respaldo sin distinguir excepciones de archivos.
Catálogo parcial utilizable no lleva aviso global de indisponibilidad.
**Alternativas**: sys.exit (prohibido), captura general de Exception (oculta errores), registro
obligatorio o jerarquía propia de excepciones (no necesarios en este alcance).

## 5. Metadatos y coordenadas del archivo

**Decisión**: conservar campos del registro sin añadir unicidad ni restricciones de tipos de
metadatos ajenas a la fuente. La validez del tablero determina la aceptación. Campo grid ausente
o mal formado invalida la entrada. Guardar las etiquetas y coordenadas externas sin reinterpretarlas.
**Evidencia**: las cinco entradas usan id, tipo, descripcion, entrada, salida y grid;
entrada=[1,0], salida=[29,30] son posiciones (fila, columna) del grid, no casillas del juego.
**Alternativa**: interpretar entrada como casilla (columna,fila), descartada por contradicción
con los datos y con entrada lógica (0,0). Las aperturas lógicas se derivan del contrato fijo.

## 6. Estrategia de pruebas y cobertura

**Decisión**: pytest y pytest-cov solo para desarrollo. Usar datos deterministas y archivos
temporales; simular OSError de lectura en vez de depender de chmod o privilegios del ejecutor.
Verificar la cobertura de laberinto explícitamente. Con varios módulos futuros, comprobar
cada uno: un porcentaje agregado no basta.
**Oráculos**: paredes esperadas leídas directamente de la fuente; distancias calculadas por
un recorrido independiente con pila en tests sobre el árbol y un tablero serpenteante de
longitudes conocidas. No importar funciones internas de producción para generar lo esperado.
**Alternativas**: usar la misma función BFS en prueba y producción (puede replicar defectos),
traer pygame para pruebas (viola independencia), lanzar 004 antes de tiempo (fuera de alcance).

## 7. Confirmación del entorno técnico y límites de integración

**Decisión**: adoptar la instrucción explícita del usuario: Python 3.10+, pygame 2.x como
única dependencia del juego, pytest/pytest-cov para desarrollo, ventana 920×740, predefinidos
en laberintos.json, generación mediante backtracking de pila explícita y ejecución con
python main.py sin empaquetado.
**Motivo**: coincide con la fuente y la constitución; completa las condiciones del producto
sin mezclar el modelo de datos con el código gráfico o el generador de 002.
**Alternativas descartadas**: generación por recursión de llamadas, dependencias gráficas
en lógica, ejecutable empaquetado y traslado del catálogo durante una fase documental.
**Ruta de datos**: cargar_catalogo recibe una ruta; base/laberintos.json es la referencia
actual. El punto de entrada de 008 resolverá el archivo relativo a su propia ubicación.

## Resultado

No quedan decisiones técnicas sin resolver para 001. Las decisiones pendientes de 002, 006
y 008 no impiden este plan. La investigación no constituye una medición de la implementación.
