from abc import ABC, abstractmethod

class EstrategiaAtaque(ABC):
    @abstractmethod
    def ejecutar(self, atacante, defensor):
        pass

class AtaqueNormal(EstrategiaAtaque):
    def ejecutar(self, atacante, defensor):
        dano = atacante.ataque
        defensor.recibir_dano(dano)
        print(f"⚔️ {atacante.nombre} usa ATAQUE NORMAL y causa {dano} de daño!")

class AtaqueFuerte(EstrategiaAtaque):
    def ejecutar(self, atacante, defensor):
        dano = int(atacante.ataque * 1.5) 
        defensor.recibir_dano(dano)
        print(f"🔥 {atacante.nombre} usa ATAQUE FUERTE y causa {dano} de daño!")