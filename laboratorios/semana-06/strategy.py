from abc import abstractmethod, ABC

class EstrategiaDescuento(ABC):
    @abstractmethod
    def aplicar(self, precioBase):
        pass

class SinDescuento(EstrategiaDescuento):
    def aplicar(self, precioBase):
        return precioBase

class DescuentoVip(EstrategiaDescuento):
    def aplicar(self,precioBase):
        return precioBase*0.80

class DescuentoEstudiante(EstrategiaDescuento):
    def aplicar(self, precioBase):
        return precioBase*0.05
class DescuentoEmpleado(EstrategiaDescuento):
    def aplicar(self,precioBase):
        return precioBase*0.25

class Compra:
    def __init__(self,estrategiaDescuento):
        self.estrategiaDescuento =estrategiaDescuento

    def calcularTotal(self, precio):
        return self.estrategiaDescuento.aplicar(precio)



def main():
    estudDescuento = DescuentoEstudiante()
    VipDescuento= DescuentoVip()
    sinDescuento= SinDescuento()
    empDescuento= DescuentoEmpleado()
    compra2=Compra(estudDescuento)
    compra3= Compra(VipDescuento)
    compra1= Compra(sinDescuento)
    compra4 = Compra(empDescuento)
    print(compra1.calcularTotal(100))
    print(compra3.calcularTotal(1000))
    print(compra2.calcularTotal(10))
    print(compra4.calcularTotal(100))

main()