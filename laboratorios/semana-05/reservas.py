
class Estudiante:
    def __init__(self, nombre):
        self.nombre = nombre

class EquipoOficial:
    def __init__(self,nombre):
        self.nombre=nombre

class ReservaRegular:
    def __init__(self, cancha,fecha, hora_inicio, hora_fin , solicitante):
        self.cancha =cancha
        self.fecha =fecha;
        self.horar_inicio =hora_inicio    
        self.hora_fin = hora_fin    
        self.solicitante=solicitante

    def confirmar(self):
        return "Reserva confirmada para " + self.solicitante

class ReservaPrioridad:
    def __init__(self, cancha,fecha, hora_inicio, hora_fin , solicitante):
        self.cancha =cancha
        self.fecha =fecha;
        self.horar_inicio =hora_inicio    
        self.hora_fin = hora_fin    
        self.solicitante=solicitante
    
    def confirmar(self):
        return "Reserva con prioridad confirmada para " + self.solicitante


def reservar_desde_web(solicitantes):
    if isinstance(solicitantes, EquipoOficial):
        reserva =ReservaRegular

    pass

def reservar_desde_hall():
    pass