"""Reproduce la traza del backtracking en el tiempo, sin dibujar."""


class ReproductorTraza:
    def __init__(self):
        self.velocidad = 1
        self.limpiar()

    def limpiar(self):
        self.traza = []
        self.indice = 0
        self.tiempo = 0
        self.intervalo = 0
        self.pausado = False
        self.evento_actual = None
        self.pila_visible = ()
        self.estados = {}
        self.apilados = 0
        self.retrocesos = 0
        self.profundidad = 0
        self.maximo = 0

    def cargar(self, traza):
        self.limpiar()
        self.traza = traza
        self.intervalo = max(0.03, 4 / len(traza))

    @property
    def esperando(self):
        return len(self.traza) == 0

    @property
    def terminado(self):
        return not self.esperando and self.indice == len(self.traza)

    @property
    def camino(self):
        if not self.terminado:
            return []
        return list(self.pila_visible[1:])

    def estado_casilla(self, casilla):
        return self.estados.get(casilla)

    def _consumir(self):
        evento = self.traza[self.indice]
        self.indice += 1
        self.evento_actual = evento
        self.pila_visible = evento.pila
        if evento.tipo == "apilar":
            self.estados[evento.casilla] = "en_pila"
            self.apilados += 1
        elif evento.tipo == "desapilar":
            self.estados[evento.casilla] = "descartada"
            self.retrocesos += 1
        self.profundidad = len(evento.pila)
        if self.profundidad > self.maximo:
            self.maximo = self.profundidad

    def actualizar(self, segundos):
        if self.esperando or self.pausado:
            return
        self.tiempo += segundos * self.velocidad
        # Puede tocar más de un evento si el cuadro fue largo.
        while self.tiempo >= self.intervalo and not self.terminado:
            self.tiempo -= self.intervalo
            self._consumir()

    def pausar(self):
        self.pausado = not self.pausado

    def paso(self):
        if self.pausado and not self.esperando and not self.terminado:
            self._consumir()

    def saltar(self):
        while not self.esperando and not self.terminado:
            self._consumir()

    def mas_rapido(self):
        if self.velocidad < 4:
            self.velocidad = self.velocidad * 2

    def mas_lento(self):
        if self.velocidad > 0.25:
            self.velocidad = self.velocidad / 2
