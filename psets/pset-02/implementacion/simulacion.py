
import threading
import time
from datetime import datetime, timedelta
from modelo import (
    ReservaFacade, Estudiante, CapitanEquipo, Cancha, 
    CampusNorteFactory, CampusSurFactory, ReservaRecurrenteBuilder, Bloqueo
)

def main():
    print("="*50)
    print("INICIANDO SIMULACIÓN RESERVAU - PSET 2")
    print("="*50)

    
    facade = ReservaFacade()
    sede_norte = CampusNorteFactory()
    sede_sur = CampusSurFactory()
    
    cancha_norte_1 = Cancha("Norte-01", sede_norte)
    cancha_norte_2 = Cancha("Norte-02", sede_norte)
    cancha_sur_1 = Cancha("Sur-01", sede_sur)
    
    estudiante = Estudiante("Juan (Estudiante)")
    capitan = CapitanEquipo("Carlos (Capitán)")
    
    
    fecha_actual = datetime(2026, 10, 5, 12, 0) 

    
    print("\n[ESCENARIO 1] Reserva en cada sede (Notificación por canal respectivo):")
    res_norte = facade.reservar(estudiante, cancha_norte_1, fecha_actual + timedelta(days=1, hours=2), fecha_actual)
    res_sur = facade.reservar(capitan, cancha_sur_1, fecha_actual + timedelta(days=1, hours=3), fecha_actual)

   
    print("\n[ESCENARIO 2] Reserva rechazada por horario (Norte cierra 22:00):")
    
    fecha_tarde = fecha_actual.replace(hour=23, minute=0)
    resultado_horario = facade.reservar(estudiante, cancha_norte_2, fecha_tarde, fecha_actual)
    print(resultado_horario)

    
    
    print("\n[ESCENARIO 3] Reserva recurrente (Builder y Todo o Nada):")
   
    fecha_recurrente = fecha_actual + timedelta(days=2)
    builder_exitoso = ReservaRecurrenteBuilder(capitan, cancha_sur_1, fecha_recurrente).con_semanas(3).con_equipo("Balones")
    print(facade.reservar_recurrente(builder_exitoso, fecha_actual))
    
    
    builder_fallido = ReservaRecurrenteBuilder(estudiante, cancha_sur_1, fecha_recurrente).con_semanas(4)
    print("Intento de estudiante en mismo horario...")
    print(facade.reservar_recurrente(builder_fallido, fecha_actual))

   
    print("\n[ESCENARIO 4] Cancelaciones y penalidades dinámicas:")
   
    res_estudiante_cancel = facade.reservar(estudiante, cancha_norte_1, fecha_actual + timedelta(hours=5), fecha_actual)
    print(f"- Estudiante (Faltan 5h): {facade.cancelar_reserva(res_estudiante_cancel, fecha_actual)}")
    
   
    res_capitan_cancel = facade.reservar(capitan, cancha_norte_2, fecha_actual + timedelta(hours=10), fecha_actual)
    print(f"- Capitán (Faltan 10h, límite 24h): {facade.cancelar_reserva(res_capitan_cancel, fecha_actual)}")
    
  
    print("\n[ESCENARIO 5] Suspensión por 3 No-Shows (Regla de 7 días):")
    malo = Estudiante("Pedro (El impuntual)")
    
    for i in range(3):
        r = facade.reservar(malo, cancha_sur_1, fecha_actual + timedelta(days=5+i, hours=1), fecha_actual)
        facade.cancelar_reserva(r, fecha_actual) # Cancela faltando 1 hora -> No Show
    print(f"- Historial de Pedro: {malo.no_shows_mes_actual} No-Shows")
    print(f"- Intento de reserva de Pedro: {facade.reservar(malo, cancha_norte_1, fecha_actual + timedelta(days=10), fecha_actual)}")

   
    print("\n[ESCENARIO 6] Bloqueo masivo y anulación sin penalidad:")
    fecha_evento = fecha_actual + timedelta(days=1)
    
    reserva_victima = facade.reservar(estudiante, cancha_norte_1, fecha_evento, fecha_actual)
    
    plantilla_bloqueo = Bloqueo("Torneo Intercolegial", "Mallas y parlantes")
    destinos = [(cancha_norte_1, fecha_evento), (cancha_norte_2, fecha_evento)]
    
    facade.bloquear_canchas(plantilla_bloqueo, destinos, fecha_actual)
    print(f"- Estado de la reserva víctima tras el bloqueo: {reserva_victima.estado}")

   
    print("\n[ESCENARIO 7] Concurrencia extrema (2 hilos a la misma cancha/hora):")
    fecha_concurrida = fecha_actual + timedelta(days=20)
    resultados_hilos = []

    def intento_reserva(usuario):
        
        res = facade.reservar(usuario, cancha_norte_1, fecha_concurrida, fecha_actual)
        resultados_hilos.append(f"{usuario.nombre}: {res}")

    
    h1 = threading.Thread(target=intento_reserva, args=(estudiante,))
    h2 = threading.Thread(target=intento_reserva, args=(capitan,))
    
  
    h1.start()
    h2.start()
    
   
    h1.join()
    h2.join()
    
    for r in resultados_hilos:
        print(r)
        
    print("\n" + "="*50)
    print("SIMULACIÓN COMPLETADA")
    print("="*50)

if __name__ == "__main__":
    main()