from abc import ABC, abstractmethod
from personajes import Guerrero, Dragon, Soldado, Alien


class PersonajeFactory:
    @staticmethod
    def crear(tipo):
        tipo = tipo.lower()
        if tipo == "guerrero": return Guerrero()
        if tipo == "dragon": return Dragon()
        if tipo == "soldado": return Soldado()
        if tipo == "alien": return Alien()
        raise ValueError(f"Personaje de tipo '{tipo}' desconocido.")


class MundoFactory(ABC):
    @abstractmethod
    def crear_jugador(self): pass
    
    @abstractmethod
    def crear_enemigo(self): pass

class FantasyFactory(MundoFactory):
    def crear_jugador(self): return PersonajeFactory.crear("guerrero")
    def crear_enemigo(self): return PersonajeFactory.crear("dragon")

class SciFiFactory(MundoFactory):
    def crear_jugador(self): return PersonajeFactory.crear("soldado")
    def crear_enemigo(self): return PersonajeFactory.crear("alien")