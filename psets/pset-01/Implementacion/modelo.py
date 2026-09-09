
from datetime import datetime, time


class ReglaPrioridad:
    def tiene_prioridad(self, hora_reserva: time) -> bool:
        raise NotImplementedError("Las subclases deben implementar este método")

class PrioridadAntesDeLas6(ReglaPrioridad):
    def tiene_prioridad(self, hora_reserva: time) -> bool:
        return hora_reserva < time(18, 0)

class SinPrioridad(ReglaPrioridad):
    def tiene_prioridad(self, hora_reserva: time) -> bool:
        return False

# Entidades
class Solicitante:
    def __init__(self, nombre: str, regla_prioridad: ReglaPrioridad):
        self.nombre = nombre
        self.regla_prioridad = regla_prioridad

    def verificar_prioridad(self, hora_reserva: time) -> bool:
        return self.regla_prioridad.tiene_prioridad(hora_reserva)

class Estudiante(Solicitante):
    def __init__(self, nombre: str):
        super().__init__(nombre, SinPrioridad())

class CapitanEquipo(Solicitante):
    def __init__(self, nombre: str):
        super().__init__(nombre, PrioridadAntesDeLas6())

class Administrador:
    def __init__(self, nombre: str):
        self.nombre = nombre

class Cancha:
    def __init__(self, id_cancha: str):
        self.id_cancha = id_cancha

class Reserva:
    def __init__(self, cancha: Cancha, solicitante: Solicitante, fecha_hora_inicio: datetime):
        self.cancha = cancha
        self.solicitante = solicitante
        self.fecha_hora_inicio = fecha_hora_inicio
        self.estado = "activa"

    def procesar_cancelacion(self, hora_actual: datetime):
        diferencia = self.fecha_hora_inicio - hora_actual
        if diferencia.total_seconds() < 7200: # Menos de 2 horas
            self.estado = "no-show"
            return "no-show"
        else:
            self.estado = "cancelada"
            return "cancelada"

class Conflicto:
    def __init__(self, nuevo_solicitante: Solicitante, reserva_existente: Reserva, fecha_hora: datetime):
        self.nuevo_solicitante = nuevo_solicitante
        self.reserva_existente = reserva_existente
        self.fecha_hora = fecha_hora
        self.estado = "pendiente"

class SistemaReservaU:
    def __init__(self):
        self.canchas = []
        self.reservas = []
        self.conflictos = []

    def gestionar_cancha(self, operacion: str, cancha: Cancha):
        print("1. El administrador indica la operación sobre el catálogo (agregar o retirar una cancha).")
        if operacion == "agregar":
            self.canchas.append(cancha)
            print("2. El sistema aplica el cambio al catálogo.")
            print("3. El sistema confirma la actualización.")

    def reservar_cancha(self, solicitante: Solicitante, cancha: Cancha, fecha_hora: datetime):
        print("1. El solicitante indica la cancha y el horario deseado.")
        print("2. El sistema verifica si la cancha está disponible en ese horario.")
        
        reserva_existente = next((r for r in self.reservas if r.cancha == cancha and r.fecha_hora_inicio == fecha_hora and r.estado == "activa"), None)
        
        if not reserva_existente:
            print("3. El sistema crea la reserva para el solicitante.")
            nueva_reserva = Reserva(cancha, solicitante, fecha_hora)
            self.reservas.append(nueva_reserva)
            print("4. El sistema confirma la reserva.")
            return nueva_reserva
        else:
            hora = fecha_hora.time()
            if solicitante.verificar_prioridad(hora) and not reserva_existente.solicitante.verificar_prioridad(hora):
                print("2b. La cancha está ocupada por un solicitante sin prioridad, y el nuevo solicitante sí tiene prioridad para ese horario.")
                print("El sistema registra un CONFLICTO en lugar de confirmar de inmediato.")
                nuevo_conflicto = Conflicto(solicitante, reserva_existente, fecha_hora)
                self.conflictos.append(nuevo_conflicto)
            else:
                print("2a. La cancha no está disponible y el solicitante no tiene prioridad para ese horario.")
                print("El sistema informa que no hay disponibilidad; termina el caso de uso.")
            return None

    def cancelar_reserva(self, reserva: Reserva, hora_actual: datetime):
        print("1. El solicitante pide cancelar su reserva.")
        print("2. El sistema calcula el tiempo restante hasta el inicio de la reserva.")
        
        resultado = reserva.procesar_cancelacion(hora_actual)
        if resultado == "cancelada":
            print("3. El sistema determina que quedan 2 horas o más.")
            print("4. El sistema marca la reserva como cancelada.")
            print("5. El sistema confirma la cancelación.")
        else:
            print("3a. Quedan menos de 2 horas -> el sistema marca la reserva como no-show en vez de cancelada, y confirma.")

    def intervenir_conflicto(self):
        print("1. El administrador revisa el conflicto pendiente.")
        if not self.conflictos:
            return
            
        conflicto = self.conflictos.pop(0)
        nuevo_sol = conflicto.nuevo_solicitante
        res_existente = conflicto.reserva_existente
        hora = conflicto.fecha_hora.time()
        
        print("2. El sistema compara la regla de prioridad de ambos solicitantes para el horario en conflicto.")
        pri_nuevo = nuevo_sol.verificar_prioridad(hora)
        pri_existente = res_existente.solicitante.verificar_prioridad(hora)
        
        print("3. El sistema determina el solicitante ganador.")
        if pri_nuevo and not pri_existente:
            print("4. El sistema cancela la reserva del solicitante sin prioridad y confirma la del ganador.")
            res_existente.estado = "cancelada"
            nueva_reserva = Reserva(res_existente.cancha, nuevo_sol, conflicto.fecha_hora)
            self.reservas.append(nueva_reserva)
            conflicto.estado = "resuelto"
            print("5. El sistema marca el conflicto como resuelto.")

            