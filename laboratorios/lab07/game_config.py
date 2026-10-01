class GameConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameConfig, cls).__new__(cls)
            cls._instance.dificultad = "Normal"
            cls._instance.numero_maximo_turnos = 50
        return cls._instance
        