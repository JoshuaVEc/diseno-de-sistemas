import copy
import threading
from abc import ABC, abstractmethod
from datetime import datetime, time, timedelta


class ConfiguracionGlobal:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConfiguracionGlobal, cls).__new__(cls)
            cls._instancia.limite_no_shows = 3
            cls._instancia.dias_suspension = 7
            cls._instancia.horas_cancelacion_estudiante = 2
            cls._instancia.horas_cancelacion_capitan = 24
            cls._instancia.hora_limite_prioridad = time(18, 0)
        return cls._instancia


class ReglaPrioridad(ABC):
    @abstractmethod
    def tiene_prioridad(self, hora_reserva: time) -> bool: pass

class PrioridadAntesDeLas6(ReglaPrioridad):
    def tiene_prioridad(self, hora_reserva: time) -> bool:
        config = ConfiguracionGlobal()
        return hora_reserva < config.hora_limite_prioridad

class SinPrioridad(ReglaPrioridad):
    def tiene_prioridad(self, hora_reserva: time) -> bool:
        return False

class PoliticaCancelacion(ABC):
    @abstractmethod
    def determinar_penalidad(self, reserva, hora_actual: datetime) -> str: pass

class CancelacionEstudiante(PoliticaCancelacion):
    def determinar_penalidad(self, reserva, hora_actual: datetime) -> str:
        config = ConfiguracionGlobal()
        diferencia = reserva.fecha_hora_inicio - hora_actual
        if diferencia.total_seconds() < config.horas_cancelacion_estudiante * 3600:
            return "no-show"
        return "cancelada"

class CancelacionCapitan(PoliticaCancelacion):
    def determinar_penalidad(self, reserva, hora_actual: datetime) -> str:
        config = ConfiguracionGlobal()
        diferencia = reserva.fecha_hora_inicio - hora_actual
        if diferencia.total_seconds() < config.horas_cancelacion_capitan * 3600:
            return "no-show"
        return "cancelada"

class CancelacionAdministrativa(PoliticaCancelacion):
    def determinar_penalidad(self, reserva, hora_actual: datetime) -> str:
        return "anulada"


class Solicitante:
    def __init__(self, nombre: str, regla_prioridad: ReglaPrioridad):
        self.nombre = nombre
        self.regla_prioridad = regla_prioridad
        self.no_shows_mes_actual = 0
        self.fecha_fin_suspension = None

    def verificar_prioridad(self, hora_reserva: time) -> bool:
        return self.regla_prioridad.tiene_prioridad(hora_reserva)

    def esta_suspendido(self, fecha_actual: datetime) -> bool:
        if self.fecha_fin_suspension and fecha_actual < self.fecha_fin_suspension:
            return True
        return False

    def registrar_no_show(self, fecha_actual: datetime):
        config = ConfiguracionGlobal()
        self.no_shows_mes_actual += 1
        if self.no_shows_mes_actual >= config.limite_no_shows:
            self.fecha_fin_suspension = fecha_actual + timedelta(days=config.dias_suspension)

class Estudiante(Solicitante):
    def __init__(self, nombre: str):
        super().__init__(nombre, SinPrioridad())

class CapitanEquipo(Solicitante):
    def __init__(self, nombre: str):
        super().__init__(nombre, PrioridadAntesDeLas6())

class Cancha:
    def __init__(self, id_cancha: str, sede_factory):
        self.id_cancha = id_cancha
        self.sede_factory = sede_factory

class Reserva:
    def __init__(self, cancha: Cancha, solicitante: Solicitante, fecha_hora_inicio: datetime, politica: PoliticaCancelacion):
        self.cancha = cancha
        self.solicitante = solicitante
        self.fecha_hora_inicio = fecha_hora_inicio
        self.politica_cancelacion = politica
        self.estado = "activa"

    def procesar_cancelacion(self, hora_actual: datetime):
        nuevo_estado = self.politica_cancelacion.determinar_penalidad(self, hora_actual)
        self.estado = nuevo_estado
        if nuevo_estado == "no-show":
            self.solicitante.registrar_no_show(hora_actual)
        return self.estado


class FabricaReserva(ABC):
    @abstractmethod
    def crear_reserva(self, cancha: Cancha, solicitante: Solicitante, fecha_hora: datetime) -> Reserva: pass

class FabricaReservaEstudiante(FabricaReserva):
    def crear_reserva(self, cancha: Cancha, solicitante: Solicitante, fecha_hora: datetime) -> Reserva:
        return Reserva(cancha, solicitante, fecha_hora, CancelacionEstudiante())

class FabricaReservaCapitan(FabricaReserva):
    def crear_reserva(self, cancha: Cancha, solicitante: Solicitante, fecha_hora: datetime) -> Reserva:
        return Reserva(cancha, solicitante, fecha_hora, CancelacionCapitan())

class Notificador(ABC):
    @abstractmethod
    def notificar(self, mensaje: str): pass

class NotificadorCorreo(Notificador):
    def notificar(self, mensaje: str): print(f"[Correo Institucional] {mensaje}")

class NotificadorSMS(Notificador):
    def notificar(self, mensaje: str): print(f"[SMS] {mensaje}")

