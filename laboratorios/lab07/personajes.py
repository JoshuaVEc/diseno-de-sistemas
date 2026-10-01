from Strategy import AtaqueNormal

class Personaje:
    def __init__(self, nombre, vida, ataque):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.estrategia = AtaqueNormal() 

    def set_estrategia(self, estrategia):
        self.estrategia = estrategia

    def atacar(self, enemigo):
        self.estrategia.ejecutar(self, enemigo)

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    def esta_vivo(self):
        return self.vida > 0

class Guerrero(Personaje):
    def __init__(self): super().__init__("Guerrero", 100, 15)

class Dragon(Personaje):
    def __init__(self): super().__init__("Dragón", 150, 20)

class Soldado(Personaje):
    def __init__(self): super().__init__("Soldado", 120, 18)

class Alien(Personaje):
    def __init__(self): super().__init__("Alien", 140, 22)