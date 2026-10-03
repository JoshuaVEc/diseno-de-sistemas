# ReservaU - PSet 2: Patrones de Diseño
Joshua Vivero 00341255 
ING. Ciencia de la Computacion
## 1. Tabla de Patrones de Diseño

| Patrón | Requerimiento que lo justifica | Problema que resuelve | Clases y métodos |
| :--- | :--- | :--- | :--- |
| **Strategy** | RF-12, RF-13 | Elimina los condicionales (`if/else`) dentro de la reserva al calcular la penalidad de cancelación. Permite inyectar dinámicamente si el límite es 2h, 24h, o si es una anulación administrativa sin castigo. | `PoliticaCancelacion` (Interfaz), `CancelacionEstudiante`, `CancelacionCapitan`, `CancelacionAdministrativa`, `Reserva.procesar_cancelacion()` |
| **Factory Method** | RF-01, RF-02, RF-12 | Centraliza la decisión de qué tipo de reserva crear y con qué política de cancelación nace, basándose en si el solicitante es Estudiante o Capitán. | `FabricaReserva` (Interfaz), `FabricaReservaEstudiante`, `FabricaReservaCapitan` |
| **Abstract Factory** | RF-17, RF-18 | Asegura que los validadores de horario y los canales de notificación correspondan estrictamente a la misma familia (Sede). Impide que se mezcle la validación del Campus Norte con el SMS del Campus Sur. | `SedeFactory`, `CampusNorteFactory`, `CampusSurFactory`, `Notificador`, `ValidadorHorario` |
| **Builder** | RF-09, RF-10 | Facilita la creación paso a paso de una reserva recurrente, manejando limpiamente sus atributos obligatorios (cancha, fecha) y opcionales (notas, equipo, número de semanas entre 2 y 8). | `ReservaRecurrenteBuilder` |
| **Prototype** | RF-15, RF-16 | Permite definir la configuración de un bloqueo masivo una sola vez (plantilla) y replicarla para múltiples canchas y fechas sin tener que instanciar y configurar desde cero cada vez. | `Bloqueo`, `Bloqueo.clonar()` |
| **Singleton** | RNF-03 | Proporciona un punto de acceso global y único a las variables del negocio (horas límite, cantidad de suspensiones). Evita tener "números mágicos" regados por el código. | `ConfiguracionGlobal`, `ConfiguracionGlobal.__new__()` |
| **Facade** | RNF-03, RF-04 | Oculta la complejidad de interactuar con fábricas, validadores y bloqueos de concurrencia. Provee una interfaz simplificada para que el cliente (`simulacion.py`) ejecute casos de uso directos. | `ReservaFacade`, `ReservaFacade.reservar()`, `ReservaFacade.bloquear_canchas()` |
| **Locking Pesimista** | RNF-04 | Resuelve la condición de carrera (doble reserva) asegurando que solo un hilo a la vez pueda verificar disponibilidad y escribir en la lista de reservas simultáneamente. | `ReservaFacade.lock` (`threading.Lock()`), uso del bloque `with self.lock:` |


## 2. Justificaciones de Diseño

### Prototype: ¿Por qué copy.deepcopy?
Se utilizó `copy.deepcopy()` en lugar de un *shallow copy* (`copy.copy()`) para asegurar que, si en el futuro la entidad `Bloqueo` incluye estructuras de datos mutables complejas (como listas de equipos específicos o sub-horarios), estas referencias no se compartan entre los clones. Si usáramos un *shallow copy*, modificar el equipo de montaje en el clon de la Cancha A alteraría accidentalmente el equipo en el clon de la Cancha B. `deepcopy` garantiza clones 100% independientes.

### Singleton: Ganancias y Costos
Al aplicar Singleton ganamos una fuente de verdad única para los parámetros operativos del sistema; cambiar la ventana de cancelación de 2 a 3 horas ahora requiere modificar solo una línea en todo el sistema. El costo que aceptamos al usar este patrón es la introducción de un estado global oculto, lo cual acopla fuertemente las políticas (`Strategy`) al Singleton y puede hacer que las pruebas unitarias aisladas sean ligeramente más complejas de configurar.

### Concurrencia: Locking Pesimista
Se eligió **Locking Pesimista** (a través de `threading.Lock`) basándonos en el escenario descrito: aunque normalmente hay más lecturas que escrituras, existen *"picos de escritura al inicio de cada semestre"*. En estos picos, la probabilidad de colisión es altísima (muchos estudiantes buscando la misma franja horaria). El locking optimista habría provocado rechazos constantes y reintentos fallidos frustrantes para el usuario durante esos picos. El locking pesimista protege rígidamente la sección crítica de validación y registro, garantizando que el incidente del primer lunes de semestre no vuelva a ocurrir.


## 3. Trazabilidad: Regla de los 3 no-shows

Recorrido de la regla de suspensión a través del diseño:
1. **¿Qué requerimiento la define?** RF-14 ("El sistema debe suspender automáticamente por 7 días... al acumular 3 no-shows").
2. **¿En qué caso de uso y diagrama aparece?** En el Caso de Uso "Cancelar reserva". Aparece explícitamente en el **Diagrama de Actividad** y en el **Diagrama de Robustez** (comunicación entre `ctrlSuspension`, `entPerfil` y `entConfig`).
3. **¿Qué entidad lleva la cuenta y qué método aplica?** La entidad `Solicitante` lleva la cuenta en su atributo `no_shows_mes_actual`. El método que lo evalúa y aplica la suspensión es `registrar_no_show(fecha_actual)`, apoyado por `esta_suspendido()`.
4. **¿Qué valor lee de la configuración?** Lee `config.limite_no_shows` (3) y `config.dias_suspension` (7) de la instancia de `ConfiguracionGlobal`.
5. **¿En qué línea de la salida de simulacion.py se observa?** En el **Escenario 5**, donde se imprime:
   `- Historial de Pedro: 3 No-Shows`
   `- Intento de reserva de Pedro: Rechazo: Solicitante suspendido.`