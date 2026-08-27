# Vehiculo -> mueva -> mover()

#Auto -> muever por carretera
#Bote -> mueve por agua
#Avion -> mueve por cielo


class TipoMovilidad:
    def mover(self):
        raise NotImplementedError

class MovilidadCarretera(TipoMovilidad):
    def mover(self):
        print('Conduciendo por Carretera')

class MovilidadAgua(TipoMovilidad):
    def mover(self):
        print('Navegando por agua')

class MovilidadAire(TipoMovilidad):
    def mover(self):
        print('Volando por el aire')

class Vehiculo:
    def __init__(self, TipoMovilidad):
        self.TipoMovilidad = TipoMovilidad

    def mover(self):
        self.TipoMovilidad.mover()

class Carro(Vehiculo):
    def __init__(self):
        conduce_carretera=MovilidadCarretera()
        super().__init__(conduce_carretera)

class Bote(Vehiculo):
    def __init__(self):
        navega_agua= MovilidadAgua()
        super().__init__(navega_agua)

class Avion(Vehiculo):
    def __init__(self):
        vuelva_aire = MovilidadAire()
        super().__init__(vuelva_aire)


if __name__ == "__main__":
    carro = Carro()
    avion = Avion()
    bote = Bote()

    carro.mover()
    avion.mover()
    bote.mover()
    