class ValidadorHorario(ABC):
    @abstractmethod
    def es_valido(self, hora: time) -> bool: pass

class ValidadorNorte(ValidadorHorario):
    def es_valido(self, hora: time) -> bool: return time(6, 0) <= hora <= time(22, 0)

class ValidadorSur(ValidadorHorario):
    def es_valido(self, hora: time) -> bool: return time(7, 0) <= hora <= time(23, 0)

class SedeFactory(ABC):
    @abstractmethod
    def crear_notificador(self) -> Notificador: pass
    @abstractmethod
    def crear_validador(self) -> ValidadorHorario: pass
    @abstractmethod
    def get_nombre(self) -> str: pass

class CampusNorteFactory(SedeFactory):
    def crear_notificador(self): return NotificadorCorreo()
    def crear_validador(self): return ValidadorNorte()
    def get_nombre(self): return "Campus Norte"

class CampusSurFactory(SedeFactory):
    def crear_notificador(self): return NotificadorSMS()
    def crear_validador(self): return ValidadorSur()
    def get_nombre(self): return "Campus Sur"

class ReservaRecurrenteBuilder:
    def __init__(self, solicitante: Solicitante, cancha: Cancha, fecha_hora_inicio: datetime):
        self.solicitante = solicitante
        self.cancha = cancha
        self.fecha_hora_inicio = fecha_hora_inicio
        self.semanas = 2
        self.equipo = None
        self.notas = None

    def con_semanas(self, numero: int):
        if 2 <= numero <= 8:
            self.semanas = numero
        return self

    def con_equipo(self, equipo: str):
        self.equipo = equipo
        return self

    def con_notas(self, notas: str):
        self.notas = notas
        return self

    def build_fechas(self) -> list:
        return [self.fecha_hora_inicio + timedelta(weeks=i) for i in range(self.semanas)]


class Bloqueo:
    def __init__(self, motivo: str, equipo_montaje: str):
        self.motivo = motivo
        self.equipo_montaje = equipo_montaje
        self.cancha = None
        self.fecha_hora = None

    def clonar(self):
        return copy.deepcopy(self)


class ReservaFacade:
    def __init__(self):
        self.reservas = []
        self.bloqueos = []
        self.lock = threading.Lock() 

    def _get_fabrica(self, solicitante: Solicitante) -> FabricaReserva:
        if isinstance(solicitante, Estudiante): return FabricaReservaEstudiante()
        return FabricaReservaCapitan()

    def reservar(self, solicitante: Solicitante, cancha: Cancha, fecha_hora: datetime, fecha_actual: datetime):
        if solicitante.esta_suspendido(fecha_actual):
            return "Rechazo: Solicitante suspendido."

        sede = cancha.sede_factory
        if not sede.crear_validador().es_valido(fecha_hora.time()):
            return f"Rechazo: Horario no permitido en {sede.get_nombre()}."

        with self.lock: 
            ocupada = any(r.cancha == cancha and r.fecha_hora_inicio == fecha_hora and r.estado == "activa" for r in self.reservas)
            
            if ocupada:
                return "Rechazo o Conflicto: Cancha ocupada."

            fabrica = self._get_fabrica(solicitante)
            nueva_reserva = fabrica.crear_reserva(cancha, solicitante, fecha_hora)
            self.reservas.append(nueva_reserva)
            
            notificador = sede.crear_notificador()
            notificador.notificar(f"Reserva confirmada en {cancha.id_cancha} para {solicitante.nombre}.")
            return nueva_reserva

    def reservar_recurrente(self, builder: ReservaRecurrenteBuilder, fecha_actual: datetime):
        fechas = builder.build_fechas()
        with self.lock:
            for fecha in fechas:
                ocupada = any(r.cancha == builder.cancha and r.fecha_hora_inicio == fecha and r.estado == "activa" for r in self.reservas)
                if ocupada:
                    return f"Rechazo: Conflicto en la semana {fecha.date()}."
            
            fabrica = self._get_fabrica(builder.solicitante)
            for fecha in fechas:
                self.reservas.append(fabrica.crear_reserva(builder.cancha, builder.solicitante, fecha))
            return "Éxito: Reserva recurrente confirmada."

    def cancelar_reserva(self, reserva: Reserva, hora_actual: datetime):
        with self.lock:
            resultado = reserva.procesar_cancelacion(hora_actual)
            return resultado

    def bloquear_canchas(self, plantilla: Bloqueo, destinos: list, hora_actual: datetime):
        with self.lock:
            for cancha, fecha in destinos:
                clon = plantilla.clonar()
                clon.cancha = cancha
                clon.fecha_hora = fecha
                self.bloqueos.append(clon)
                
                afectadas = [r for r in self.reservas if r.cancha == cancha and r.fecha_hora_inicio == fecha and r.estado == "activa"]
                for r in afectadas:
                    r.politica_cancelacion = CancelacionAdministrativa() 
                    r.procesar_cancelacion(hora_actual)
                    r.cancha.sede_factory.crear_notificador().notificar(f"Reserva anulada por bloqueo administrativo: {clon.motivo}.")