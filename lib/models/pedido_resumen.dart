class PedidoResumen {
  const PedidoResumen({
    required this.id,
    required this.nombre,
    required this.telefono,
    required this.total,
    required this.estado,
    required this.fecha,
  });

  final int id;
  final String nombre;
  final String telefono;
  final double total;
  final String estado;
  final DateTime fecha;

  factory PedidoResumen.fromMap(Map<String, dynamic> map) => PedidoResumen(
    id: map['id'] as int,
    nombre: map['nombre'] as String,
    telefono: map['telefono'] as String,
    total: (map['total'] as num).toDouble(),
    estado: map['estado'] as String,
    fecha: DateTime.parse(map['created_at'] as String).toLocal(),
  );
}
