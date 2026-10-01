from game_config import GameConfig
from factories import FantasyFactory, SciFiFactory
from Strategy import AtaqueNormal, AtaqueFuerte

class GameFacade:
    def __init__(self):
        self.config = GameConfig()
        self.jugador = None
        self.enemigo = None
        self.turno_actual = 1

    def iniciar_juego(self):
        print("=== BIENVENIDO AL JUEGO POR TURNOS ===")
        print("Selecciona un mundo:")
        print("1. Fantasía (Guerrero vs Dragón)")
        print("2. Ciencia Ficción (Soldado vs Alien)")
        
        opcion = input("Elige (1 o 2): ")
        factory = FantasyFactory() if opcion == "1" else SciFiFactory()
        
        self.jugador = factory.crear_jugador()
        self.enemigo = factory.crear_enemigo()
        
        print(f"\n¡Mundo creado! Eres un {self.jugador.nombre} y te enfrentas a un {self.enemigo.nombre}.\n")
        self.ejecutar_combate()

    def ejecutar_combate(self):
        while self.jugador.esta_vivo() and self.enemigo.esta_vivo() and self.turno_actual <= self.config.numero_maximo_turnos:
            print(f"--- TURNO {self.turno_actual} ---")
            print(f"Tu vida: {self.jugador.vida} | Vida enemigo: {self.enemigo.vida}")
            
          
            print("Elige tu ataque: 1. Normal  2. Fuerte")
            ataque = input("Opción (1 o 2): ")
            estrategia = AtaqueNormal() if ataque == "1" else AtaqueFuerte()
            
            self.jugador.set_estrategia(estrategia)
            self.jugador.atacar(self.enemigo)

            
            if self.enemigo.esta_vivo():
                self.enemigo.set_estrategia(AtaqueNormal()) 
                self.enemigo.atacar(self.jugador)
                
            self.turno_actual += 1
            print("-" * 25 + "\n")

        self.determinar_ganador()

    def determinar_ganador(self):
        print("=== FIN DEL JUEGO ===")
        if self.jugador.esta_vivo() and not self.enemigo.esta_vivo():
            print("🏆 ¡HAS GANADO!")
        elif self.enemigo.esta_vivo() and not self.jugador.esta_vivo():
            print("💀 HAS MUERTO. El enemigo gana.")
        else:
            print("⏱️ Límite de turnos alcanzado. ¡Empate!")