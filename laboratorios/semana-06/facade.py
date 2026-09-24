
class Inventario:
    def verificar(self,producto):
        print(f"Verificando el stock de {producto}")
        return True

class Pago:
    def procesar(self, monto):
        print(f"Procesando Pago: {monto}")
        return True

class Envio():
    def crearEnvio(self,producto):
        print(f"Preparando el envio del: {producto}")
        

class Notificacion():
    def notificar(self,producto):
        print(f"Se ha comprado: {producto}, exitosamente")

class TiendaFacade:
    def __init__(self):
        self.inventario =Inventario()
        self.envio= Envio()
        self.pago=Pago()
        self.notificacion=Notificacion()
    def comprar(self,producto,precio):
        if not self.inventario.verificar(producto):
            print('No hay stock')
            return

        if not self.pago.procesar(precio):
            print('fallo el pago')
            return
        
        self.envio.crearEnvio(producto)
        self.notificacion.notificar(producto)
        

        

def main():
    tienda= TiendaFacade()

    tienda.comprar('laptop', 1500)


main()
