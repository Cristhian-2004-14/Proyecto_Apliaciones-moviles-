enum EstadoReserva {
  solicitada,
  aceptada,
  denegada;

  String get dbValue => switch (this) {
    EstadoReserva.solicitada => 'solicitada',
    EstadoReserva.aceptada => 'aceptada',
    EstadoReserva.denegada => 'denegada',
  };

  String get label => switch (this) {
    EstadoReserva.solicitada => 'EN ESPERA',
    EstadoReserva.aceptada => 'CONFIRMADA',
    EstadoReserva.denegada => 'RECHAZADA',
  };

  static EstadoReserva fromDb(String? value) => EstadoReserva.values.firstWhere(
    (estado) => estado.dbValue == value,
    orElse: () => EstadoReserva.solicitada,
  );
}

class ReservaResumen {
  const ReservaResumen({
    required this.id,
    required this.nombre,
    required this.telefono,
    required this.fecha,
    required this.hora,
    required this.personas,
    required this.estado,
  });

  final int id;
  final String nombre;
  final String telefono;
  final DateTime fecha;
  final String hora;
  final int personas;
  final EstadoReserva estado;

  factory ReservaResumen.fromMap(Map<String, dynamic> map) => ReservaResumen(
    id: (map['id'] as num).toInt(),
    nombre: map['nombre'] as String,
    telefono: map['telefono'] as String,
    fecha: DateTime.parse(map['fecha'] as String),
    hora: map['hora'].toString(),
    personas: (map['personas'] as num).toInt(),
    estado: EstadoReserva.fromDb(map['estado'] as String?),
  );
}
