import copy




class Computadora:
    def __init__(self):
        self.cpu=None
        self.disco= None
        self.ram =None
        self.gpu = None
        self.wifi=None
    

    def mostrar(self):
        print('CPU: ' , self.cpu)
        print('RAM: ' , self.ram)
        print('GPU: ' , self.gpu)
        print('DISCO: ', self.disco)
        print('Wifi:', self.wifi)
    def clonar(self)-> 'Computadora':
        return copy.deepcopy(self)


class ComputadoraBuilder:
    def __init__(self):
        self.computadora = Computadora()
    def addCPU(self, cpu):
        self.computadora.cpu = cpu
        return self
    def addDisco(self, disco):
        self.computadora.disco=disco
        return self
    def addRam(self, ram):
        self.computadora.ram=ram
        return self
    def addGPU(self, gpu):
        self.computadora.gpu=gpu
        return self
    def addWifi(self, wifi):
        self.computadora.wifi=wifi
        return self
    def build(self):
        return self.computadora

def main():
    pc_builder= ComputadoraBuilder()

    pc_builder= pc_builder.addRam(4).addGPU(18)

    pc_gaming = pc_builder.addDisco(1).addCPU(20).addWifi('5G').build()

    pc_gaming.mostrar()

    pc_work = pc_gaming.clonar()

    pc_work.ram=64

    pc_work.mostrar()


main()

