# psets/pset-01/implementacion/simulacion.py
from datetime import datetime
from modelo import SistemaReservaU, Administrador, Cancha, Estudiante, CapitanEquipo, Conflicto

def main():
    sistema = SistemaReservaU()
    admin = Administrador("Administrador Complejo")
    cancha_tenis = Cancha("Cancha Tenis Principal")
    
    estudiante = Estudiante("Estudiante Regular")
    capitan = CapitanEquipo("Capitán Oficial")
    
    fecha_reserva = datetime(2026, 9, 8, 16, 0) # 4:00 PM
    
    print("--- CU-03: GESTIONAR CANCHAS ---")
    sistema.gestionar_cancha("agregar", cancha_tenis)
    
    print("\n--- CU-01: RESERVAR CANCHA (Flujo Principal) ---")
    reserva_estudiante = sistema.reservar_cancha(estudiante, cancha_tenis, fecha_reserva)
    
    print("\n--- CU-01: RESERVAR CANCHA (Flujo Alterno 2b - Conflicto) ---")
    sistema.reservar_cancha(capitan, cancha_tenis, fecha_reserva)
    
    print("\n--- CU-04: INTERVENIR EN CONFLICTO ---")
    sistema.intervenir_conflicto()
    
    print("\n--- CU-02: CANCELAR RESERVA (Flujo Principal) ---")
    # El capitán ganó la reserva en el conflicto anterior. Se cancela con >2 horas.
    reserva_capitan = [r for r in sistema.reservas if r.solicitante == capitan and r.estado == "activa"][0]
    hora_actual_temprano = datetime(2026, 9, 8, 12, 0) 
    sistema.cancelar_reserva(reserva_capitan, hora_actual_temprano)
    
    print("\n--- CU-02: CANCELAR RESERVA (Flujo Alterno 3a - No-Show) ---")
    # Nueva reserva para probar cancelación tardía (< 2 horas)
    reserva_tardia = sistema.reservar_cancha(estudiante, cancha_tenis, datetime(2026, 9, 9, 10, 0))
    hora_actual_tardia = datetime(2026, 9, 9, 9, 0) # Falta solo 1 hora
    sistema.cancelar_reserva(reserva_tardia, hora_actual_tardia)

if __name__ == "__main__":
    main()